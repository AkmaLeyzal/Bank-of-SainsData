"""
database.py — Lapisan akses data MongoDB untuk Bank of Sains Data.
Seluruh query ke MongoDB dipusatkan di sini sehingga UI tidak perlu
mengetahui detail implementasi database.
"""

import pymongo
from bson import ObjectId
from pymongo import MongoClient

from src.utils import decryption, current_timestamp, hash_password


class Database:
    """
    Mengelola koneksi dan semua operasi ke MongoDB Atlas.
    Instansiasi sekali di `main.py` dan dioper ke seluruh view & handler.
    """

    def __init__(self):
        conn_str = decryption()
        self.client = MongoClient(
            conn_str,
            serverSelectionTimeoutMS=5000,
            tls=True,                          # Enforce TLS (anti-MITM)
            tlsAllowInvalidCertificates=False,  # Tolak sertifikat tidak valid
        )
        # Test koneksi — gagal cepat jika tidak ada internet
        self.client.admin.command('ping')
        db = self.client['Bank_Sains_Data']
        self._users = db['database_client_BSD']
        self._history = db['transaction_history']

    # ─── User Operations ────────────────────────────────────────────────────

    def find_user(self, username: str, password: str) -> dict | None:
        """Mencari user berdasarkan username dan password (sudah di-hash)."""
        return self._users.find_one({'username': username, 'password': password})

    def find_user_by_username(self, username: str) -> dict | None:
        """Mencari user hanya berdasarkan username."""
        return self._users.find_one({'username': username})

    def find_user_by_norek(self, norek: str) -> dict | None:
        """Mencari user berdasarkan nomor rekening."""
        return self._users.find_one({'nomor_rekening': norek})

    def find_user_by_pin(self, username: str, password: str, pin: str) -> dict | None:
        """Verifikasi PIN user. PIN di-hash sebelum dicocokkan."""
        hashed_pin = hash_password(pin)
        return self._users.find_one({
            'pin': hashed_pin, 'username': username, 'password': password
        })

    def find_user_for_reset(self, username: str, norek: str) -> dict | None:
        """Mencari user berdasarkan username + nomor rekening (untuk reset password)."""
        return self._users.find_one({'username': username, 'nomor_rekening': norek})

    def create_user(self, username: str, password: str, balance: int, pin: str,
                    norek: str, nomor_kartu: str, email: str) -> None:
        """Membuat akun user baru. PIN di-hash sebelum disimpan."""
        hashed_pin = hash_password(pin)
        self._users.insert_one({
            'username': username,
            'password': password,
            'balance': balance,
            'pin': hashed_pin,
            'nomor_rekening': norek,
            'nomor_kartu': nomor_kartu,
            'email': email,
        })

    def update_password_pin(self, username: str, new_password: str, new_pin: str) -> None:
        """Mengupdate password dan PIN user (untuk fitur lupa password). PIN di-hash."""
        hashed_pin = hash_password(new_pin)
        self._users.update_one(
            {'username': username},
            {'$set': {'password': new_password, 'pin': hashed_pin}}
        )

    def set_balance(self, username: str, new_balance: int) -> None:
        """Menyetel saldo user ke nilai tertentu."""
        self._users.update_one(
            {'username': username},
            {'$set': {'balance': new_balance}}
        )

    def increment_balance(self, norek: str, amount: int) -> None:
        """Menambahkan saldo ke akun berdasarkan nomor rekening (untuk penerima transfer)."""
        self._users.update_one(
            {'nomor_rekening': norek},
            {'$inc': {'balance': amount}}
        )

    def atomic_deduct_balance(self, username: str, amount: int) -> bool:
        """
        Mengurangi saldo secara atomik. Hanya berhasil jika saldo cukup.
        Mencegah race condition pada operasi balance.

        Returns:
            True jika berhasil (saldo cukup), False jika gagal.
        """
        result = self._users.update_one(
            {'username': username, 'balance': {'$gte': amount}},
            {'$inc': {'balance': -amount}}
        )
        return result.modified_count > 0

    # ─── Transaction History Operations ─────────────────────────────────────

    def get_history(self, username: str, limit: int = 50):
        """Mengambil riwayat transaksi user, urut dari terlama, dibatasi limit."""
        return (self._history
                .find({'username': username})
                .sort([('_id', pymongo.ASCENDING)])
                .limit(limit))

    def insert_transaction(self, username: str, transaction_type: str, nominal: int) -> None:
        """Menyimpan satu entri riwayat transaksi."""
        self._history.insert_one({
            '_id': ObjectId(),
            'username': username,
            'transaction_type': transaction_type,
            'nominal_transaction': nominal,
            'time_transaction': current_timestamp(),
        })

    # ─── Lifecycle ───────────────────────────────────────────────────────────

    def close(self) -> None:
        """Menutup koneksi MongoDB. Panggil saat aplikasi ditutup."""
        self.client.close()
