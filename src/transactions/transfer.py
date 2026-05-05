"""
transfer.py — Handler logika Transfer Antar Rekening.
Memisahkan business logic transfer dari UI di main_view.py.
"""

import tkinter as tk

from src.image_cache import ImageCache
from src.utils import format_currency, generate_resi, current_time_date, save_receipt
from src.widgets import PinPadDialog, AlertFrame
from src.rate_limiter import pin_limiter
from src.audit_log import log_pin_failed, log_pin_locked, log_transaction
from src.validators import validate_norek, validate_nominal


class TransferHandler:
    """
    Mengelola alur transaksi Transfer:
    1. Validasi input (norek tujuan, nominal)
    2. Tampilkan konfirmasi
    3. Tampilkan numpad PIN
    4. Eksekusi transaksi ke database
    5. Tampilkan struk
    """

    def __init__(self, parent_frame, db, app_state: dict):
        self._parent = parent_frame
        self._db = db
        self._state = app_state

    def _show_text_alert(self, message: str):
        frame = tk.Frame(self._parent, bg="#e74c3c", padx=20, pady=20)
        frame.place(x=440, y=280)
        tk.Label(frame, text=message, font=('Helvetica', 12, 'bold'),
                 bg="#e74c3c", fg="white").pack()
        tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0, width=8,
                  font=('Helvetica', 10),
                  command=frame.destroy).pack(pady=10)

    def execute(self):
        """Entry point — dipanggil saat tombol Transfer diklik."""
        norek = self._state['norek_tujuan'].get()
        nominal_str = self._state['nominalTF'].get()
        username = self._state['username']
        password = self._state['password']

        row = self._db.find_user(username, password)
        if row is None:
            return

        my_norek = row.get('nomor_rekening')
        balance = self._state['balance']

        target_row = self._db.find_user_by_norek(norek)

        # ─── Validasi ───────────────────────────────────────────────
        ok, msg = validate_norek(norek)
        if not ok:
            self._show_text_alert(msg); return
            
        if target_row is None or norek == my_norek:
            if norek == my_norek:
                AlertFrame(self._parent, "images/Frame 76 (1).png")
            else:
                AlertFrame(self._parent, "images/Frame 22.png")
            return

        ok, nominal, msg = validate_nominal(nominal_str, min_amount=10000)
        if not ok:
            self._show_text_alert(msg); return

        if balance < nominal:
            AlertFrame(self._parent, "images/Frame 37.png")
            return
        if balance - nominal < 20000:
            AlertFrame(self._parent, "images/Frame 49.png")
            return

        # ─── Konfirmasi ──────────────────────────────────────────────
        self._show_confirmation(my_norek, norek, nominal, balance)

    # ─── Private helpers ──────────────────────────────────────────────────

    def _show_confirmation(self, my_norek, norek_tujuan, nominal, balance):
        frame_k = tk.Frame(self._parent)
        frame_k.place(x=420, y=200)

        photo = ImageCache.get("images/Frame 47 (2).png", (520, 302))
        tk.Label(frame_k, image=photo).pack()

        angka_tf = format_currency(nominal)
        login_name = self._state['login_username']

        tk.Label(frame_k, text=login_name, width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=90)
        tk.Label(frame_k, text=my_norek, width=24, border=0, anchor='w',
                 font=('Helvetica', 18, 'bold'), bg="white").place(x=140, y=120)
        tk.Label(frame_k, text=f'TF To {norek_tujuan}', width=24, border=0, anchor='w',
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
                                   self._show_pin_pad(my_norek, norek_tujuan, nominal, angka_tf)]
                  ).place(x=310, y=240)

    def _show_pin_pad(self, my_norek, norek_tujuan, nominal, angka_tf):
        pad = PinPadDialog(
            self._parent,
            on_submit=lambda pin: self._process_pin(
                pin, my_norek, norek_tujuan, nominal, angka_tf, pad
            )
        )
        pad.frame.place(x=590, y=270)

    def _process_pin(self, pin: str, my_norek, norek_tujuan, nominal, angka_tf, pad):
        pad.destroy()
        username = self._state['username']
        password = self._state['password']
        login_name = self._state['login_username']

        # Rate limiting PIN — cegah brute-force
        if not pin_limiter.is_allowed(username):
            remaining = pin_limiter.remaining_lockout(username)
            frame = tk.Frame(self._parent)
            frame.place(x=500, y=300)
            tk.Label(frame, text=f"PIN terkunci!\nCoba lagi dalam {remaining} detik.",
                     font=('Helvetica', 14, 'bold'),
                     bg="#e74c3c", fg="white", padx=20, pady=15).pack()
            tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0,
                      width=8, command=frame.destroy).pack(pady=5)
            log_pin_locked(username, pin_limiter.remaining_lockout(username))
            return

        if len(pin) != 6:
            AlertFrame(self._parent, "images/Frame 29.png")
            return

        pin_row = self._db.find_user_by_pin(username, password, pin)
        if pin_row is None:
            pin_limiter.record_failure(username)
            log_pin_failed(username, "transfer")
            AlertFrame(self._parent, "images/Frame 34.png")
            return

        pin_limiter.reset(username)

        # Eksekusi transfer
        new_balance = self._state['balance'] - nominal
        self._state['balance'] = new_balance
        self._db.set_balance(login_name, new_balance)
        self._db.increment_balance(norek_tujuan, nominal)
        self._db.insert_transaction(login_name, "Transfer", nominal)
        log_transaction(login_name, "Transfer", nominal, norek_tujuan=norek_tujuan)

        # Refresh saldo jika tampil
        if self._state.get('click_count', 0) % 2 == 1:
            self._state['show_balance_callback']()

        # Resi
        no_resi = generate_resi("TF")
        cur_time, cur_date = current_time_date()
        save_receipt("transfer", angka_tf, no_resi, login_name, new_balance)

        # Struk on-screen
        self._show_receipt(login_name, my_norek, norek_tujuan, angka_tf,
                           cur_time, cur_date, no_resi)

    def _show_receipt(self, name, my_norek, norek_tujuan, angka_tf,
                      cur_time, cur_date, no_resi):
        frame_r = tk.Frame(self._parent)
        frame_r.place(x=550, y=250)

        photo = ImageCache.get("images/Frame 10.png", (211, 293))
        tk.Label(frame_r, image=photo).pack()

        tk.Button(frame_r, text="X", font=('Helvetica', 10, 'bold'),
                  bg="#e4b672", fg="white", activebackground="#e4b672",
                  activeforeground="white", border=0,
                  command=frame_r.destroy).place(x=180, y=9)

        items = [
            (name, 75), (my_norek, 97), (f'TF To {norek_tujuan}', 119),
            (angka_tf, 139), (f'{cur_time}, {cur_date}', 160), (no_resi, 183),
        ]
        for text, y in items:
            tk.Label(frame_r, text=text, width=18, border=0, anchor='w',
                     font=('Helvetica', 9), bg="#fdcb7f").place(x=80, y=y)
