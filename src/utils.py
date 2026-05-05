"""
utils.py — Fungsi utilitas umum Bank of Sains Data.
Berisi: resource_path, dekripsi, hashing, format currency, generate resi, save receipt.
"""

import os
import sys
import hashlib
import secrets
import locale
import datetime
from cryptography.fernet import Fernet
from src.config import config_path

# Folder struk transaksi
RECEIPTS_DIR = "receipts"


def resource_path(relative_path: str) -> str:
    """Mengembalikan path absolut ke resource (untuk PyInstaller compatibility)."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def decryption() -> str:
    """
    Mendekripsi string koneksi MongoDB dari file config.enc dan key.key.

    File-file ini dibaca dari folder config external (AppData saat mode .exe),
    BUKAN dari dalam bundle .exe, untuk mencegah extraction oleh attacker.
    """
    key_path = config_path('key.key')
    enc_path = config_path('config.enc')
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    with open(enc_path, 'rb') as enc_file:
        encrypted_password = enc_file.read()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password).decode()


def hash_password(input_string: str) -> str:
    """Menghash string menggunakan SHA3-256. Digunakan untuk password dan PIN."""
    return hashlib.sha3_256(input_string.encode('utf-8')).hexdigest()


def format_currency(angka: int) -> str:
    """Memformat angka ke format mata uang Indonesia (e.g. 1.500.000)."""
    locale.setlocale(locale.LC_NUMERIC, 'id_ID')
    return locale.format_string("%d", angka, grouping=True)


def generate_resi(prefix: str) -> str:
    """Membuat nomor resi unik dengan prefix tertentu (misal 'TF', 'D', 'W')."""
    random_number = secrets.randbelow(90000000) + 10000000
    return f'{prefix}-{random_number}'


def generate_card_number() -> str:
    """Membuat nomor kartu 12 digit dengan format XXXX-XXXX-XXXX."""
    rng = secrets.randbelow(900000000000) + 100000000000
    formatted = f'{rng:012}'
    return '-'.join([formatted[i:i + 4] for i in range(0, len(formatted), 4)])


def current_timestamp() -> str:
    """Mengembalikan timestamp saat ini dalam format 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def current_time_date() -> tuple[str, str]:
    """Mengembalikan tuple (waktu, tanggal) saat ini dalam format yang mudah dibaca."""
    import time
    return time.strftime('%H:%M:%S'), time.strftime('%d-%m-%y')


def save_receipt(transaction_type: str, amount: str, no_resi: str,
                 username: str, balance: int, token: str | None = None) -> None:
    """
    Simpan struk transaksi ke file teks di folder receipts/.
    Dipanggil oleh semua transaction handler.
    """
    os.makedirs(RECEIPTS_DIR, exist_ok=True)
    receipt_file = os.path.join(RECEIPTS_DIR, f"receipt_{username}.txt")
    with open(receipt_file, 'a') as f:
        f.write('\n' + "-" * 30)
        f.write(f"\nTanggal\t\t: {datetime.datetime.now()}")
        f.write(f"\nNama\t\t: {username}")
        f.write(f"\nTransaksi\t: {transaction_type}")
        f.write(f"\nNo. Resi\t: {no_resi}")
        if token:
            f.write(f"\nNomer Token\t: {token}")
        f.write(f"\nJumlah\t\t: Rp{amount}")
        f.write(f"\nSaldo Akhir\t: Rp{balance}")
        f.write('\n' + "-" * 30)
