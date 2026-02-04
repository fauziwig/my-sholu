# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan dalam file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/lang/id/).

## [Unreleased]

### Added
- Fitur notifikasi waktu sholat (planned)
- Support untuk tema gelap/terang (planned)
- Konfigurasi melalui GUI (planned)

## [1.0.0] - 2026-02-04

### Added
- **Initial release** - Rilis pertama aplikasi Jadwal Sholat
- System tray indicator menggunakan GTK3 dan Ayatana AppIndicator
- Menu context untuk menampilkan jadwal sholat harian
- Integrasi dengan menu aplikasi Linux Mint/XFCE
- Script `src/fetch_jadwal.py` untuk mengambil data dari API MyQuran
- Utility `src/get_data_json.py` untuk membaca data JSON
- Dokumentasi lengkap (README, INSTALL, USAGE, CONTRIBUTING)
- File desktop entry untuk integrasi menu aplikasi
- Lisensi MIT

### Features
- Menampilkan 8 waktu sholat: Imsak, Subuh, Terbit, Dhuha, Dzuhur, Ashar, Maghrib, Isya
- Auto-load data berdasarkan tanggal hari ini
- Manual refresh data dari menu
- Data tersimpan dalam format JSON
- Ringan dan cepat (Python 3, GTK3)

### Technical
- Menggunakan PyGObject untuk binding GTK3
- Support AppIndicator3 untuk system tray
- Error handling untuk file JSON dan API
- Cross-platform Linux support

---

## Template untuk Release Baru

```
## [X.Y.Z] - YYYY-MM-DD

### Added
- Fitur baru

### Changed
- Perubahan pada fitur yang sudah ada

### Deprecated
- Fitur yang akan dihapus

### Removed
- Fitur yang dihapus

### Fixed
- Bug yang diperbaiki

### Security
- Perbaikan security
```

---

## Release Notes Detail

### Version 1.0.0

**Tanggal Rilis:** 4 Februari 2026

**Highlights:**
- 🎉 Rilis pertama aplikasi Jadwal Sholat
- 🖥️ System tray indicator untuk Linux
- 📅 Data jadwal sholat otomatis
- 🚀 Ringan dan mudah digunakan

**Cocok untuk:**
- Linux Mint XFCE
- Ubuntu
- Distribusi Linux berbasis GTK3

**Dependencies:**
- Python 3.6+
- GTK3
- Ayatana AppIndicator3
- requests library

**Catatan Instalasi:**
Lihat [INSTALL.md](INSTALL.md) untuk panduan instalasi lengkap.

**Known Issues:**
- Belum ada fitur notifikasi otomatis
- Konfigurasi kota hanya bisa dilakukan dengan edit file
- Belum ada support untuk timezone selain sistem

**Upgrade Path:**
Untuk update ke versi berikutnya, cukup pull latest code dan jalankan aplikasi.

---

## Contributors

Terima kasih kepada kontributor yang telah berkontribusi pada proyek ini:

- **Fauziwig** - Initial development and documentation

---

## Contact

Untuk pertanyaan, bug report, atau feature request:
- Buat issue di GitHub repository
- Email: [your-email@example.com]

---

**Catatan:** Changelog ini diupdate secara manual. Pastikan setiap release
memiliki entry yang lengkap dan akurat.
