"""
signup_view.py — Tampilan layar Pendaftaran Akun Baru.
Responsif: koordinat SAMA dengan BankOfSainsData.py asli, diskala via Layout.
"""

import threading
import tkinter as tk
from tkinter import Toplevel

from src.utils import hash_password, generate_card_number
from src.widgets import PlaceholderEntry
from src.image_cache import ImageCache
from src.layout import Layout
from src.email_service import generate_otp, send_otp_email


class SignupView:
    """
    Pendaftaran akun baru.
    Koordinat field diambil dari BankOfSainsData.py (desain 1280×720).
    Layout scaling menangani penyesuaian untuk layar lain.
    """

    # Halaman Syarat & Ketentuan
    _SNK_PAGES = [
        ("images/Frame 69 (5).png", (500, 600)),
        ("images/Frame 70 (1).png", (500, 600)),
        ("images/Frame 73 (1).png", (500, 600)),
        ("images/Frame 72 (1).png", (500, 600)),
        ("images/Frame 71 (1).png", (500, 600)),
    ]

    def __init__(self, parent: tk.Tk, db):
        self._parent = parent
        self._db = db

        self._window = Toplevel(parent)
        self._window.title('BSD — Daftar Akun')
        self._window.attributes('-fullscreen', True)
        self._window.configure(bg="#333333")

        self._L = Layout(self._window)
        self._checkbox_var = tk.BooleanVar()
        self._snk_frame = None
        self._snk_page_index = 0
        self._daftar_btn = None
        self._build_ui()

    def _build_ui(self):
        L = self._L
        sw, sh = L.screen_w, L.screen_h

        # Background penuh
        photo = ImageCache.get("images/Frame 12 (5).png", (sw, sh))
        tk.Label(self._window, image=photo).place(x=0, y=0)

        # ── Entry fields ──────────────────────────────────────────────────
        # Koordinat dari BankOfSainsData.py asli (desain 1280×720):
        # Username (490,170)  Password (490,225)  PIN (490,275)
        # NIM      (490,325)  Deposit  (490,375)  Email (490,425)
        entry_cfg = dict(
            font=('Helvetica', L.font(18)),
            fg="black", bg="#ffffff", border=0, width=17
        )
        field_positions = [
            ("Username",            490, 170),
            ("Password",            490, 225),
            ("PIN",                 490, 275),
            ("NIM",                 490, 325),
            ("Deposit Min. 150000", 490, 375),
            ("Email",               490, 425),
        ]
        self._entries: dict[str, PlaceholderEntry] = {}
        _masked = {"Password", "PIN"}
        for placeholder, dx, dy in field_positions:
            entry = PlaceholderEntry(
                self._window, placeholder=placeholder,
                is_password=(placeholder in _masked), **entry_cfg)
            L.place(entry, dx, dy)
            self._entries[placeholder] = entry

        # ── Syarat & Ketentuan + Checkbox ─────────────────────────────────
        # T&C button: (611, 470), Checkbox: (780, 475)
        tk.Button(self._window, text='Syarat & Ketentuan',
                  font=("Helvetica", L.font(10)),
                  fg="black", bg="#FDCB7F", width=19, border=0,
                  activebackground="#FDCB7F", activeforeground="black",
                  cursor="hand2", command=self._open_tnc
                  ).place(x=L.x(611), y=L.y(470))

        tk.Checkbutton(self._window, variable=self._checkbox_var,
                       activebackground="white", bg="white", border=0,
                       cursor="hand2"
                       ).place(x=L.x(780), y=L.y(475))

        # ── Buttons ───────────────────────────────────────────────────────
        # Daftar: (470, 518), Kembali: (470, 572)
        self._daftar_btn = tk.Button(
            self._window, text='Daftar', font=("Helvetica", L.font(18)),
            command=self._on_signup, fg="black", bg="#FDCB7F",
            width=23, border=0, activebackground="#FDCB7F",
            activeforeground="#ffffff", cursor="hand2")
        L.place(self._daftar_btn, 470, 518)

        tk.Button(self._window, text='Kembali', font=("Helvetica", L.font(18)),
                  command=self._go_back, fg="black", bg="#FDCB7F",
                  width=23, border=0, activebackground="#FDCB7F",
                  activeforeground="#ffffff", cursor="hand2"
                  ).place(x=L.x(470), y=L.y(572))

    # ─── T&C Pagination ──────────────────────────────────────────────────────

    def _open_tnc(self):
        self._snk_page_index = 0
        self._show_snk_page()

    def _show_snk_page(self):
        L = self._L
        if self._snk_frame and self._snk_frame.winfo_exists():
            self._snk_frame.destroy()

        idx = self._snk_page_index
        if idx < 0 or idx >= len(self._SNK_PAGES):
            return

        img_path, (dw, dh) = self._SNK_PAGES[idx]

        # SNK frame di posisi asli (380, 60)
        self._snk_frame = tk.Frame(self._window)
        L.place(self._snk_frame, 380, 60)

        photo = ImageCache.get(img_path, L.img(dw, dh))
        tk.Label(self._snk_frame, image=photo).pack()

        # Tombol navigasi (posisi relatif dalam frame, diskala dari desain)
        if idx < len(self._SNK_PAGES) - 1:
            tk.Button(self._snk_frame, text="▶️", font=('Helvetica', L.font(20)),
                      fg="#ffffff", bg="#FDCB7F", border=0,
                      cursor="hand2", width=3,
                      command=self._snk_next).place(x=L.px(89), y=L.py(540))

        if idx > 0:
            tk.Button(self._snk_frame, text="◀️", font=('Helvetica', L.font(20)),
                      fg="#ffffff", bg="#FDCB7F", border=0,
                      cursor="hand2", width=3,
                      command=self._snk_back).place(x=L.px(27), y=L.py(540))
        else:
            tk.Button(self._snk_frame, text="Kembali", font=('Helvetica', L.font(18)),
                      fg="#ffffff", bg="#FDCB7F", border=0,
                      cursor="hand2", width=8,
                      command=self._snk_frame.destroy).place(x=L.px(350), y=L.py(545))

    def _snk_next(self):
        self._snk_page_index += 1
        self._show_snk_page()

    def _snk_back(self):
        self._snk_page_index -= 1
        self._show_snk_page()

    # ─── Logic ───────────────────────────────────────────────────────────────

    def _go_back(self):
        self._window.destroy()
        self._parent.deiconify()

    def _alert(self, path: str, size=(219, 227)):
        """Tampilkan popup notifikasi di posisi asli (520, 270)."""
        L = self._L
        frame = tk.Frame(self._window)
        # Posisi asli: frame_9.place(x=520, y=270)
        frame.place(x=L.x(520), y=L.y(270))
        photo = ImageCache.get(path, L.img(*size))
        tk.Label(frame, image=photo).pack()
        tk.Button(frame, text="x", fg="#ffffff", bg="#FDCB7F", border=0,
                  cursor="hand2", width=3,
                  command=frame.destroy).place(x=L.px(175), y=L.py(7))

    def _on_signup(self):
        username     = self._entries["Username"].get_value()
        email        = self._entries["Email"].get_value()
        password_raw = self._entries["Password"].get_value()
        pin          = self._entries["PIN"].get_value()
        norek        = self._entries["NIM"].get_value()
        depo         = self._entries["Deposit Min. 150000"].get_value()

        if not self._checkbox_var.get():
            self._alert("images/Frame 43.png"); return
        if not username or self._db.find_user_by_username(username) is not None:
            self._alert("images/Frame 42.png"); return
        if not pin.isdigit() or len(pin) != 6:
            self._alert("images/Frame 29.png"); return
        if (not norek.isdigit() or len(norek) != 11
                or self._db.find_user_by_norek(norek) is not None):
            self._alert("images/Frame 35.png"); return
        if not depo.isdigit() or int(depo) < 150000:
            self._alert("images/Frame 40.png"); return

        self._show_otp_confirm(username, email, password_raw, pin, norek, int(depo))

    def _show_otp_confirm(self, username, email, password_raw, pin, norek, depo):
        L = self._L
        frame_check = tk.Frame(self._window)
        # Posisi asli: frame_check.place(x=470, y=270)
        frame_check.place(x=L.x(470), y=L.y(270))
        photo = ImageCache.get("images/Frame 59 (1).png", L.img(355, 139))
        tk.Label(frame_check, image=photo).pack()

        tk.Button(frame_check, text="X", font=('Helvetica', L.font(10), 'bold'),
                  bg="#fdcb7f", fg="white", border=0,
                  command=frame_check.destroy).place(x=L.px(340), y=L.py(8))

        tk.Button(frame_check, text="Lanjutkan", font=('Helvetica', L.font(14), 'bold'),
                  bg="#ffa41c", fg='black', border=0, width=10,
                  command=lambda: [frame_check.destroy(),
                                   self._send_otp_async(username, email, password_raw,
                                                        pin, norek, depo)]
                  ).place(x=L.px(120), y=L.py(78))

    def _send_otp_async(self, username, email, password_raw, pin, norek, depo):
        L = self._L
        if not email or "@gmail.com" not in email:
            self._alert("images/Frame 44.png"); return

        otp_code = generate_otp()

        loading_frame = tk.Frame(self._window, bg="#FDCB7F", padx=20, pady=12)
        # Loading di posisi yang tidak menghalangi form
        loading_frame.place(x=L.x(440), y=L.y(320))
        tk.Label(loading_frame, text="Mengirim OTP ke email Anda...",
                 font=('Helvetica', L.font(14), 'bold'),
                 bg="#FDCB7F", fg="white").pack()
        dots_lbl = tk.Label(loading_frame, text="●  ○  ○",
                            font=('Helvetica', L.font(12)), bg="#FDCB7F", fg="white")
        dots_lbl.pack()
        dot_states = ["●  ○  ○", "○  ●  ○", "○  ○  ●"]
        dot_idx = [0]

        def animate():
            if loading_frame.winfo_exists():
                dots_lbl.config(text=dot_states[dot_idx[0] % 3])
                dot_idx[0] += 1
                self._window.after(400, animate)

        animate()
        self._daftar_btn.config(state=tk.DISABLED, text="Mengirim...")

        def run():
            success = send_otp_email(email, username, otp_code)
            self._window.after(0, lambda: self._on_email_done(
                success, otp_code, username, email, password_raw,
                pin, norek, depo, loading_frame))

        threading.Thread(target=run, daemon=True).start()

    def _on_email_done(self, success, otp_code, username, email,
                       password_raw, pin, norek, depo, loading_frame):
        if loading_frame.winfo_exists():
            loading_frame.destroy()
        self._daftar_btn.config(state=tk.NORMAL, text="Daftar")
        if success:
            self._show_otp_numpad(username, email, password_raw, pin, norek, depo, otp_code)
        else:
            self._alert("images/Frame 44.png")

    def _show_otp_numpad(self, username, email, password_raw, pin, norek, depo, otp_code):
        L = self._L
        frame_otp = tk.Frame(self._window)
        # Posisi asli: frame_otp.place(x=590, y=270)
        frame_otp.place(x=L.x(590), y=L.y(270))

        photo = ImageCache.get("images/Frame 60 (2).png", L.img(211, 293))
        tk.Label(frame_otp, image=photo).pack()

        otp_var = tk.StringVar()
        tk.Entry(frame_otp, font=('Helvetica', L.font(16), 'bold'),
                 width=12, border=0, bg="#d9d9d9",
                 textvariable=otp_var).place(x=L.px(40), y=L.py(52))

        tk.Button(frame_otp, text="X", font=('Helvetica', L.font(10), 'bold'),
                  bg="#e4b672", fg="white", border=0,
                  command=frame_otp.destroy).place(x=L.px(186), y=L.py(13))

        for label, bx, by in [("1",47,97),("2",97,97),("3",147,95),
                                ("4",47,140),("5",97,140),("6",147,140),
                                ("7",47,185),("8",97,185),("9",147,185)]:
            tk.Button(frame_otp, text=label, font=('Helvetica', L.font(13), 'bold'),
                      bg="#d9d9d9", border=0,
                      command=lambda d=label: otp_var.set(otp_var.get() + d)
                      ).place(x=L.px(bx), y=L.py(by))

        tk.Button(frame_otp, text="0", font=('Helvetica', L.font(13), 'bold'),
                  bg="#d9d9d9", border=0,
                  command=lambda: otp_var.set(otp_var.get() + "0")
                  ).place(x=L.px(97), y=L.py(230))
        tk.Button(frame_otp, text="⬅", font=('Helvetica', L.font(16), 'bold'),
                  border=0, bg="#e4b672", fg="white",
                  command=lambda: otp_var.set("")
                  ).place(x=L.px(29), y=L.py(240))
        tk.Button(frame_otp, text="✅", font=('Helvetica', L.font(16), 'bold'),
                  border=0, bg="#FDCB7F", fg="white",
                  command=lambda: self._verify_and_create(
                      otp_var.get(), otp_code, username, email,
                      password_raw, pin, norek, depo, frame_otp
                  )).place(x=L.px(140), y=L.py(240))

    def _verify_and_create(self, entered_otp, correct_otp,
                            username, email, password_raw, pin, norek, depo, frame_otp):
        if entered_otp != correct_otp:
            self._alert("images/Frame 62.png"); return
        password = hash_password(password_raw)
        nomor_kartu = generate_card_number()
        self._db.create_user(username=username, password=password, balance=depo,
                             pin=pin, norek=norek, nomor_kartu=nomor_kartu, email=email)
        frame_otp.destroy()
        self._window.destroy()
        self._parent.deiconify()
