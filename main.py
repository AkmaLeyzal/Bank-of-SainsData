import os
import sys
import tkinter as tk
from tkinter import messagebox

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    try:
        from src.database import Database
        db = Database()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Koneksi Gagal",
            "Tidak dapat terhubung ke database.\n"
            "Pastikan koneksi internet tersedia.\n\n"
            f"Detail: {e}"
        )
        root.destroy()
        sys.exit(1)

    root = tk.Tk()

    from src.image_cache import ImageCache, COMMON_IMAGES
    ImageCache.preload(COMMON_IMAGES)

    from src.views.login_view import LoginView
    LoginView(root, db)

    try:
        root.mainloop()
    finally:
        db.close()


if __name__ == '__main__':
    main()
