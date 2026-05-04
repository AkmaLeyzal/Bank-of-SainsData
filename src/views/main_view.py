"""
main_view.py — Tampilan Dashboard Utama Bank of Sains Data.
Responsif: semua koordinat & font diskala otomatis via Layout.
"""

import time
import locale
import tkinter as tk
from tkinter import Toplevel, ttk, LEFT, RIGHT, BOTH, Y, VERTICAL

from src.image_cache import ImageCache
from src.layout import Layout
from src.transactions.transfer import TransferHandler
from src.transactions.deposit import DepositHandler
from src.transactions.withdraw import WithdrawHandler
from src.transactions.ecommerce import EcommerceHandler
from src.widgets import PlaceholderEntry

# Auto-logout setelah 5 menit tidak aktif (dalam milidetik)
_IDLE_TIMEOUT_MS = 300_000


class MainView:
    """
    Dashboard utama setelah login.
    Menampilkan: saldo, jam, riwayat transaksi, tombol-tombol transaksi.
    Semua elemen diskala otomatis sesuai resolusi layar aktual.
    """

    def __init__(self, parent: tk.Tk, db, username: str, password: str, user_data: dict):
        self._parent = parent
        self._db = db
        self._user_data = user_data  # Simpan data user dari login, tidak query ulang

        self._mains = Toplevel(parent)
        self._mains.attributes('-fullscreen', True)
        self._mains.configure(bg="black")

        self._L = Layout(self._mains)

        self._state = {
            'username': username,
            'password': password,
            'login_username': user_data.get('username'),
            'balance': int(user_data.get('balance', 0)),
            'click_count': 0,
            'show_balance_callback': self.show_balance,
            'norek_tujuan': None,
            'nominalTF': None,
            'layout': self._L,
        }

        self._my_canvas = None
        self._time_label = None
        self._date_label = None
        self._balance_label = None
        self._idle_timer = None

        self._build_ui()
        self._setup_idle_timer()
        self._mains.mainloop()

    # ─── Idle Auto-Logout ─────────────────────────────────────────────────────

    def _setup_idle_timer(self):
        """Pasang listener untuk reset idle timer setiap ada aktivitas user."""
        self._reset_idle_timer()
        self._mains.bind_all("<Any-KeyPress>", lambda e: self._reset_idle_timer())
        self._mains.bind_all("<Any-Button>", lambda e: self._reset_idle_timer())
        self._mains.bind_all("<Motion>", lambda e: self._reset_idle_timer())

    def _reset_idle_timer(self):
        """Reset countdown auto-logout. Dipanggil setiap ada input user."""
        if self._idle_timer:
            self._mains.after_cancel(self._idle_timer)
        self._idle_timer = self._mains.after(_IDLE_TIMEOUT_MS, self._auto_logout)

    def _auto_logout(self):
        """Logout otomatis karena tidak ada aktivitas."""
        self._mains.destroy()
        self._parent.deiconify()

    # ─── UI Builder ──────────────────────────────────────────────────────────

    def _build_ui(self):
        L = self._L
        sw, sh = L.screen_w, L.screen_h

        # Background — selalu full layar
        photo = ImageCache.get("images/Frame 24 (4).png", (sw, sh))
        tk.Label(self._mains, image=photo).place(x=0, y=0)

        self._build_transfer_section()
        self._build_action_buttons()
        self._build_icon_buttons()
        self._build_info_widgets()
        self._build_history_panel()

        # Tombol show/hide saldo
        tk.Button(self._mains, text='👁', command=self._toggle_balance,
                  border=0, font=('Helvetica', L.font(15)),
                  bg='white', fg="#FDCB7F"
                  ).place(x=L.x(422), y=L.y(146))

        # Label saldo tersembunyi
        self._balance_label = tk.Label(
            self._mains, text='● ● ● ● ●',
            font=('Helvetica', L.font(22)), bg='white', fg="black",
            width=14, anchor="w"
        )
        self._balance_label.place(x=L.x(183), y=L.y(146))

        # Logout
        tk.Button(self._mains, text='LOGOUT', font=("Helvetica", L.font(15)),
                  command=self._on_logout, fg="#ffffff", bg="#E4B672", border=0,
                  activebackground="#E4B672", activeforeground="#ffffff",
                  cursor="hand2", width=11
                  ).place(x=L.x(1140), y=L.y(13))

        self._update_time()
        self._load_history()

    def _build_transfer_section(self):
        L = self._L
        norek_entry = PlaceholderEntry(
            self._mains, placeholder="No. Rek Tujuan",
            placeholder_color="#777777", text_color="black",
            font=('Helvetica', L.font(20)), fg="#777777", bg="white",
            width=19, border=0
        )
        norek_entry.place(x=L.x(535), y=L.y(152))
        self._state['norek_tujuan'] = norek_entry

        nominal_entry = PlaceholderEntry(
            self._mains, placeholder="Nominal",
            placeholder_color="#777777", text_color="black",
            font=('Helvetica', L.font(20)), fg="#777777", bg="white",
            width=19, border=0
        )
        nominal_entry.place(x=L.x(540), y=L.y(212))
        self._state['nominalTF'] = nominal_entry

        tk.Button(self._mains, text='TRANSFER', font=("Helvetica", L.font(15), 'bold'),
                  command=self._on_transfer, fg="white", bg="#fdcb7f", border=0,
                  activebackground="#FDCB7F", activeforeground="white",
                  cursor="hand2", width=25
                  ).place(x=L.x(540), y=L.y(278))

        # Tombol info
        tk.Button(self._mains, text="i", font=('Helvetica', L.font(12), 'bold'),
                  fg="white", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="white",
                  cursor="hand2", width=2, anchor='center',
                  command=self._show_transfer_info
                  ).place(x=L.x(830), y=L.y(105))

    def _build_action_buttons(self):
        L = self._L
        actions = [
            ("DEPOSIT",    380, self._on_deposit),
            ("WITHDRAW",   480, self._on_withdraw),
            ("E-Commerce", 588, self._on_ecommerce),
        ]
        for text, dy, cmd in actions:
            tk.Button(self._mains, text=text, command=cmd,
                      font=("Helvetica", L.font(20), 'bold'),
                      fg="white", bg="#FDCB7F", border=0,
                      activebackground="#FDCB7F", activeforeground="white",
                      cursor="hand2", width=14
                      ).place(x=L.x(212), y=L.y(dy))

    def _build_icon_buttons(self):
        L = self._L
        icon_size = L.img(90, 90)
        icons = [
            ("images/Frame 54 (1).png", 946, self._on_deposit),
            ("images/Frame 55 (1).png", 1055, self._on_withdraw),
            ("images/Frame 53 (1).png", 1169, self._on_ecommerce),
        ]
        for path, dx, cmd in icons:
            photo = ImageCache.get(path, icon_size)
            btn = tk.Button(self._mains, command=cmd, cursor="hand2",
                            image=photo, border=0)
            btn.place(x=L.x(dx), y=L.y(247))

    def _build_info_widgets(self):
        L = self._L
        login_name = self._state['login_username']
        # Gunakan data user dari login, tidak query DB ulang
        my_norek = int(self._user_data.get('nomor_rekening', 0))
        my_card  = self._user_data.get('nomor_kartu', '')

        # Greeting
        tk.Label(self._mains, font=('Encode Sans Semi Condensed', L.font(22), 'bold'),
                 bg='white', width=18,
                 text=f"Welcome, {login_name.split()[0] if login_name else ''}"
                 ).place(x=L.x(935), y=L.y(87))

        # Jam
        self._time_label = tk.Label(self._mains, font=('Helvetica', L.font(45), 'bold'),
                                    bg='white', width=9)
        self._time_label.place(x=L.x(935), y=L.y(120))

        # Tanggal
        self._date_label = tk.Label(self._mains, font=('Helvetica', L.font(20), 'bold'),
                                    bg='white', width=18)
        self._date_label.place(x=L.x(955), y=L.y(198))

        # Norek
        tk.Label(self._mains, font=('Helvetica', L.font(14), 'bold'),
                 bg='white', fg="black", width=18, anchor='w',
                 text=str(my_norek)).place(x=L.x(515), y=L.y(667))

        # Kartu
        tk.Label(self._mains, font=('Helvetica', L.font(14), 'bold'),
                 bg='#77878c', border=0, fg="white",
                 text=str(my_card)).place(x=L.x(510), y=L.y(565))

    def _build_history_panel(self):
        L = self._L
        frame_h = tk.Frame(self._mains)
        frame_h.place(x=L.x(932), y=L.y(387))

        canvas_w = L.px(320)
        canvas_h = L.py(320)
        self._my_canvas = tk.Canvas(frame_h, width=canvas_w, height=canvas_h, bg="white")
        self._my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = ttk.Scrollbar(frame_h, orient=VERTICAL, command=self._my_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._my_canvas.configure(yscrollcommand=scrollbar.set)
        self._my_canvas.bind(
            "<Configure>",
            lambda e: self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))
        )

    # ─── Balance Show/Hide ───────────────────────────────────────────────────

    def show_balance(self):
        locale.setlocale(locale.LC_NUMERIC, 'id_ID')
        balance_fmt = locale.format_string("%d", self._state['balance'], grouping=True)
        self._balance_label.config(
            text=f'Rp. {balance_fmt}',
            font=('Helvetica', self._L.font(18), 'bold'))

    def hide_balance(self):
        self._balance_label.config(
            text='● ● ● ● ●',
            font=('Helvetica', self._L.font(22)))

    def _toggle_balance(self):
        count = self._state['click_count']
        self.hide_balance() if count % 2 == 1 else self.show_balance()
        self._state['click_count'] = count + 1

    # ─── History ─────────────────────────────────────────────────────────────

    def _load_history(self):
        rows = self._db.get_history(self._state['login_username'])
        for row in rows:
            t_type = row.get('transaction_type')
            nominal = row.get('nominal_transaction')
            ts = row.get('time_transaction')
            try:
                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                nom_fmt = locale.format_string("%d", nominal, grouping=True)
                nom_str = (f"+{nom_fmt}" if "Deposit" in (t_type or "")
                           or t_type == "Transfer " else f"-{nom_fmt}")
            except Exception:
                nom_str = str(nominal)
            self._add_history_item(t_type, nom_str, ts)

    def _add_history_item(self, t_type: str, nominal_fmt: str, timestamp: str):
        L = self._L
        frame_h = tk.LabelFrame(self._my_canvas)
        photo = ImageCache.get("images/Frame 42.png", L.img(320, 80))
        tk.Label(frame_h, image=photo).pack()

        tk.Label(frame_h, text=t_type, font=('Comic Sans', L.font(17)),
                 bg="#F6C57B", border=0, width=10, anchor='w').place(x=2, y=2)

        tk.Label(frame_h, text=timestamp, font=('Comic Sans', L.font(10)),
                 bg="#E4B672", border=0, width=15).place(x=L.px(200), y=L.py(60))

        tk.Label(frame_h, text=nominal_fmt, font=('Comic Sans', L.font(20)),
                 bg="#F6C57B", anchor='e', border=0, width=12).place(x=L.px(130), y=2)

        y_pos = len(self._my_canvas.winfo_children()) * L.py(80)
        self._my_canvas.create_window((0, y_pos), window=frame_h, anchor="nw")
        self._my_canvas.update_idletasks()
        self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))

    # ─── Timer ───────────────────────────────────────────────────────────────

    def _update_time(self):
        self._time_label['text'] = time.strftime('%H:%M:%S')
        self._date_label['text'] = f"    {time.strftime('%A')}, {time.strftime('%d-%m-%Y')}     "
        self._mains.after(1000, self._update_time)

    # ─── Transaction Handlers ─────────────────────────────────────────────────

    def _on_transfer(self):
        TransferHandler(self._mains, self._db, self._state).execute()

    def _on_deposit(self):
        DepositHandler(self._mains, self._db, self._state).open_form()

    def _on_withdraw(self):
        WithdrawHandler(self._mains, self._db, self._state).open_form()

    def _on_ecommerce(self):
        EcommerceHandler(self._mains, self._db, self._state).open_menu()

    # ─── Info & Logout ────────────────────────────────────────────────────────

    def _show_transfer_info(self):
        L = self._L
        info_frame = tk.Frame(self._mains)
        # Posisi asli: info_frame.place(x=495, y=80)
        info_frame.place(x=L.x(495), y=L.y(80))
        photo = ImageCache.get("images/Frame 78.png", L.img(379, 257))
        tk.Label(info_frame, image=photo).pack()

        tk.Button(info_frame, text="x", font=('Helvetica', L.font(18), 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  cursor="hand2", width=3,
                  command=info_frame.destroy).place(x=L.px(330), y=L.py(3))

    def _on_logout(self):
        L = self._L
        frame_logout = tk.Frame(self._mains)
        # Posisi asli: frame_logout.place(x=440, y=270)
        frame_logout.place(x=L.x(440), y=L.y(270))
        photo = ImageCache.get("images/Frame 51.png", L.img(520, 187))
        tk.Label(frame_logout, image=photo).pack()

        def do_logout():
            frame_logout.destroy()
            self._mains.destroy()
            self._parent.deiconify()

        tk.Button(frame_logout, text="Iya", font=('Helvetica', L.font(18), 'bold'),
                  fg="black", bg="#ffa41c", border=0, cursor="hand2", width=10,
                  command=do_logout).place(x=L.px(297), y=L.py(105))

        tk.Button(frame_logout, text="Tidak", font=('Helvetica', L.font(18), 'bold'),
                  fg="black", bg="#FDCB7F", border=0, cursor="hand2", width=10,
                  command=frame_logout.destroy).place(x=L.px(75), y=L.py(105))
