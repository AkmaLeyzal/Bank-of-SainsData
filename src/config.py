"""
config.py — Manajemen konfigurasi aman untuk Bank of Sains Data.

Secrets (key.key, config.enc, .env) TIDAK lagi dibundel ke dalam .exe.
Sebagai gantinya, secrets disimpan di folder AppData user:
    %APPDATA%/BankOfSainsData/

Saat pertama kali menjalankan .exe, user harus menyalin file-file berikut
ke folder tersebut secara manual (atau melalui installer):
    - key.key
    - config.enc
    - .env
"""

import os
import sys

# Nama aplikasi untuk folder config
_APP_NAME = "BankOfSainsData"


def get_config_dir() -> str:
    """
    Mengembalikan path ke folder konfigurasi yang aman.

    Prioritas:
    1. Jika berjalan sebagai script biasa (development):
       → gunakan folder proyek saat ini (os.path.abspath("."))
    2. Jika berjalan sebagai .exe (PyInstaller):
       → gunakan %APPDATA%/BankOfSainsData/

    Returns:
        Path absolut ke folder konfigurasi.

    Raises:
        FileNotFoundError: Jika folder config tidak ditemukan saat mode .exe.
    """
    if getattr(sys, 'frozen', False):
        # Mode .exe — gunakan AppData
        app_data = os.getenv('APPDATA', os.path.expanduser('~'))
        config_dir = os.path.join(app_data, _APP_NAME)
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        return config_dir
    else:
        # Mode development — gunakan folder proyek
        return os.path.abspath(".")


def config_path(filename: str) -> str:
    """
    Mengembalikan path absolut ke file konfigurasi.

    Args:
        filename: Nama file (misal "key.key", "config.enc", ".env").

    Returns:
        Path absolut ke file tersebut di folder config.
    """
    return os.path.join(get_config_dir(), filename)
