"""
build_exe.py — Script untuk membuat file .exe Bank of Sains Data.

KEAMANAN:
    File-file sensitif (key.key, config.enc, .env) TIDAK lagi dibundel
    ke dalam .exe. User harus menyalin file-file tersebut ke:
        %APPDATA%/BankOfSainsData/

    Ini mencegah attacker mengekstrak secrets dari .exe menggunakan
    tools seperti pyinstxtractor atau uncompyle6.
"""

import os
import subprocess
import sys


def build():
    print("Memulai proses pembuatan file executable (.exe)...")

    # Pastikan PyInstaller terinstall
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller belum terinstall. Menginstall PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Argumen PyInstaller
    args = [
        "pyinstaller",
        "--noconfirm",          # Overwrite output jika sudah ada
        "--onefile",            # Satu file .exe (lebih sulit di-extract)
        "--windowed",           # Jangan tampilkan console CMD (karena ini GUI app)
        "--name=BankOfSainsData",

        # Tambahkan folder images (format: "sumber;tujuan" di Windows)
        "--add-data=images;images",

        # Icon aplikasi
        "--icon=images/BSDLogo.ico",

        # ⚠️ KEAMANAN: JANGAN bundel file-file berikut:
        #   - key.key    (encryption key)
        #   - config.enc (encrypted MongoDB connection string)
        #   - .env       (email credentials)
        #
        # File-file tersebut harus disalin ke %APPDATA%/BankOfSainsData/
        # secara terpisah (melalui installer atau manual).

        # Script utama
        "main.py"
    ]

    # Jalankan proses build
    print(f"Menjalankan: {' '.join(args)}")
    subprocess.check_call(args)

    print("\n✅ Build Selesai!")
    print("Aplikasi Anda berada di: dist/BankOfSainsData.exe")
    print()
    print("⚠️  PENTING: Sebelum menjalankan .exe, pastikan file berikut")
    print("    sudah disalin ke folder %APPDATA%/BankOfSainsData/:")
    print("    - key.key")
    print("    - config.enc")
    print("    - .env")


if __name__ == "__main__":
    build()
