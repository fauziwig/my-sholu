#!/usr/bin/env python3
"""
Utility script untuk membaca dan menampilkan data jadwal sholat.

Script ini membaca file jadwal.json dan menampilkan informasi
jadwal sholat dalam format yang mudah dibaca. Cocok digunakan
untuk testing atau melihat data tanpa menjalankan aplikasi GUI.

Dependencies:
    - Python 3.6+ (standard library only)

Usage:
    $ python3 get_data_json.py
    Jadwal: Kamis, 5 Februari 2026

    Atau untuk menampilkan jadwal lengkap hari ini:
    $ python3 get_data_json.py --today

File Structure:
    File jadwal.json memiliki struktur:
    {
        "2026-02-04": {
            "tanggal": "Rabu, 4 Februari 2026",
            "imsak": "04:30",
            "subuh": "04:40",
            "terbit": "06:00",
            "dhuha": "06:15",
            "dzuhur": "12:00",
            "ashar": "15:15",
            "maghrib": "18:10",
            "isya": "19:20"
        },
        ...
    }

Author:
    Fauziwig

License:
    MIT License
"""

import json
import os
import sys
from datetime import datetime


# ============================================================================
# KONFIGURASI
# ============================================================================

# Path ke file jadwal.json
# Default: file di direktori yang sama dengan script ini
DEFAULT_JSON_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "jadwal.json"
)


def load_schedule_data(file_path):
    """Membaca data jadwal sholat dari file JSON.
    
    Membaca dan memparsing file jadwal.json menjadi Python dictionary.
    
    Args:
        file_path (str): Path lengkap ke file jadwal.json.
    
    Returns:
        dict: Data jadwal sholat dengan format:
            {
                "2026-02-04": {
                    "tanggal": "Rabu, 4 Februari 2026",
                    "imsak": "04:30",
                    "subuh": "04:40",
                    ...
                }
            }
        
        Mengembalikan dictionary kosong jika file tidak ditemukan
        atau format JSON tidak valid.
    
    Raises:
        FileNotFoundError: Jika file tidak ditemukan (ditangkap dan diproses).
        json.JSONDecodeError: Jika format JSON tidak valid (ditangkap dan diproses).
    
    Example:
        >>> data = load_schedule_data("jadwal.json")
        >>> print(len(data))
        28
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
        print("Jalankan 'python3 fetch_jadwal.py' terlebih dahulu untuk mengambil data.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Format JSON tidak valid di file '{file_path}'.")
        print(f"Detail: {e}")
        return {}


def get_schedule_for_date(data, date_str):
    """Mengambil data jadwal untuk tanggal tertentu.
    
    Args:
        data (dict): Dictionary berisi seluruh data jadwal.
        date_str (str): Tanggal dalam format "YYYY-MM-DD".
    
    Returns:
        dict atau None: Data jadwal untuk tanggal tersebut,
            atau None jika tidak ditemukan.
    
    Example:
        >>> data = load_schedule_data("jadwal.json")
        >>> today = get_schedule_for_date(data, "2026-02-04")
        >>> if today:
        ...     print(today['subuh'])
        '04:40'
    """
    return data.get(date_str)


def get_today_schedule(data):
    """Mengambil data jadwal untuk hari ini.
    
    Mengembalikan data jadwal sholat berdasarkan tanggal hari ini
    sesuai dengan sistem clock.
    
    Args:
        data (dict): Dictionary berisi seluruh data jadwal.
    
    Returns:
        tuple: (date_str, schedule_data) dimana:
            - date_str (str): Tanggal hari ini format "YYYY-MM-DD"
            - schedule_data (dict atau None): Data jadwal hari ini
    
    Example:
        >>> data = load_schedule_data("jadwal.json")
        >>> date, schedule = get_today_schedule(data)
        >>> print(f"Jadwal untuk {date}: {schedule['tanggal']}")
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return today, data.get(today)


def print_schedule(schedule, date_str=None):
    """Menampilkan data jadwal dalam format yang rapi.
    
    Args:
        schedule (dict): Dictionary berisi data jadwal satu hari.
        date_str (str, optional): Tanggal untuk ditampilkan di header.
    
    Example:
        >>> data = load_schedule_data("jadwal.json")
        >>> schedule = data.get("2026-02-04")
        >>> print_schedule(schedule, "2026-02-04")
    """
    if not schedule:
        print("Tidak ada data jadwal untuk tanggal ini.")
        return
    
    # Header
    if date_str:
        print(f"\n{'='*50}")
        print(f"Jadwal Sholat - {date_str}")
        print(f"{'='*50}")
    
    # Tanggal dalam format Indonesia
    print(f"Tanggal: {schedule.get('tanggal', 'N/A')}\n")
    
    # Daftar waktu sholat
    prayer_times = [
        ('imsak', 'Imsak'),
        ('subuh', 'Subuh'),
        ('terbit', 'Terbit'),
        ('dhuha', 'Dhuha'),
        ('dzuhur', 'Dzuhur'),
        ('ashar', 'Ashar'),
        ('maghrib', 'Maghrib'),
        ('isya', 'Isya')
    ]
    
    print(f"{'Waktu Sholat':<15} | {'Jam':<10}")
    print("-" * 30)
    
    for key, label in prayer_times:
        time = schedule.get(key, '-')
        print(f"{label:<15} | {time:<10}")
    
    print()


def print_all_schedules(data):
    """Menampilkan semua data jadwal dalam file.
    
    Args:
        data (dict): Dictionary berisi seluruh data jadwal.
    
    Example:
        >>> data = load_schedule_data("jadwal.json")
        >>> print_all_schedules(data)
    """
    if not data:
        print("Tidak ada data jadwal.")
        return
    
    print(f"\nTotal jadwal: {len(data)} hari\n")
    
    for date_str in sorted(data.keys()):
        print_schedule(data[date_str], date_str)


def main():
    """Entry point utama script.
    
    Fungsi ini membaca file jadwal.json dan menampilkan informasi
    jadwal sholat. Secara default menampilkan jadwal untuk tanggal
    sample (2026-02-01), namun dapat dimodifikasi untuk menampilkan
    hari ini atau semua data.
    
    Example:
        $ python3 get_data_json.py
        Jadwal: Kamis, 5 Februari 2026
    
    Exit Codes:
        0: Success
        1: Error (file not found, invalid JSON)
    """
    # Load data
    data = load_schedule_data(DEFAULT_JSON_PATH)
    
    if not data:
        sys.exit(1)
    
    # Contoh: Tampilkan jadwal untuk tanggal tertentu
    sample_date = "2026-02-01"
    schedule = get_schedule_for_date(data, sample_date)
    
    if schedule:
        print(f"Jadwal: {schedule['tanggal']}")
    else:
        print(f"Data untuk tanggal {sample_date} tidak ditemukan.")
    
    # Uncomment baris di bawah untuk fitur tambahan:
    
    # Tampilkan jadwal hari ini
    # today, today_schedule = get_today_schedule(data)
    # print_schedule(today_schedule, today)
    
    # Tampilkan semua jadwal
    # print_all_schedules(data)


if __name__ == "__main__":
    main()
