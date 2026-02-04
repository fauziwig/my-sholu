# Panduan Penggunaan Jadwal Sholat

Dokumen ini berisi panduan lengkap cara menggunakan aplikasi Jadwal Sholat sehari-hari.

## Daftar Isi

1. [Memulai](#memulai)
2. [Interface Aplikasi](#interface-aplikasi)
3. [Melihat Jadwal](#melihat-jadwal)
4. [Mengupdate Data](#mengupdate-data)
5. [Konfigurasi Kota](#konfigurasi-kota)
6. [Tips Penggunaan](#tips-penggunaan)

## Memulai

### Menjalankan Aplikasi

#### Dari Menu Aplikasi
1. Tekan tombol **Super** (Windows key) di keyboard
2. Ketik "Jadwal Sholat"
3. Klik ikon aplikasi untuk menjalankan

#### Dari Terminal
```bash
cd ~/Documents/coding/myReminder
./jadwal-sholat
```

#### Autostart (Jalankan Otomatis)
Lihat [INSTALL.md](INSTALL.md#autostart) untuk setup autostart.

### Indikator Berjalan

Setelah dijalankan, aplikasi akan berjalan di background dengan indicator di system tray (area notifikasi di pojok kanan atas). Aplikasi TIDAK akan muncul jendela utama - semua interaksi dilakukan melalui menu system tray.

## Interface Aplikasi

### System Tray Indicator

Aplikasi menggunakan ikon jam di system tray Anda. Lokasi ikon tergantung desktop environment:

- **XFCE**: Panel atas/bawah, area system tray
- **GNOME**: Top panel (memerlukan extension jika menggunakan GNOME 3)
- **KDE**: System tray di panel

### Menu Context

Klik ikon di system tray untuk membuka menu context dengan fitur:

1. **Header Tanggal** - Menampilkan tanggal hari ini
2. **Jadwal Sholat** - Daftar lengkap waktu sholat:
   - Imsak
   - Subuh
   - Terbit
   - Dhuha
   - Dzuhur
   - Ashar
   - Maghrib
   - Isya
3. **Refresh Data** - Perbarui data jadwal dari file JSON
4. **Keluar** - Tutup aplikasi

## Melihat Jadwal

### Langkah-langkah

1. **Klik ikon aplikasi** di system tray
2. **Lihat jadwal** di menu yang muncul
3. **Perhatikan format waktu**:
   ```
   Imsak      : 04:30
   Subuh      : 04:40
   Terbit     : 06:00
   Dhuha      : 06:15
   Dzuhur     : 12:00
   Ashar      : 15:15
   Maghrib    : 18:10
   Isya       : 19:20
   ```

### Informasi yang Ditampilkan

- **Tanggal**: Format Indonesia (contoh: "Rabu, 4 Februari 2026")
- **Waktu Sholat**: Format 24 jam (HH:MM)
- **Data Real-time**: Diambil dari file JSON yang diupdate sesuai bulan

### Jika Data Tidak Ditemukan

Jika muncul pesan "⚠️ Data hari ini tidak ditemukan", berarti:
- File `jadwal.json` belum ada
- Data untuk bulan ini belum di-fetch
- Format tanggal di file JSON tidak sesuai

**Solusi**: Jalankan `src/fetch_jadwal.py` untuk mengambil data terbaru.

## Mengupdate Data

### Mengambil Data dari API

Data jadwal diambil dari [MyQuran API](https://api.myquran.com/). Untuk mengupdate:

```bash
cd ~/Documents/coding/myReminder
python3 src/src/fetch_jadwal.py
```

Proses ini akan:
1. Mengambil data dari API
2. Menyimpan ke `jadwal.json`
3. Data otomatis tersedia di aplikasi

### Jadwal Update yang Direkomendasikan

- **Awal bulan**: Update data untuk bulan baru
- **Jika pindah kota**: Update dengan ID kota baru
- **Jika data error**: Refresh dengan fetch ulang

### Refresh Data di Aplikasi

Jika file `jadwal.json` diedit manual atau diupdate:

1. Klik ikon aplikasi di system tray
2. Pilih **"Refresh Data"**
3. Menu akan diupdate dengan data terbaru

## Konfigurasi Kota

### Mencari ID Kota

1. Kunjungi [MyQuran API Documentation](https://api.myquran.com/)
2. Cari endpoint untuk daftar kota
3. Temukan kota Anda dan catat ID-nya

### Mengubah Kota

Edit file `src/fetch_jadwal.py`:

```python
# Ganti YOUR_CITY_ID dengan ID kota Anda
URL = "https://api.myquran.com/v3/sholat/jadwal/YOUR_CITY_ID/2026-02"
```

Contoh ID kota populer:
- Jakarta: 1301
- Surabaya: 1605
- Bandung: 1210
- Yogyakarta: 1805
- Semarang: 1420

**Catatan**: Ganti juga tahun dan bulan di URL sesuai kebutuhan.

### Mengupdate Data Setelah Ganti Kota

```bash
python3 src/src/fetch_jadwal.py
```

Lalu refresh aplikasi dari menu system tray.

## Tips Penggunaan

### 1. Shortcut Keyboard

Buat shortcut keyboard untuk akses cepat:

**Linux Mint / XFCE**:
1. Settings → Keyboard → Application Shortcuts
2. Klik Add
3. Command: `./jadwal-sholat`
4. Press shortcut key (contoh: Super+S)

### 2. Mengetahui Waktu Sholat Saat Ini

Buat script sederhana:

```bash
#!/bin/bash
cd ~/Documents/coding/myReminder
python3 src/src/get_data_json.py
```

### 3. Autostart dengan Delay

Jika aplikasi error saat autostart, tambahkan delay:

```bash
# Di command autostart
bash -c "sleep 5 && ./jadwal-sholat"
```

### 4. Backup Data

Backup file `jadwal.json` secara berkala:

```bash
cp jadwal.json jadwal.json.backup
```

### 5. Multi-Monitor Setup

System tray indicator akan muncul di primary monitor. Jika menggunakan multi-monitor dan tidak terlihat:
- Pastikan panel/system tray ada di monitor yang benar
- Atau gunakan extension untuk menampilkan indicator di semua monitor

### 6. Custom Icon

Untuk mengganti ikon aplikasi:

1. Siapkan icon file (format .png atau .svg)
2. Edit `jadwal-sholat.desktop`:
   ```
   Icon=/path/to/your/icon.png
   ```
3. Update database menu:
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

### 7. Debug Mode

Jika aplikasi tidak berjalan, jalankan dengan debug:

```bash
./jadwal-sholat 2>&1 | tee debug.log
```

Periksa file `debug.log` untuk melihat error.

### 8. Integrasi dengan Cron

Update otomatis setiap awal bulan:

```bash
# Edit crontab
crontab -e

# Tambahkan line berikut (update setiap tanggal 1 jam 00:00)
0 0 1 * * cd . && python3 src/src/fetch_jadwal.py
```

## FAQ

**Q: Kenapa aplikasi tidak muncul di system tray?**
A: Pastikan desktop environment Anda mendukung AppIndicator. Beberapa DE memerlukan extension tambahan.

**Q: Bisakah aplikasi memberi notifikasi waktu sholat?**
A: Saat ini belum ada fitur notifikasi. Fitur ini dapat ditambahkan di versi mendatang.

**Q: Apakah bisa digunakan offline?**
A: Ya, setelah data di-fetch dan tersimpan di `jadwal.json`, aplikasi dapat digunakan offline.

**Q: Bagaimana jika saya pindah ke zona waktu lain?**
A: Waktu yang ditampilkan mengikuti waktu sistem. Pastikan timezone sistem Anda sudah benar.

**Q: Apakah ada versi mobile?**
A: Tidak, aplikasi ini khusus untuk desktop Linux.

---

**Masih ada pertanyaan?** Silakan buat issue di repository GitHub.
