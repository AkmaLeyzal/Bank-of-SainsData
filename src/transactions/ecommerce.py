"""
ecommerce.py — Handler logika E-Commerce (Pulsa & Token Listrik).
"""

import random
import tkinter as tk

from src.image_cache import ImageCache
from src.utils import format_currency, generate_resi, current_time_date, save_receipt
from src.widgets import PinPadDialog, AlertFrame
from src.rate_limiter import pin_limiter
from src.audit_log import log_pin_failed, log_pin_locked, log_transaction
from src.validators import validate_nominal, validate_phone, validate_token_listrik


class EcommerceHandler:
    """Mengelola fitur E-Commerce: Pulsa dan Token Listrik."""

    def __init__(self, parent_frame, db, app_state: dict):
        self._parent = parent_frame
        self._db = db
        self._state = app_state
        self._frame_e = None   # Frame menu utama ecommerce
        self._frame_p = None   # Frame form pulsa
        self._frame_l = None   # Frame form listrik

    def _show_text_alert(self, message: str):
        frame = tk.Frame(self._parent, bg="#e74c3c", padx=20, pady=20)
        frame.place(x=440, y=280)
        tk.Label(frame, text=message, font=('Helvetica', 12, 'bold'),
                 bg="#e74c3c", fg="white").pack()
        tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0, width=8,
                  font=('Helvetica', 10), command=frame.destroy).pack(pady=10)

    # ─── Menu Ecommerce ──────────────────────────────────────────────────────

    def open_menu(self):
        """Buka menu utama E-Commerce."""
        self._frame_e = tk.Frame(self._parent)
        self._frame_e.place(x=400, y=90)

        photo = ImageCache.get("images/Frame 16 (1).png", (528, 628))
        tk.Label(self._frame_e, image=photo).pack()

        tk.Button(self._frame_e, text='Pulsa', font=("Helvetica", 17, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=22,
                  command=self.open_pulsa).place(x=105, y=107)

        tk.Button(self._frame_e, text='Beli Listrik', font=("Helvetica", 17, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=22,
                  command=self.open_listrik).place(x=105, y=190)

        tk.Button(self._frame_e, text='X', font=("Helvetica", 21, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=3,
                  command=self._frame_e.destroy).place(x=473, y=9)

    # ─── Pulsa ───────────────────────────────────────────────────────────────

    def open_pulsa(self):
        """Buka form beli pulsa."""
        self._frame_p = tk.Frame(self._parent)
        self._frame_p.place(x=400, y=90)

        photo = ImageCache.get("images/Frame 17 (2).png", (520, 620))
        tk.Label(self._frame_p, image=photo).pack()

        # Entry nominal pulsa
        self._nominal_pulsa = tk.Entry(self._frame_p, font=('Helvetica', 20),
                                        fg="#777777", bg="white", width=19, border=0)
        self._nominal_pulsa.place(y=194, x=118)
        self._nominal_pulsa.insert(0, "Nominal")
        self._nominal_pulsa.bind('<FocusIn>',
            lambda e: self._clear_if_placeholder(self._nominal_pulsa, "Nominal"))
        self._nominal_pulsa.bind('<FocusOut>',
            lambda e: self._restore_placeholder(self._nominal_pulsa, "Nominal"))

        # Entry nomor HP
        self._no_hp = tk.Entry(self._frame_p, font=('Helvetica', 20),
                                fg="#777777", bg="white", width=19, border=0)
        self._no_hp.place(x=118, y=279)
        self._no_hp.insert(0, "No. Handphone")
        self._no_hp.bind('<FocusIn>',
            lambda e: self._clear_if_placeholder(self._no_hp, "No. Handphone"))
        self._no_hp.bind('<FocusOut>',
            lambda e: self._restore_placeholder(self._no_hp, "No. Handphone"))

        tk.Button(self._frame_p, text='Lanjut', font=("Helvetica", 17, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=21,
                  command=self._validate_pulsa).place(x=110, y=357)

        tk.Button(self._frame_p, text='X', font=("Helvetica", 21, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=3,
                  command=self._frame_p.destroy).place(x=465, y=9)

    def _validate_pulsa(self):
        nominal_str = self._get_entry_value(self._nominal_pulsa, "Nominal")
        no_hp = self._get_entry_value(self._no_hp, "No. Handphone")
        balance = self._state['balance']
        username = self._state['username']
        password = self._state['password']

        row = self._db.find_user(username, password)
        if row is None:
            return
        my_norek = int(row.get('nomor_rekening'))

        if not nominal_str.isdigit():
            AlertFrame(self._parent, "images/Frame 36 (1).png"); return
        nominal = int(nominal_str)

        if nominal < 10000:
            AlertFrame(self._parent, "images/Frame 48.png"); return
        if balance < nominal:
            AlertFrame(self._parent, "images/Frame 37.png"); return
        if balance - nominal < 20000:
            AlertFrame(self._parent, "images/Frame 49.png"); return
        if not no_hp.isdigit():
            AlertFrame(self._parent, "images/Frame 41.png"); return
        if not (12 <= len(no_hp) <= 13):
            AlertFrame(self._parent, "images/Frame 21.png"); return

        angka_tf = format_currency(nominal)
        self._show_confirmation_pulsa(my_norek, nominal, angka_tf)

    def _show_confirmation_pulsa(self, my_norek, nominal, angka_tf):
        login_name = self._state['login_username']
        frame_k = tk.Frame(self._parent)
        frame_k.place(x=420, y=200)

        photo = ImageCache.get("images/Frame 47 (2).png", (520, 302))
        tk.Label(frame_k, image=photo).pack()

        for text, y in [(login_name, 90), (my_norek, 120),
                        ('Pembelian Pulsa', 150), (angka_tf, 183)]:
            tk.Label(frame_k, text=text, width=24, border=0, anchor='w',
                     font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=y)

        tk.Button(frame_k, text='Batal', width=12, border=0, font=('Helvetica', 16, 'bold'),
                  bg="#fdcb7f", fg='black', activebackground="#fdcb7f",
                  command=frame_k.destroy).place(x=80, y=240)

        tk.Button(frame_k, text='Lanjut', width=12, border=0, font=('Helvetica', 16, 'bold'),
                  bg="#ffa41c", fg='black', activebackground="#ffa41c",
                  command=lambda: [frame_k.destroy(),
                                   self._show_pin_pulsa(my_norek, nominal, angka_tf)]
                  ).place(x=310, y=240)

    def _show_pin_pulsa(self, my_norek, nominal, angka_tf):
        pad = PinPadDialog(
            self._parent,
            on_submit=lambda pin: self._process_pulsa(pin, my_norek, nominal, angka_tf, pad)
        )
        pad.frame.place(x=590, y=270)

    def _process_pulsa(self, pin: str, my_norek, nominal, angka_tf, pad):
        pad.destroy()
        username = self._state['username']
        password = self._state['password']
        login_name = self._state['login_username']

        # Rate limiting PIN
        if not pin_limiter.is_allowed(username):
            remaining = pin_limiter.remaining_lockout(username)
            frame = tk.Frame(self._parent)
            frame.place(x=500, y=300)
            tk.Label(frame, text=f"PIN terkunci!\nCoba lagi dalam {remaining} detik.",
                     font=('Helvetica', 14, 'bold'),
                     bg="#e74c3c", fg="white", padx=20, pady=15).pack()
            tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0,
                      width=8, command=frame.destroy).pack(pady=5)
            return

        if len(pin) != 6:
            AlertFrame(self._parent, "images/Frame 29.png"); return
        pin_row = self._db.find_user_by_pin(username, password, pin)
        if pin_row is None:
            pin_limiter.record_failure(username)
            log_pin_failed(username, "pulsa")
            AlertFrame(self._parent, "images/Frame 34.png"); return

        pin_limiter.reset(username)

        new_balance = self._state['balance'] - nominal
        self._state['balance'] = new_balance
        self._db.set_balance(login_name, new_balance)
        self._db.insert_transaction(login_name, "Pulsa", nominal)
        log_transaction(login_name, "Pulsa", nominal)

        if self._state.get('click_count', 0) % 2 == 1:
            self._state['show_balance_callback']()

        no_resi = generate_resi("P")
        cur_time, cur_date = current_time_date()
        save_receipt("pulsa", angka_tf, no_resi, login_name, new_balance)

        for f in [self._frame_p, self._frame_e]:
            if f and f.winfo_exists():
                f.destroy()

        self._show_receipt_pulsa(login_name, my_norek, angka_tf, cur_time, cur_date, no_resi)

    def _show_receipt_pulsa(self, name, my_norek, angka_tf, cur_time, cur_date, no_resi):
        frame_r = tk.Frame(self._parent)
        frame_r.place(x=550, y=250)

        photo = ImageCache.get("images/Frame 10.png", (211, 293))
        tk.Label(frame_r, image=photo).pack()

        tk.Button(frame_r, text="X", font=('Helvetica', 10, 'bold'),
                  bg="#e4b672", fg="white", border=0,
                  command=frame_r.destroy).place(x=180, y=9)

        items = [(name, 75), (my_norek, 97), ('PEMBELIAN PULSA', 119),
                 (angka_tf, 139), (f'{cur_time}, {cur_date}', 160), (no_resi, 183)]
        for text, y in items:
            tk.Label(frame_r, text=text, width=18 if y != 119 else 20, border=0, anchor='w',
                     font=('Helvetica', 9 if y != 119 else 8), bg="#fdcb7f").place(x=80, y=y)

    # ─── Listrik ─────────────────────────────────────────────────────────────

    def open_listrik(self):
        """Buka form beli token listrik."""
        self._frame_l = tk.Frame(self._parent)
        self._frame_l.place(x=400, y=90)

        photo = ImageCache.get("images/Frame 18 (2).png", (520, 620))
        tk.Label(self._frame_l, image=photo).pack()

        self._nominal_listrik = tk.Entry(self._frame_l, font=('Helvetica', 20),
                                          fg="#777777", bg="white", width=19, border=0)
        self._nominal_listrik.place(y=196, x=118)
        self._nominal_listrik.insert(0, "Nominal")
        self._nominal_listrik.bind('<FocusIn>',
            lambda e: self._clear_if_placeholder(self._nominal_listrik, "Nominal"))
        self._nominal_listrik.bind('<FocusOut>',
            lambda e: self._restore_placeholder(self._nominal_listrik, "Nominal"))

        self._no_token = tk.Entry(self._frame_l, font=('Helvetica', 20),
                                   fg="#777777", bg="white", width=19, border=0)
        self._no_token.place(x=118, y=279)
        self._no_token.insert(0, "No. Token Listrik")
        self._no_token.bind('<FocusIn>',
            lambda e: self._clear_if_placeholder(self._no_token, "No. Token Listrik"))
        self._no_token.bind('<FocusOut>',
            lambda e: self._restore_placeholder(self._no_token, "No. Token Listrik"))

        tk.Button(self._frame_l, text='Lanjut', font=("Helvetica", 17, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=21,
                  command=self._validate_listrik).place(x=110, y=357)

        tk.Button(self._frame_l, text='X', font=("Helvetica", 21, 'bold'),
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=3,
                  command=self._frame_l.destroy).place(x=465, y=9)

    def _validate_listrik(self):
        nominal_str = self._get_entry_value(self._nominal_listrik, "Nominal")
        token_str = self._get_entry_value(self._no_token, "No. Token Listrik")
        balance = self._state['balance']
        username = self._state['username']
        password = self._state['password']

        row = self._db.find_user(username, password)
        if row is None:
            return
        my_norek = int(row.get('nomor_rekening'))

        if not nominal_str.isdigit():
            AlertFrame(self._parent, "images/Frame 36 (1).png"); return
        nominal = int(nominal_str)

        if nominal < 10000:
            AlertFrame(self._parent, "images/Frame 48.png"); return
        if balance < nominal:
            AlertFrame(self._parent, "images/Frame 37.png"); return
        if balance - nominal < 20000:
            AlertFrame(self._parent, "images/Frame 49.png"); return
        if not token_str.isdigit() or not (12 <= len(token_str) <= 13):
            AlertFrame(self._parent, "images/Frame 26.png"); return

        angka_tf = format_currency(nominal)
        self._show_confirmation_listrik(my_norek, nominal, angka_tf)

    def _show_confirmation_listrik(self, my_norek, nominal, angka_tf):
        login_name = self._state['login_username']
        frame_k = tk.Frame(self._parent)
        frame_k.place(x=420, y=200)

        photo = ImageCache.get("images/Frame 47 (2).png", (520, 302))
        tk.Label(frame_k, image=photo).pack()

        for text, y in [(login_name, 90), (my_norek, 120),
                        ('Pembelian Listrik', 150), (angka_tf, 183)]:
            tk.Label(frame_k, text=text, width=24, border=0, anchor='w',
                     font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=y)

        tk.Button(frame_k, text='Batal', width=12, border=0, font=('Helvetica', 16, 'bold'),
                  bg="#fdcb7f", fg='black', activebackground="#fdcb7f",
                  command=frame_k.destroy).place(x=80, y=240)

        tk.Button(frame_k, text='Lanjut', width=12, border=0, font=('Helvetica', 16, 'bold'),
                  bg="#ffa41c", fg='black', activebackground="#ffa41c",
                  command=lambda: [frame_k.destroy(),
                                   self._show_pin_listrik(my_norek, nominal, angka_tf)]
                  ).place(x=310, y=240)

    def _show_pin_listrik(self, my_norek, nominal, angka_tf):
        pad = PinPadDialog(
            self._parent,
            on_submit=lambda pin: self._process_listrik(pin, my_norek, nominal, angka_tf, pad)
        )
        pad.frame.place(x=590, y=270)

    def _process_listrik(self, pin: str, my_norek, nominal, angka_tf, pad):
        pad.destroy()
        username = self._state['username']
        password = self._state['password']
        login_name = self._state['login_username']

        # Rate limiting PIN
        if not pin_limiter.is_allowed(username):
            remaining = pin_limiter.remaining_lockout(username)
            frame = tk.Frame(self._parent)
            frame.place(x=500, y=300)
            tk.Label(frame, text=f"PIN terkunci!\nCoba lagi dalam {remaining} detik.",
                     font=('Helvetica', 14, 'bold'),
                     bg="#e74c3c", fg="white", padx=20, pady=15).pack()
            tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0,
                      width=8, command=frame.destroy).pack(pady=5)
            return

        if len(pin) != 6:
            AlertFrame(self._parent, "images/Frame 29.png"); return
        pin_row = self._db.find_user_by_pin(username, password, pin)
        if pin_row is None:
            pin_limiter.record_failure(username)
            log_pin_failed(username, "listrik")
            AlertFrame(self._parent, "images/Frame 34.png"); return

        pin_limiter.reset(username)

        # Generate token listrik
        token_number = random.randint(0, 99999999999999999999)
        formatted_number = f'{token_number:020}'
        results = '-'.join([formatted_number[i:i + 4] for i in range(0, len(formatted_number), 4)])

        new_balance = self._state['balance'] - nominal
        self._state['balance'] = new_balance
        self._db.set_balance(login_name, new_balance)
        self._db.insert_transaction(login_name, "Listrik", nominal)

        if self._state.get('click_count', 0) % 2 == 1:
            self._state['show_balance_callback']()

        no_resi = generate_resi("L")
        cur_time, cur_date = current_time_date()
        save_receipt("Pembelian Pulsa Listrik", angka_tf, no_resi,
                     login_name, new_balance, token=results)

        for f in [self._frame_l, self._frame_e]:
            if f and f.winfo_exists():
                f.destroy()

        self._show_receipt_listrik(login_name, my_norek, angka_tf,
                                   cur_time, cur_date, no_resi, results)

    def _show_receipt_listrik(self, name, my_norek, angka_tf, cur_time, cur_date,
                               no_resi, token):
        frame_r = tk.Frame(self._parent)
        frame_r.place(x=550, y=250)

        photo = ImageCache.get("images/Frame 10.png", (211, 293))
        tk.Label(frame_r, image=photo).pack()

        tk.Button(frame_r, text="X", font=('Helvetica', 10, 'bold'),
                  bg="#e4b672", fg="white", border=0,
                  command=frame_r.destroy).place(x=180, y=9)

        items = [(name, 75), (my_norek, 97), ('Pembelian Token Listrik', 119),
                 (angka_tf, 139), (f'{cur_time}, {cur_date}', 160), (no_resi, 183)]
        for text, y in items:
            tk.Label(frame_r, text=text, width=18 if y != 119 else 21, border=0, anchor='w',
                     font=('Helvetica', 9 if y != 119 else 8), bg="#fdcb7f").place(x=80, y=y)

        tk.Label(frame_r, text='No. Token', width=15, border=0, anchor='w',
                 font=('Helvetica', 10), bg="#fdcb7f").place(x=80, y=220)
        tk.Label(frame_r, text=token, width=22, border=0, anchor='w',
                 font=('Helvetica', 10), bg="#fdcb7f").place(x=30, y=240)

    # ─── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _clear_if_placeholder(entry: tk.Entry, placeholder: str):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    @staticmethod
    def _restore_placeholder(entry: tk.Entry, placeholder: str):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#777777")

    @staticmethod
    def _get_entry_value(entry: tk.Entry, placeholder: str) -> str:
        val = entry.get()
        return "" if val == placeholder else val
