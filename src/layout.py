"""
layout.py — Sistem scaling koordinat responsif untuk Bank of Sains Data.

Masalah:
    Semua koordinat hardcoded untuk resolusi 1280×720.
    Di layar 1366×768, 1920×1080, atau 1440×900, UI akan tampak salah posisi.

Solusi:
    Layout menghitung faktor skala relatif terhadap resolusi desain (1280×720).
    Semua view memanggil lx(), ly(), font(), img() alih-alih nilai mentah.

Penggunaan:
    # Di konstruktor view:
    L = Layout(root_or_window)

    # Koordinat:
    widget.place(x=L.x(490), y=L.y(255))

    # Font:
    font=('Helvetica', L.font(20))

    # Gambar:
    ImageCache.get("images/bg.png", L.img(1280, 720))

    # Popup tengah layar:
    L.center(frame, 355, 139)   # frame berukuran 355×139 dalam desain space
"""

import tkinter as tk


class Layout:
    """
    Kalkulator skala otomatis berdasarkan resolusi layar aktual.

    Resolusi desain: 1280 × 720 (16:9)
    Semua nilai x/y dalam kode didasarkan pada resolusi ini.
    """

    BASE_W: int = 1280
    BASE_H: int = 720

    def __init__(self, widget: tk.Misc):
        """
        Args:
            widget: Widget tkinter mana saja (root, Toplevel, Frame).
                    Digunakan untuk mendapatkan dimensi layar aktual.
        """
        # Update idle tasks dulu agar winfo_screenwidth sudah akurat
        widget.update_idletasks()
        self.screen_w: int = widget.winfo_screenwidth()
        self.screen_h: int = widget.winfo_screenheight()

        self._sx: float = self.screen_w / self.BASE_W
        self._sy: float = self.screen_h / self.BASE_H
        # Skala seragam untuk font (ambil minimum agar tidak terpotong)
        self._sf: float = min(self._sx, self._sy)

    # ─── Skala Koordinat ─────────────────────────────────────────────────────

    def x(self, val: int | float) -> int:
        """Skala posisi horizontal."""
        return int(val * self._sx)

    def y(self, val: int | float) -> int:
        """Skala posisi vertikal."""
        return int(val * self._sy)

    def px(self, val: int | float) -> int:
        """Skala lebar dalam piksel (untuk gambar)."""
        return int(val * self._sx)

    def py(self, val: int | float) -> int:
        """Skala tinggi dalam piksel (untuk gambar)."""
        return int(val * self._sy)

    def img(self, w: int, h: int) -> tuple[int, int]:
        """Mengembalikan ukuran gambar yang sudah diskala sebagai tuple (w, h)."""
        return (self.px(w), self.py(h))

    # ─── Skala Font ──────────────────────────────────────────────────────────

    def font(self, size: int) -> int:
        """Skala ukuran font, minimum 8pt."""
        return max(8, int(size * self._sf))

    # ─── Helper Place ─────────────────────────────────────────────────────────

    def place(self, widget: tk.Widget, x: int, y: int, **kwargs):
        """Shortcut: place widget dengan koordinat yang sudah diskala."""
        widget.place(x=self.x(x), y=self.y(y), **kwargs)

    def center(self, widget: tk.Widget, design_w: int, design_h: int,
                cx: int = 640, cy: int = 360):
        """
        Tempatkan widget di tengah layar (atau di sekitar titik cx, cy dalam
        koordinat desain).

        Args:
            widget:   Widget yang akan ditempatkan.
            design_w: Lebar widget dalam koordinat desain (1280-base).
            design_h: Tinggi widget dalam koordinat desain.
            cx, cy:   Titik tengah target dalam koordinat desain.
        """
        x = self.x(cx) - self.px(design_w) // 2
        y = self.y(cy) - self.py(design_h) // 2
        widget.place(x=x, y=y)

    # ─── Info ─────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (f"Layout({self.screen_w}×{self.screen_h}, "
                f"sx={self._sx:.3f}, sy={self._sy:.3f}, sf={self._sf:.3f})")
