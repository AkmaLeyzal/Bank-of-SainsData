"""
login_view.py — Tampilan Layar Login Bank of Sains Data.
Responsif: semua koordinat & font diskala otomatis via Layout.
"""

import tkinter as tk

from src.utils import hash_password
from src.widgets import PlaceholderEntry
from src.image_cache import ImageCache
from src.layout import Layout


class LoginView:
    """Mengelola UI dan logika layar Login."""

    def __init__(self, root: tk.Tk, db):
        self._root = root
        self._db = db

        self._root.title('Bank of Sains Data')
        self._root.attributes('-fullscreen', True)
        self._root.configure(bg='#333333')

        self._L = Layout(self._root)
        self._build_ui()

    def _build_ui(self):
        L = self._L
        sw, sh = L.screen_w, L.screen_h

        # Background — diskala ke ukuran layar penuh
        photo = ImageCache.get("images/Frame 25 (2).png", (sw, sh))
        tk.Label(self._root, image=photo).place(x=0, y=0)

        # ─ Entry fields ─────────────────────────────────────────────────────
        entry_cfg = dict(
            font=('Helvetica', L.font(20)), fg="black", bg="#ffffff",
            border=0, width=17
        )
        self._username_entry = PlaceholderEntry(
            self._root, placeholder="Username", **entry_cfg)
        L.place(self._username_entry, 490, 252)

        self._password_entry = PlaceholderEntry(
            self._root, placeholder="Password", is_password=True, **entry_cfg)
        L.place(self._password_entry, 490, 303)

        # ─ Buttons ──────────────────────────────────────────────────────────
        tk.Button(self._root, text='MASUK', font=("Helvetica", L.font(18)),
                  command=self._on_login, fg="#ffffff", bg="#FDCB7F",
                  width=23, border=0, activebackground="#FDCB7F",
                  activeforeground="#ffffff", cursor="hand2"
                  ).place(x=L.x(480), y=L.y(370))

        tk.Button(self._root, text='DAFTAR', font=("Helvetica", L.font(18)),
                  command=self._on_signup, bg="#FDCB7F", fg="#ffffff",
                  cursor="hand2", border=0, width=23,
                  activebackground="#FDCB7F", activeforeground="#ffffff"
                  ).place(x=L.x(480), y=L.y(475))

        # Lupa password
        tk.Button(self._root, text='Klik', font=("Helvetica", L.font(10)),
                  command=self._on_forgot, fg="black", bg="#FDCB7F",
                  width=8, border=0, activebackground="#FDCB7F",
                  activeforeground="black", cursor="hand2"
                  ).place(x=L.x(740), y=L.y(535))

        # QUIT
        tk.Button(self._root, text='QUIT', font=("Helvetica", L.font(15)),
                  command=self._on_quit, fg="#ffffff", bg="#E4B672",
                  border=0, activebackground="#E4B672",
                  activeforeground="#ffffff", cursor="hand2", width=11
                  ).place(x=L.x(1140), y=L.y(13))

    # ─── Event Handlers ──────────────────────────────────────────────────────

    def _on_login(self):
        username = self._username_entry.get_value()
        password_raw = self._password_entry.get_value()
        if not username or not password_raw:
            return
        password = hash_password(password_raw)
        row = self._db.find_user(username, password)
        if row is not None:
            self._root.iconify()
            from src.views.main_view import MainView
            MainView(self._root, self._db, username=username,
                     password=password, user_data=row)
        else:
            self._show_alert("images/Frame 45.png")

    def _on_signup(self):
        from src.views.signup_view import SignupView
        SignupView(self._root, self._db)

    def _on_forgot(self):
        from src.views.forgot_view import ForgotPasswordView
        ForgotPasswordView(self._root, self._db)

    def _on_quit(self):
        L = self._L
        frame_quit = tk.Frame(self._root)
        # Posisi asli: frame_quit.place(x=380, y=270)
        frame_quit.place(x=L.x(380), y=L.y(270))

        photo = ImageCache.get("images/Frame 52.png", L.img(520, 226))
        tk.Label(frame_quit, image=photo).pack()

        def quit_confirmed():
            self._db.close()
            self._root.destroy()

        # Iya: (297, 140), Tidak: (75, 140) — koordinat asli
        tk.Button(frame_quit, text="Iya", font=('Helvetica', L.font(18), 'bold'),
                  fg="black", bg="#ffa41c", border=0, cursor="hand2", width=10,
                  command=quit_confirmed).place(x=L.px(297), y=L.py(140))

        tk.Button(frame_quit, text="Tidak", font=('Helvetica', L.font(18), 'bold'),
                  fg="black", bg="#FDCB7F", border=0, cursor="hand2", width=10,
                  command=frame_quit.destroy).place(x=L.px(75), y=L.py(140))

    def _show_alert(self, image_path: str):
        L = self._L
        frame = tk.Frame(self._root)
        # Posisi asli: frame_9.place(x=520, y=270)
        frame.place(x=L.x(520), y=L.y(270))

        photo = ImageCache.get(image_path, L.img(219, 227))
        tk.Label(frame, image=photo).pack()

        tk.Button(frame, text="x", fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=3,
                  command=frame.destroy).place(x=L.px(175), y=L.py(7))
