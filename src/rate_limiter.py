"""
rate_limiter.py — Pembatasan percobaan login & PIN untuk Bank of Sains Data.

Mencegah brute-force attack dengan mengunci akun setelah beberapa percobaan
gagal dalam jangka waktu tertentu.
"""

import time
from collections import defaultdict


class RateLimiter:
    """
    Rate limiter berbasis sliding window.

    Setiap key (misal username) memiliki daftar timestamp percobaan gagal.
    Jika jumlah percobaan dalam window melebihi max_attempts, key tersebut
    dikunci sampai percobaan tertua keluar dari window.

    Penggunaan:
        limiter = RateLimiter(max_attempts=5, lockout_seconds=300)

        if not limiter.is_allowed("user123"):
            remaining = limiter.remaining_lockout("user123")
            print(f"Akun terkunci. Coba lagi dalam {remaining} detik.")
            return

        # ... coba login ...
        if login_gagal:
            limiter.record_failure("user123")
        else:
            limiter.reset("user123")
    """

    def __init__(self, max_attempts: int = 5, lockout_seconds: int = 300):
        """
        Args:
            max_attempts:    Jumlah maksimal percobaan gagal sebelum dikunci.
            lockout_seconds: Durasi window dalam detik (default 5 menit).
        """
        self._attempts: dict[str, list[float]] = defaultdict(list)
        self._max = max_attempts
        self._lockout = lockout_seconds

    def _cleanup(self, key: str) -> None:
        """Hapus percobaan yang sudah di luar window."""
        now = time.time()
        self._attempts[key] = [
            t for t in self._attempts[key]
            if now - t < self._lockout
        ]

    def is_allowed(self, key: str) -> bool:
        """
        Cek apakah key masih boleh mencoba.

        Returns:
            True jika masih boleh, False jika terkunci.
        """
        self._cleanup(key)
        return len(self._attempts[key]) < self._max

    def record_failure(self, key: str) -> None:
        """Catat satu percobaan gagal untuk key."""
        self._cleanup(key)
        self._attempts[key].append(time.time())

    def reset(self, key: str) -> None:
        """Reset semua percobaan gagal untuk key (setelah login berhasil)."""
        self._attempts.pop(key, None)

    def remaining_lockout(self, key: str) -> int:
        """
        Berapa detik lagi sampai key bisa mencoba kembali.

        Returns:
            Sisa detik lockout, atau 0 jika tidak terkunci.
        """
        self._cleanup(key)
        if len(self._attempts[key]) < self._max:
            return 0
        oldest = min(self._attempts[key])
        remaining = self._lockout - (time.time() - oldest)
        return max(0, int(remaining))

    def attempts_left(self, key: str) -> int:
        """
        Berapa percobaan tersisa sebelum terkunci.

        Returns:
            Jumlah percobaan yang tersisa.
        """
        self._cleanup(key)
        return max(0, self._max - len(self._attempts[key]))


# ─── Global instances ────────────────────────────────────────────────────────
# Dipakai oleh login_view dan transaction handlers
login_limiter = RateLimiter(max_attempts=5, lockout_seconds=300)
pin_limiter = RateLimiter(max_attempts=3, lockout_seconds=600)
