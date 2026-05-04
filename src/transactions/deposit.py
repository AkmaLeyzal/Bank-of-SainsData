"""
deposit.py — Handler logika Deposit (Setor Tunai).
"""

import tkinter as tk

from src.image_cache import ImageCache
from src.utils import format_currency, generate_resi, current_time_date, save_receipt
from src.widgets import PinPadDialog, AlertFrame


class DepositHandler:
    """Mengelola alur transaksi Deposit."""

    def __init__(self, parent_frame, db, app_state: dict):
        self._parent = parent_frame
        self._db = db
        self._state = app_state
        self._frame_d = None

    def open_form(self):
        """Buka form input nominal deposit."""
        self._frame_d = tk.Frame(self._parent)
        self._frame_d.place(x=420, y=200)

        photo = ImageCache.get("images/Frame 14 (2).png", (450, 300))
        tk.Label(self._frame_d, image=photo).pack()

        tk.Button(self._frame_d, text="X", font=('Helvetica', 13, 'bold'),
                  border=0, bg="#e8bf83", fg="white", activebackground="#e8bf83",
                  activeforeground="white",
                  command=self._frame_d.destroy).place(x=409, y=21)

        self._nominal_entry = tk.Entry(self._frame_d, width=17, border=0,
                                       bg="#ffffff", font=('Helvetica', 20))
        self._nominal_entry.place(x=94, y=108)

        tk.Button(self._frame_d, text="DEPOSIT", width=18,
                  font=('Helvetica', 17, 'bold'), border=0, bg="#fdcb7f",
                  fg="white", activebackground="#fdcb7f", activeforeground="white",
                  command=self._validate).place(x=95, y=163)

    def _validate(self):
        nominal_str = self._nominal_entry.get()
        username = self._state['username']
        password = self._state['password']

        row = self._db.find_user(username, password)
        if row is None:
            return

        my_norek = int(row.get('nomor_rekening'))

        if not nominal_str.isdigit():
            AlertFrame(self._parent, "images/Frame 36 (1).png")
            return

        nominal = int(nominal_str)
        if nominal < 10000:
            AlertFrame(self._parent, "images/Frame 48.png")
            return

        angka_tf = format_currency(nominal)
        self._show_confirmation(my_norek, nominal, angka_tf)

    def _show_confirmation(self, my_norek, nominal, angka_tf):
        login_name = self._state['login_username']

        frame_k = tk.Frame(self._parent)
        frame_k.place(x=420, y=200)

        photo = ImageCache.get("images/Frame 47 (2).png", (520, 302))
        tk.Label(frame_k, image=photo).pack()

        tk.Label(frame_k, text=login_name, width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=90)
        tk.Label(frame_k, text=my_norek, width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=120)
        tk.Label(frame_k, text='Deposit', width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=150)
        tk.Label(frame_k, text=angka_tf, width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=183)

        tk.Button(frame_k, text='Batal', width=12, border=0, anchor='center',
                  font=('Helvetica', 16, 'bold'), bg="#fdcb7f", fg='black',
                  activebackground="#fdcb7f", activeforeground="black",
                  command=frame_k.destroy).place(x=80, y=240)

        tk.Button(frame_k, text='Lanjut', width=12, border=0, anchor='center',
                  font=('Helvetica', 16, 'bold'), bg="#ffa41c", fg='black',
                  activebackground="#ffa41c", activeforeground="black",
                  command=lambda: [frame_k.destroy(),
                                   self._show_pin_pad(my_norek, nominal, angka_tf)]
                  ).place(x=310, y=240)

    def _show_pin_pad(self, my_norek, nominal, angka_tf):
        pad = PinPadDialog(
            self._parent,
            on_submit=lambda pin: self._process_pin(pin, my_norek, nominal, angka_tf, pad)
        )
        pad.frame.place(x=590, y=270)

    def _process_pin(self, pin: str, my_norek, nominal, angka_tf, pad):
        pad.destroy()
        username = self._state['username']
        password = self._state['password']
        login_name = self._state['login_username']

        if len(pin) != 6:
            AlertFrame(self._parent, "images/Frame 29.png")
            return

        pin_row = self._db.find_user_by_pin(username, password, pin)
        if pin_row is None:
            AlertFrame(self._parent, "images/Frame 34.png")
            return

        # Eksekusi deposit
        new_balance = self._state['balance'] + nominal
        self._state['balance'] = new_balance
        self._db.set_balance(login_name, new_balance)
        self._db.insert_transaction(login_name, "Deposit", nominal)

        if self._state.get('click_count', 0) % 2 == 1:
            self._state['show_balance_callback']()

        no_resi = generate_resi("D")
        cur_time, cur_date = current_time_date()
        save_receipt("deposit", angka_tf, no_resi, login_name, new_balance)

        # Tutup form deposit
        if self._frame_d and self._frame_d.winfo_exists():
            self._frame_d.destroy()

        self._show_receipt(login_name, my_norek, angka_tf, cur_time, cur_date, no_resi)

    def _show_receipt(self, name, my_norek, angka_tf, cur_time, cur_date, no_resi):
        frame_r = tk.Frame(self._parent)
        frame_r.place(x=550, y=250)

        photo = ImageCache.get("images/Frame 10.png", (211, 293))
        tk.Label(frame_r, image=photo).pack()

        tk.Button(frame_r, text="X", font=('Helvetica', 10, 'bold'),
                  bg="#e4b672", fg="white", activebackground="#e4b672",
                  activeforeground="white", border=0,
                  command=frame_r.destroy).place(x=180, y=9)

        items = [
            (name, 75), (my_norek, 97), ('Deposit', 119),
            (angka_tf, 139), (f'{cur_time}, {cur_date}', 160), (no_resi, 183),
        ]
        for text, y in items:
            tk.Label(frame_r, text=text, width=18, border=0, anchor='w',
                     font=('Helvetica', 9), bg="#fdcb7f").place(x=80, y=y)
