"""
audit_log.py — Sistem audit logging untuk Bank of Sains Data.

Mencatat semua aktivitas penting (login, transaksi, kegagalan keamanan)
ke file log untuk keperluan audit dan forensik.

Log disimpan di:
    - Development: ./logs/bsd_audit.log
    - .exe mode:   %APPDATA%/BankOfSainsData/logs/bsd_audit.log
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from src.config import get_config_dir


def _setup_logger() -> logging.Logger:
    """
    Konfigurasi logger dengan:
    - RotatingFileHandler (max 5MB per file, 3 backup)
    - Format: timestamp - level - message
    """
    log_dir = os.path.join(get_config_dir(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'bsd_audit.log')

    logger = logging.getLogger('bsd_audit')
    logger.setLevel(logging.INFO)

    # Cegah duplicate handlers jika module di-import berkali-kali
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Global logger instance
_logger = _setup_logger()


# ─── Public API ──────────────────────────────────────────────────────────────

def log_login_success(username: str) -> None:
    """Catat login berhasil."""
    _logger.info(f"LOGIN_OK | user={username}")


def log_login_failed(username: str, reason: str = "wrong_credentials") -> None:
    """Catat percobaan login gagal."""
    _logger.warning(f"LOGIN_FAIL | user={username} | reason={reason}")


def log_account_locked(username: str, duration_sec: int) -> None:
    """Catat akun terkunci karena terlalu banyak percobaan."""
    _logger.critical(f"ACCOUNT_LOCKED | user={username} | duration={duration_sec}s")


def log_pin_failed(username: str, context: str = "transaction") -> None:
    """Catat percobaan PIN gagal."""
    _logger.warning(f"PIN_FAIL | user={username} | context={context}")


def log_pin_locked(username: str, duration_sec: int) -> None:
    """Catat PIN terkunci."""
    _logger.critical(f"PIN_LOCKED | user={username} | duration={duration_sec}s")


def log_transaction(username: str, tx_type: str, nominal: int,
                    norek_tujuan: str | None = None) -> None:
    """Catat transaksi berhasil."""
    extra = f" | to={norek_tujuan}" if norek_tujuan else ""
    _logger.info(f"TX_OK | user={username} | type={tx_type} | nominal={nominal}{extra}")


def log_signup(username: str, norek: str) -> None:
    """Catat pendaftaran akun baru."""
    _logger.info(f"SIGNUP | user={username} | norek={norek}")


def log_password_reset(username: str) -> None:
    """Catat reset password."""
    _logger.info(f"PWD_RESET | user={username}")


def log_security_event(event: str, detail: str = "") -> None:
    """Catat event keamanan umum (misal: config error, suspicious activity)."""
    _logger.warning(f"SECURITY | event={event} | {detail}")
