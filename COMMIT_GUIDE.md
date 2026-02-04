# 🚀 Panduan Commit ke GitHub

## ✅ Struktur Sudah Siap!

```
jadwal-sholat/
├── assets/           # Audio & data files
├── src/              # Source code Python
├── docs/             # Dokumentasi
├── tests/            # Unit tests (kosong)
├── jadwal-sholat     # Launcher script
├── .gitignore        # Git ignore rules
├── requirements.txt  # Python dependencies
├── LICENSE           # MIT License
└── README.md         # Main documentation
```

## 📝 Langkah Commit

### 1. Inisialisasi Git Repository

```bash
cd ~/Documents/coding/myReminder
git init
```

### 2. Konfigurasi Git (Satu kali saja)

```bash
git config user.name "Nama Anda"
git config user.email "email@example.com"
```

### 3. Stage & Commit Files

```bash
# Stage semua file
git add .

# Commit dengan pesan
git commit -m "feat: Initial release v1.0.0

- System tray indicator for Linux
- Prayer time notifications with audio
- Auto-play adzan when prayer time arrives
- GTK3 popup notifications
- Pygame audio playback
- Timer thread for monitoring prayer times"
```

### 4. Push ke GitHub

```bash
# Tambah remote repository
git remote add origin https://github.com/username/jadwal-sholat.git

# Push ke main branch
git branch -M main
git push -u origin main
```

## 🎯 Apa yang Akan Terlihat di GitHub?

✅ README.md dengan badges dan screenshot
✅ Source code yang terorganisir rapi
✅ Dokumentasi lengkap
✅ License MIT
✅ Requirements terdefinisi
✅ .gitignore yang proper

## 📌 Tips Portfolio

1. **Tambahkan Screenshot**: Buat screenshot app di docs/screenshot.png
2. **Update Author**: Ganti "Fauziwig" dengan nama Anda di README.md
3. **Tambah GitHub URL**: Update link di README.md
4. **Buat Release**: Setelah push, buat release v1.0.0 di GitHub

## 🔗 Repository URL

Ganti `username` dengan username GitHub Anda:
```
https://github.com/username/jadwal-sholat
```

## ✨ Selesai!

Struktur sudah siap untuk di-commit. Semua paths sudah diperbarui untuk struktur folder baru.
