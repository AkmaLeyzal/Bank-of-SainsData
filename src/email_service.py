"""
email_service.py — Layanan pengiriman OTP via Gmail SMTP.
Dipisahkan dari UI agar tidak memblokir thread utama Tkinter.

KEAMANAN:
    - Kredensial dibaca dari .env di folder config external (AppData),
      BUKAN dibundel ke dalam .exe.
    - Tidak ada fallback hardcoded — warning jelas jika .env tidak ditemukan.
    - OTP dihasilkan menggunakan CSPRNG (secrets module).
"""

import os
import secrets
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from src.config import config_path

# Load .env dari folder config external
load_dotenv(dotenv_path=config_path('.env'))

_SENDER_EMAIL = os.getenv("EMAIL_SENDER")
_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not _SENDER_EMAIL or not _APP_PASSWORD:
    import warnings
    warnings.warn(
        "EMAIL_SENDER dan/atau EMAIL_APP_PASSWORD tidak ditemukan di .env. "
        "Fitur pengiriman OTP tidak akan berfungsi. "
        f"Pastikan file .env ada di: {config_path('.env')}",
        RuntimeWarning, stacklevel=2
    )


def generate_otp() -> str:
    """Membuat kode OTP 6 digit sebagai string (menggunakan CSPRNG)."""
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(recipient_email: str, recipient_name: str, otp_code: str) -> bool:
    """
    Mengirim email OTP ke penerima.

    Args:
        recipient_email: Alamat email tujuan (harus berakhiran @gmail.com).
        recipient_name:  Nama penerima untuk sapaan di email.
        otp_code:        Kode OTP 6 digit yang akan dikirim.

    Returns:
        True jika berhasil, False jika gagal atau email tidak valid.
    """
    if not _SENDER_EMAIL or not _APP_PASSWORD:
        return False

    if not recipient_email or "@gmail.com" not in recipient_email:
        return False

    subject = "Konfirmasi Kode OTP untuk Akses Akun Anda"
    body = (
        f" Dear {recipient_name}\n\n"
        f"Kami ingin mengkonfirmasi bahwa Anda telah meminta untuk menerima kode OTP "
        f"untuk mengakses akun Anda. Berikut adalah detail kode OTP 6 digit PIN yang "
        f"dapat Anda gunakan:\n\n"
        f"Kode OTP: {otp_code}\n\n"
        f"Salam Hangat dari Admin Bank Sains Data.\n\nTerima kasih."
    )

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = _SENDER_EMAIL
    message["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(_SENDER_EMAIL, _APP_PASSWORD)
            server.sendmail(_SENDER_EMAIL, [recipient_email], message.as_string())
        return True
    except Exception:
        return False
