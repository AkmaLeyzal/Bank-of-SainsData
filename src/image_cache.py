"""
image_cache.py — Cache gambar global untuk Bank of Sains Data.

Tanpa cache: setiap buka popup → Image.open() + resize() dari disk (~10-50ms/gambar).
Dengan cache: akses pertama dari disk, selanjutnya dari RAM (< 1ms).

Catatan penting:
    ImageTk.PhotoImage HARUS dibuat di main thread (tkinter requirement).
    Cache ini aman karena seluruh UI berjalan di main thread.
    Referensi disimpan di dict sehingga tidak di-garbage-collect oleh Python.
"""

from __future__ import annotations
from PIL import Image, ImageTk
from src.utils import resource_path


class ImageCache:
    """
    Singleton cache untuk ImageTk.PhotoImage.

    Penggunaan:
        from src.image_cache import ImageCache
        photo = ImageCache.get("images/Frame 9.png", (211, 293))
        label = tk.Label(frame, image=photo)
        # Tidak perlu menyimpan referensi photo secara manual!
    """

    _cache: dict[tuple[str, tuple[int, int]], ImageTk.PhotoImage] = {}

    @classmethod
    def get(cls, path: str, size: tuple[int, int]) -> ImageTk.PhotoImage:
        """
        Ambil ImageTk.PhotoImage dari cache.
        Jika belum di-cache, load dari disk dan simpan.

        Args:
            path: Path relatif ke file gambar (misal "images/Frame 9.png").
            size: Tuple (width, height) untuk resize.

        Returns:
            ImageTk.PhotoImage yang sudah di-cache.
        """
        key = (path, size)
        if key not in cls._cache:
            abs_path = resource_path(path)
            img = Image.open(abs_path).resize(size, Image.LANCZOS)
            cls._cache[key] = ImageTk.PhotoImage(img)
        return cls._cache[key]

    @classmethod
    def preload(cls, items: list[tuple[str, tuple[int, int]]]) -> None:
        """
        Pre-load sekumpulan gambar ke cache sekaligus (opsional).
        Bisa dipanggil saat startup untuk mempercepat pembukaan popup pertama.

        Args:
            items: List of (path, size) tuples.
        """
        for path, size in items:
            cls.get(path, size)

    @classmethod
    def clear(cls) -> None:
        """Hapus seluruh cache (gunakan dengan hati-hati, hanya untuk testing)."""
        cls._cache.clear()

    @classmethod
    def size(cls) -> int:
        """Jumlah gambar yang tersimpan di cache."""
        return len(cls._cache)


# ─── Gambar-gambar yang sering dipakai (preload kandidat) ───────────────────
COMMON_IMAGES = [
    # Alert/notification frames
    ("images/Frame 9.png",      (211, 293)),   # PinPad background
    ("images/Frame 10.png",     (211, 293)),   # Struk transaksi
    ("images/Frame 42.png",     (320, 80)),    # History item
    ("images/Frame 47 (2).png", (520, 302)),   # Konfirmasi transaksi
    ("images/Frame 59 (1).png", (355, 139)),   # Dialog konfirmasi OTP
    ("images/Frame 60 (2).png", (211, 293)),   # Numpad OTP
]
