# 🕌 MySholu Desktop (Electron)

![Preview MySholu](apps/assets/Preview%20MySholu.png)



[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-green.svg)](#)
[![Electron](https://img.shields.io/badge/electron-28.0-blue.svg)](#)

Aplikasi desktop jadwal sholat untuk Linux menggunakan Electron dengan system tray indicator dan notifikasi adzan otomatis.

## ✨ Fitur

- 🔔 **Notifikasi Waktu Sholat** - Popup dan suara adzan otomatis
- 🔊 **Audio Adzan** - Memutar suara adzan menggunakan mpg123
- 🖥️ **System Tray** - Akses cepat jadwal sholat dari system tray
- ⏰ **Countdown** - Hitung mundur ke waktu sholat berikutnya
- 📅 **Jadwal Imsakiyah** - Data jadwal sholat Ramadan
- ⚡ **Ringan & Cepat** - Menggunakan Electron

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- mpg123 (untuk audio adzan)

```bash
sudo apt install mpg123
```

### Install & Run

```bash
# Install dependencies
npm install

# Run app
npm start

# Build AppImage
npm run build
```

## 📁 Struktur Proyek

```
apps/
├── desktop/
│   └── src/
│       ├── main/           # Main process
│       ├── preload/        # Preload scripts
│       └── renderer/       # UI
└── assets/                 # Icons, audio, data
    ├── icon.png
    ├── icon-tray.png
    ├── jadwal_imsakiyah.json
    └── sound_adzan_alaqsa2_64_22.mp3
```

## 📖 Dokumentasi

Lihat [ELECTRON_IMPLEMENTATION.md](ELECTRON_IMPLEMENTATION.md) untuk detail implementasi.

## 🛠️ Teknologi

- **Electron 28** - Desktop framework
- **Node.js** - Runtime
- **mpg123** - Audio playback

## 📄 License

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

