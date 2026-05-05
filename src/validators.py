"""
validators.py — Validasi input ketat untuk Bank of Sains Data.

Semua input dari user divalidasi di sini sebelum masuk ke database.
Mencegah injection, data korup, dan input tidak terduga.
"""

import re

# ─── Regex Patterns ──────────────────────────────────────────────────────────

_USERNAME_RE = re.compile(r'^[a-zA-Z0-9_ ]{3,30}$')
_PIN_RE = re.compile(r'^\d{6}$')
_NOREK_RE = re.compile(r'^\d{11}$')
_PHONE_RE = re.compile(r'^\d{12,13}$')
_TOKEN_LISTRIK_RE = re.compile(r'^\d{12,13}$')
_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


# ─── Validator Functions ─────────────────────────────────────────────────────

def validate_username(username: str) -> tuple[bool, str]:
    """
    Validasi username: 3-30 karakter, hanya alphanumeric, underscore, dan spasi.

    Returns:
        (valid, pesan_error)
    """
    if not username or not username.strip():
        return False, "Username tidak boleh kosong."
    if len(username) < 3:
        return False, "Username minimal 3 karakter."
    if len(username) > 30:
        return False, "Username maksimal 30 karakter."
    if not _USERNAME_RE.match(username):
        return False, "Username hanya boleh huruf, angka, underscore, dan spasi."
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validasi password: minimal 6 karakter.

    Returns:
        (valid, pesan_error)
    """
    if not password:
        return False, "Password tidak boleh kosong."
    if len(password) < 6:
        return False, "Password minimal 6 karakter."
    if len(password) > 100:
        return False, "Password terlalu panjang."
    return True, ""


def validate_pin(pin: str) -> tuple[bool, str]:
    """
    Validasi PIN: tepat 6 digit angka.

    Returns:
        (valid, pesan_error)
    """
    if not pin:
        return False, "PIN tidak boleh kosong."
    if not _PIN_RE.match(pin):
        return False, "PIN harus 6 digit angka."
    return True, ""


def validate_norek(norek: str) -> tuple[bool, str]:
    """
    Validasi nomor rekening (NIM): tepat 11 digit angka.

    Returns:
        (valid, pesan_error)
    """
    if not norek:
        return False, "Nomor rekening tidak boleh kosong."
    if not _NOREK_RE.match(norek):
        return False, "Nomor rekening harus 11 digit angka."
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validasi format email.

    Returns:
        (valid, pesan_error)
    """
    if not email:
        return False, "Email tidak boleh kosong."
    if not _EMAIL_RE.match(email):
        return False, "Format email tidak valid."
    if len(email) > 254:
        return False, "Email terlalu panjang."
    return True, ""


def validate_nominal(nominal_str: str, min_amount: int = 10000,
                     max_amount: int = 1_000_000_000) -> tuple[bool, int, str]:
    """
    Validasi nominal transaksi: harus angka positif dalam range.

    Returns:
        (valid, nilai_int, pesan_error)
    """
    if not nominal_str:
        return False, 0, "Nominal tidak boleh kosong."
    if not nominal_str.isdigit():
        return False, 0, "Nominal harus berupa angka."

    nominal = int(nominal_str)

    if nominal < min_amount:
        return False, 0, f"Nominal minimal Rp{min_amount:,}."
    if nominal > max_amount:
        return False, 0, f"Nominal maksimal Rp{max_amount:,}."
    return True, nominal, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Validasi nomor HP: 12-13 digit angka.

    Returns:
        (valid, pesan_error)
    """
    if not phone:
        return False, "Nomor HP tidak boleh kosong."
    if not _PHONE_RE.match(phone):
        return False, "Nomor HP harus 12-13 digit angka."
    return True, ""


def validate_token_listrik(token: str) -> tuple[bool, str]:
    """
    Validasi nomor token listrik: 12-13 digit angka.

    Returns:
        (valid, pesan_error)
    """
    if not token:
        return False, "Nomor token tidak boleh kosong."
    if not _TOKEN_LISTRIK_RE.match(token):
        return False, "Nomor token harus 12-13 digit angka."
    return True, ""


def sanitize_text(text: str) -> str:
    """
    Sanitasi teks umum: strip whitespace, hapus karakter kontrol.
    Digunakan untuk input yang akan ditampilkan di UI atau disimpan ke file.
    """
    if not text:
        return ""
    # Hapus karakter kontrol (kecuali newline/tab)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return cleaned.strip()
