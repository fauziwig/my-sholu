# 🕌 MySholu Desktop (Electron)

![Preview MySholu](apps/assets/Preview%20MySholu.png)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-green.svg)](#)
[![Electron](https://img.shields.io/badge/electron-28.0-blue.svg)](#)

MySholu adalah aplikasi desktop Linux berbasis Electron untuk menampilkan jadwal sholat, menyediakan indikator status di area system tray, serta memicu notifikasi visual dan audio adzan otomatis saat memasuki waktu sholat.

Aplikasi ini menggunakan teknologi web standar (HTML, CSS, Vanilla JS) untuk proses *renderer* dan Node.js/Electron untuk proses *main* tanpa memerlukan framework eksternal seperti React atau Vue, sehingga sangat ringan dan cepat.

---

## ✨ Fitur Utama

- 🔔 **Notifikasi Waktu Sholat Otomatis** - Menampilkan jendela notifikasi kustom saat waktu sholat tiba.
- 🔊 **Pemutaran Audio Adzan** - Memutar suara adzan secara otomatis menggunakan utilitas pemutar audio sistem `mpg123`.
- 🖥️ **System Tray Indicator** - Ikon tray dinamis yang menampilkan hitung mundur ke waktu sholat berikutnya serta daftar waktu sholat hari ini saat diklik kanan/kiri.
- ⏰ **Countdown Real-time** - Menampilkan hitungan mundur detik/menit menuju waktu sholat berikutnya di jendela utama maupun tray.
- 📅 **Data Jadwal Lokal** - Menggunakan data jadwal sholat terintegrasi dari [jadwal_imsakiyah.json](file:///home/fauziwig/Documents/coding/MySholu/apps/assets/jadwal_imsakiyah.json) sehingga dapat berjalan sepenuhnya secara offline tanpa koneksi internet.
- ⚡ **Tombol Uji Coba** - Memiliki tombol untuk menguji notifikasi langsung dari UI untuk memastikan suara adzan dan popup visual berfungsi.

---

## 🛠️ Prasyarat Sistem (Prerequisites)

Untuk menjalankan atau membangun aplikasi ini, Anda memerlukan:

1. **Node.js** (versi 16 atau lebih baru) dan **npm** terinstal di sistem Anda.
2. **mpg123** (pemutar audio CLI) terinstal di Linux Anda agar suara adzan dapat diputar.

### Cara Install `mpg123` di Linux:

Di keluarga Debian/Ubuntu/Mint:
```bash
sudo apt update
sudo apt install mpg123
```

Di Arch Linux:
```bash
sudo pacman -S mpg123
```

Di Fedora:
```bash
sudo dnf install mpg123
```

---

## 🚀 Panduan Memulai (Quick Start)

### 1. Instalasi Dependensi
Jalankan perintah berikut di direktori utama proyek untuk memasang seluruh pustaka yang dibutuhkan:
```bash
npm install
```

### 2. Menjalankan Aplikasi (Mode Pengembangan)
Untuk menguji dan menjalankan aplikasi secara lokal dengan *hot reload* atau eksekusi cepat, jalankan:
```bash
npm start
```
*Catatan: Anda juga bisa menggunakan perintah `npm run dev` yang akan memicu perintah start yang sama.*

---

## 📦 Pembangunan Aplikasi & Distribusi (Build)

Untuk mengemas aplikasi menjadi aplikasi mandiri yang siap digunakan tanpa perlu menjalankan terminal Node.js:

```bash
npm run build
```

Perintah ini akan menggunakan `electron-builder` untuk membuat berkas distribusi di dalam folder `dist/`:
- **`MySholu-1.1.0.AppImage`** (Berkas portabel universal untuk Linux)
- **`mysholu_1.1.0_amd64.deb`** (Paket instalasi untuk Debian/Ubuntu)

---

## 📝 Cara Instalasi & Autostart di Desktop Linux (Detail)

Setelah melakukan build, Anda dapat mengintegrasikan MySholu ke sistem Linux Anda agar terasa seperti aplikasi bawaan desktop:

### 1. Eksekusi AppImage
Pindahkan file hasil build ke folder aplikasi lokal Anda dan berikan izin eksekusi:
```bash
# Buat folder Applications jika belum ada
mkdir -p ~/Applications

# Pindahkan file AppImage
mv dist/MySholu-1.1.0.AppImage ~/Applications/

# Berikan izin eksekusi
chmod +x ~/Applications/MySholu-1.1.0.AppImage
```

### 2. Membuat Desktop Shortcut (Pintasan Aplikasi)
Agar MySholu muncul di menu pencarian aplikasi sistem Anda (seperti GNOME, KDE, atau XFCE), buat berkas desktop entry berikut:

```bash
nano ~/.local/share/applications/mysholu.desktop
```

Salin dan tempel konfigurasi berikut (sesuaikan path folder jika berbeda):
```ini
[Desktop Entry]
Name=MySholu
Comment=Aplikasi Jadwal Sholat Desktop
Exec=/home/fauziwig/Applications/MySholu-1.1.0.AppImage
Icon=/home/fauziwig/Documents/coding/MySholu/apps/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;
```

### 3. Mengatur Aplikasi agar Berjalan Otomatis Saat Laptop Menyala (Autostart)
Agar aplikasi otomatis berjalan di background sejak komputer Anda dinyalakan:

```bash
# Salin file desktop shortcut ke folder autostart
mkdir -p ~/.config/autostart
cp ~/.local/share/applications/mysholu.desktop ~/.config/autostart/
```

---

## 📁 Struktur Kode Proyek

Struktur folder aktif dalam aplikasi ini adalah:

```
MySholu/
├── apps/
│   ├── desktop/
│   │   └── src/
│   │       ├── main/          # Proses Utama Electron (App lifecycle, Tray, IPC)
│   │       ├── preload/       # Bridge IPC aman antara Main & Renderer
│   │       └── renderer/      # Frontend/Tampilan HTML, CSS, JS
│   └── assets/                # Aset runtime (Ikon, data jadwal, adzan MP3)
├── dist/                      # Direktori keluaran hasil build (AppImage & deb)
├── package.json               # Konfigurasi proyek, dependensi, dan skrip build
└── README.md                  # Dokumentasi proyek (berkas ini)
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
