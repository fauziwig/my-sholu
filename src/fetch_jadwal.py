#!/usr/bin/env python3
"""
Script untuk mengambil data jadwal sholat dari API MyQuran.

Script ini mengambil data jadwal sholat bulanan dari API MyQuran
(https://api.myquran.com/) dan menyimpannya ke file jadwal.json.

Dependencies:
    - requests: Untuk HTTP requests ke API

Usage:
    $ python3 fetch_jadwal.py
    Jadwal tersimpan

Configuration:
    Edit variabel URL di bawah ini dengan ID kota dan periode yang diinginkan.
    ID kota dapat ditemukan di https://api.myquran.com/

Example:
    # Mengambil jadwal untuk Jakarta (ID: 1301) bulan Februari 2026
    URL = "https://api.myquran.com/v3/sholat/jadwal/1301/2026-02"

    # Mengambil jadwal untuk Surabaya (ID: 1605) bulan Maret 2026
    URL = "https://api.myquran.com/v3/sholat/jadwal/1605/2026-03"

Author:
    Fauziwig

License:
    MIT License
"""

import requests
import json
import os
import sys


# ============================================================================
# KONFIGURASI
# ============================================================================

# ID Kota default (Jakarta: 1301)
# Ganti dengan ID kota Anda. Lihat daftar kota di https://api.myquran.com/
CITY_ID = "577ef1154f3240ad5b9b413aa7346a1e"

# Format: YYYY-MM
PERIOD = "2026-02"

# URL API MyQuran
# Format: https://api.myquran.com/v3/sholat/jadwal/{city_id}/{year-month}
URL = f"https://api.myquran.com/v3/sholat/jadwal/{CITY_ID}/{PERIOD}"

# Path output file JSON
# File akan disimpan di direktori yang sama dengan script ini
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "jadwal.json"
)


def fetch_schedule_data(url):
    """Mengambil data jadwal sholat dari API MyQuran.
    
    Melakukan HTTP GET request ke API MyQuran dan mengembalikan
    data JSON hasil response.
    
    Args:
        url (str): URL API endpoint untuk mengambil data jadwal.
    
    Returns:
        dict: Data JSON hasil response dari API.
        
        Format response:
        {
            "status": true,
            "request": {...},
            "data": {
                "jadwal": {
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
            }
        }
    
    Raises:
        requests.exceptions.RequestException: Jika terjadi error saat
            melakukan HTTP request (timeout, connection error, dll).
        json.JSONDecodeError: Jika response tidak valid JSON.
    
    Example:
        >>> url = "https://api.myquran.com/v3/sholat/jadwal/1301/2026-02"
        >>> data = fetch_schedule_data(url)
        >>> print(data['data']['jadwal']['2026-02-04']['subuh'])
        '04:40'
    """
    try:
        print(f"Mengambil data dari: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise exception untuk status code >= 400
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: Request timeout. Periksa koneksi internet Anda.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Tidak dapat terhubung ke server. Periksa koneksi internet.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP Error {e.response.status_code}")
        sys.exit(1)


def save_schedule_data(data, output_path):
    """Menyimpan data jadwal ke file JSON.
    
    Menyimpan dictionary berisi data jadwal sholat ke file JSON
    dengan format yang terstruktur dan readable.
    
    Args:
        data (dict): Dictionary berisi data jadwal sholat.
        output_path (str): Path lengkap ke file output JSON.
    
    Returns:
        bool: True jika berhasil menyimpan, False jika gagal.
    
    Raises:
        IOError: Jika tidak dapat menulis ke file (permission denied,
            disk full, dll).
        TypeError: Jika data bukan tipe dict.
    
    Example:
        >>> data = {"2026-02-04": {"subuh": "04:40"}}
        >>> success = save_schedule_data(data, "jadwal.json")
        >>> if success:
        ...     print("Data tersimpan")
    """
    try:
        # Pastikan direktori ada
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Simpan dengan formatting yang rapi
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except PermissionError:
        print(f"Error: Tidak memiliki izin menulis ke {output_path}")
        return False
    except IOError as e:
        print(f"Error: Gagal menulis file - {e}")
        return False


def main():
    """Entry point utama script.
    
    Fungsi ini mengorkestrasi proses pengambilan data dari API
    dan penyimpanan ke file JSON.
    
    Flow:
        1. Fetch data dari API
        2. Ekstrak data jadwal dari response
        3. Simpan ke file JSON
        4. Tampilkan konfirmasi
    
    Example:
        $ python3 fetch_jadwal.py
        Mengambil data dari: https://api.myquran.com/v3/sholat/jadwal/...
        Jadwal tersimpan
        Lokasi file: /home/user/Documents/coding/myReminder/jadwal.json
    
    Exit Codes:
        0: Success
        1: Error (network, file, dll)
    """
    try:
        # Ambil data dari API
        response_data = fetch_schedule_data(URL)
        
        # Ekstrak data jadwal dari response
        # Struktur: response -> data -> jadwal
        schedule_data = response_data.get("data", {}).get("jadwal", {})
        
        if not schedule_data:
            print("Error: Tidak ada data jadwal dalam response")
            sys.exit(1)
        
        # Simpan ke file
        if save_schedule_data(schedule_data, OUTPUT_FILE):
            print(f"Jadwal tersimpan")
            print(f"Lokasi file: {OUTPUT_FILE}")
            print(f"Total hari: {len(schedule_data)}")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nDihentikan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"Error tidak terduga: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
