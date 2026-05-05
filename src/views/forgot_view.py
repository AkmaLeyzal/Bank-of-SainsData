"""
forgot_view.py — Tampilan layar Lupa Password.
Responsif: semua koordinat & font diskala otomatis via Layout.
"""

import threading
import tkinter as tk
from tkinter import Toplevel

from src.utils import hash_password
from src.widgets import PlaceholderEntry, AlertFrame
from src.image_cache import ImageCache
from src.layout import Layout
from src.email_service import generate_otp, send_otp_email
from src.audit_log import log_password_reset
from src.validators import validate_username, validate_password, validate_pin, validate_norek


class ForgotPasswordView:
    def __init__(self, parent: tk.Tk, db):
        self._parent = parent
        self._db = db

        self._window = Toplevel(parent)
        self._window.title('BSD — Lupa Password')
        self._window.attributes('-fullscreen', True)
        self._window.configure(bg="#333333")

        self._L = Layout(self._window)
        self._lanjut_btn = None
        self._build_ui()
        self._window.mainloop()

    def _build_ui(self):
        L = self._L
        sw, sh = L.screen_w, L.screen_h

        photo = ImageCache.get("images/Frame 58.png", (sw, sh))
        tk.Label(self._window, image=photo).place(x=0, y=0)

        entry_cfg = dict(font=('Helvetica', L.font(20)), fg="black",
                         bg="#ffffff", border=0, width=17)

        self._entry_username = PlaceholderEntry(
            self._window, placeholder="Username", **entry_cfg)
        L.place(self._entry_username, 490, 255)

        self._entry_norek = PlaceholderEntry(
            self._window, placeholder="NIM", **entry_cfg)
        L.place(self._entry_norek, 490, 307)

        self._entry_password = PlaceholderEntry(
            self._window, placeholder="Password Baru", is_password=True, **entry_cfg)
        L.place(self._entry_password, 490, 357)

        self._entry_pin = PlaceholderEntry(
            self._window, placeholder="PIN Baru", is_password=True, **entry_cfg)
        L.place(self._entry_pin, 490, 407)

        self._lanjut_btn = tk.Button(
            self._window, text='Lanjutkan', font=("Helvetica", L.font(18)),
            command=self._on_lanjut, fg="black", bg="#FDCB7F", width=23,
            border=0, activebackground="#FDCB7F", cursor="hand2")
        L.place(self._lanjut_btn, 473, 469)

        tk.Button(self._window, text='Keluar', font=("Helvetica", L.font(18)),
                  command=self._go_back, fg="black", bg="#FDCB7F", width=23,
                  border=0, activebackground="#FDCB7F", cursor="hand2"
                  ).place(x=L.x(473), y=L.y(532))

    def _go_back(self):
        self._window.destroy()
        self._parent.deiconify()

    def _on_lanjut(self):
        username     = self._entry_username.get_value()
        norek        = self._entry_norek.get_value()
        password_raw = self._entry_password.get_value()
        pin          = self._entry_pin.get_value()

        ok, msg = validate_username(username)
        if not ok: self._show_text_alert(msg); return
        ok, msg = validate_norek(norek)
        if not ok: self._show_text_alert(msg); return
        ok, msg = validate_password(password_raw)
        if not ok: self._show_text_alert(msg); return
        ok, msg = validate_pin(pin)
        if not ok: self._show_text_alert(msg); return

        row = self._db.find_user_for_reset(username, norek)
        if row is None:
            self._show_text_alert("Username atau Norek tidak valid."); return

        new_password = hash_password(password_raw)

        self._show_otp_confirm(username, new_password, pin, row.get("email"))

    def _alert(self, path: str):
        L = self._L
        frame = tk.Frame(self._window)
        # Posisi asli: frame_9.place(x=520, y=270)
        frame.place(x=L.x(520), y=L.y(270))
        photo = ImageCache.get(path, L.img(219, 227))
        tk.Label(frame, image=photo).pack()
        tk.Button(frame, text="x", fg="#ffffff", bg="#FDCB7F", border=0,
                  cursor="hand2", width=3, command=frame.destroy
                  ).place(x=L.px(175), y=L.py(7))

    def _show_text_alert(self, message: str):
        L = self._L
        frame = tk.Frame(self._window, bg="#e74c3c", padx=20, pady=20)
        frame.place(x=L.x(440), y=L.y(280))
        tk.Label(frame, text=message, font=('Helvetica', L.font(12), 'bold'),
                 bg="#e74c3c", fg="white").pack()
        tk.Button(frame, text="OK", bg="#c0392b", fg="white", border=0, width=8,
                  font=('Helvetica', L.font(10)),
                  command=frame.destroy).pack(pady=10)

    def _show_otp_confirm(self, username, new_password, pin, email_tujuan):
        L = self._L
        frame_check = tk.Frame(self._window)
        # Posisi asli: frame_check.place(x=470, y=270)
        frame_check.place(x=L.x(470), y=L.y(270))
        photo = ImageCache.get("images/Frame 59 (1).png", L.img(355, 139))
        tk.Label(frame_check, image=photo).pack()

        tk.Button(frame_check, text="X", font=('Helvetica', L.font(10), 'bold'),
                  bg="#fdcb7f", fg="white", border=0,
                  command=frame_check.destroy
                  ).place(x=L.px(340), y=L.py(8))

        tk.Button(frame_check, text="Lanjutkan", font=('Helvetica', L.font(14), 'bold'),
                  bg="#ffa41c", fg='black', border=0, width=10,
                  command=lambda: [frame_check.destroy(),
                                   self._send_otp_async(username, new_password, pin, email_tujuan)]
                  ).place(x=L.px(120), y=L.py(78))

    def _send_otp_async(self, username, new_password, pin, email_tujuan):
        L = self._L
        if not email_tujuan or "@gmail.com" not in email_tujuan:
            self._alert("images/Frame 66.png"); return

        otp_code = generate_otp()

        loading_frame = tk.Frame(self._window, bg="#FDCB7F", padx=20, pady=12)
        # Loading di tengah vertikal layar
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
        self._lanjut_btn.config(state=tk.DISABLED, text="Mengirim...")

        def run():
            success = send_otp_email(email_tujuan, username, otp_code)
            self._window.after(0, lambda: self._on_email_done(
                success, otp_code, username, new_password, pin, loading_frame))

        threading.Thread(target=run, daemon=True).start()

    def _on_email_done(self, success, otp_code, username, new_password, pin, loading_frame):
        if loading_frame.winfo_exists():
            loading_frame.destroy()
        self._lanjut_btn.config(state=tk.NORMAL, text="Lanjutkan")
        if success:
            self._show_otp_numpad(username, new_password, pin, otp_code)
        else:
            self._alert("images/Frame 66.png")

    def _show_otp_numpad(self, username, new_password, pin, otp_code):
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
                  command=lambda: self._verify_otp(
                      otp_var.get(), otp_code, username, new_password, pin, frame_otp
                  )).place(x=L.px(140), y=L.py(240))

    def _verify_otp(self, entered_otp, correct_otp, username, new_password, new_pin, frame_otp):
        if entered_otp == correct_otp:
            self._db.update_password_pin(username, new_password, new_pin)
            log_password_reset(username)
            frame_otp.destroy()
            self._window.destroy()
            self._parent.deiconify()
        else:
            self._alert("images/Frame 62.png")
