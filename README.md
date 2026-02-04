# 🕌 MySholu

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-green.svg)](#)
[![Python](https://img.shields.io/badge/python-3.6+-yellow.svg)](#)

Aplikasi penampil jadwal sholat untuk Linux dengan system tray indicator dan notifikasi adzan otomatis. Aplikasi ini menampilkan jadwal sholat harian langsung di system tray Linux Anda dengan fitur pengingat waktu sholat lengkap dengan suara adzan.

![Screenshot](docs/screenshot.png)

## ✨ Fitur

- 🔔 **Notifikasi Waktu Sholat** - Popup dan suara adzan otomatis saat masuk waktu sholat
- 🔊 **Audio Adzan** - Memutar suara adzan menggunakan pygame
- 🖥️ **System Tray Indicator** - Akses cepat jadwal sholat dari system tray
- 📅 **Data Harian Otomatis** - Menampilkan jadwal sholat sesuai tanggal hari ini
- 🔄 **Refresh Manual** - Perbarui data jadwal kapan saja
- 📱 **Integrasi Menu Aplikasi** - Muncul di menu aplikasi Linux Mint/XFCE
- ⚡ **Ringan & Cepat** - Menggunakan Python dan GTK3

## 🚀 Quick Start

### Prerequisites

- Python 3.6 atau lebih tinggi
- GTK3 (GObject Introspection)
- Ayatana AppIndicator
- Library Python: `requests`, `PyGObject`, `pygame`

### Install Dependencies

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1

# Install Python dependencies
pip3 install -r requirements.txt
```

### Install & Run

```bash
# Clone repository
cd ~/Documents
git clone https://github.com/username/mysholu.git
cd mysholu

# Setup virtual environment (recommended)
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip3 install pygame

# Jalankan aplikasi
./mysholu
```

## 📁 Struktur Proyek

```
mysholu/
├── assets/                    # Assets (audio, data)
│   ├── sound_adzan_alaqsa2_64_22.mp3
│   └── jadwal.json
├── src/                       # Source code
│   ├── panel_jadwal.py       # Aplikasi utama (GUI system tray)
│   ├── fetch_jadwal.py       # Script mengambil data dari API
│   └── get_data_json.py      # Utility membaca data JSON
├── docs/                      # Dokumentasi
│   ├── INSTALL.md            # Panduan instalasi detail
│   ├── USAGE.md              # Panduan penggunaan
│   ├── CONTRIBUTING.md       # Panduan berkontribusi
│   └── CHANGELOG.md          # Riwayat perubahan
├── tests/                     # Unit tests
├── mysholu                    # Launcher script
├── requirements.txt          # Dependencies
├── LICENSE                   # Lisensi MIT
└── README.md                 # Dokumentasi ini
```

## 📖 Dokumentasi

- **[INSTALL.md](docs/INSTALL.md)** - Panduan instalasi lengkap
- **[USAGE.md](docs/USAGE.md)** - Panduan penggunaan dan konfigurasi
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Cara berkontribusi
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Riwayat versi

## 🎯 Cara Penggunaan

### Menjalankan Aplikasi

```bash
# Dari terminal
./mysholu

# Atau langsung
python3 src/panel_jadwal.py
```

### Mengupdate Data Jadwal

```bash
python3 src/fetch_jadwal.py
```

**Catatan:** Edit `src/fetch_jadwal.py` dan ganti `CITY_ID` dengan ID kota Anda.

### Autostart (Opsional)

Untuk menjalankan otomatis saat login:

```bash
# Copy desktop file
cp mysholu.desktop ~/.config/autostart/

# Atau manual via Settings → Session and Startup
```

## 🛠️ Teknologi

- **Python 3.6+** - Bahasa pemrograman
- **GTK3** - GUI toolkit
- **Ayatana AppIndicator** - System tray integration
- **Pygame** - Audio playback
- **MyQuran API** - Data jadwal sholat

## 🐛 Troubleshooting

### Audio tidak berbunyi
- Pastikan pygame terinstall: `pip3 install pygame`
- Cek volume sistem
- Test file audio: `mpg123 assets/sound_adzan_alaqsa2_64_22.mp3`

### Aplikasi tidak muncul di system tray
- Pastikan system tray aktif di desktop environment
- Jalankan dari terminal untuk melihat error: `python3 src/panel_jadwal.py`

### Error: ModuleNotFoundError
```bash
pip3 install -r requirements.txt
```

## 🤝 Contributing

Kontribusi sangat diterima! Silakan baca [CONTRIBUTING.md](docs/CONTRIBUTING.md) untuk panduan berkontribusi.

## 📄 License

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 🙏 Acknowledgments

- Data jadwal sholat oleh [MyQuran API](https://api.myquran.com/)
- Audio adzan Al-Aqsa
- Icon oleh GTK3 default theme


---

**Catatan:** Aplikasi ini dikembangkan untuk Linux Mint XFCE namun seharusnya kompatibel dengan distribusi Linux lain yang menggunakan GTK3.
