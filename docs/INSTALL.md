# Panduan Instalasi Jadwal Sholat

Dokumen ini berisi panduan instalasi lengkap untuk aplikasi Jadwal Sholat di berbagai distribusi Linux.

## Daftar Isi

1. [Persyaratan Sistem](#persyaratan-sistem)
2. [Instalasi Dependencies](#instalasi-dependencies)
3. [Setup Aplikasi](#setup-aplikasi)
4. [Autostart](#autostart)
5. [Uninstall](#uninstall)

## Persyaratan Sistem

### Minimum Requirements

- **OS**: Linux Mint, Ubuntu, atau distribusi berbasis Debian lainnya
- **Desktop Environment**: XFCE, GNOME, KDE, atau yang mendukung system tray
- **Python**: Versi 3.6 atau lebih tinggi
- **RAM**: 50 MB (sangat ringan)
- **Storage**: 10 MB

### Dependencies Python

- `requests` - Untuk HTTP requests ke API
- `PyGObject` - Binding Python untuk GTK3

### Dependencies Sistem

- `gir1.2-gtk-3.0` - GTK3 GObject Introspection
- `gir1.2-ayatanaappindicator3-0.1` - AppIndicator untuk system tray

## Instalasi Dependencies

### Linux Mint / Ubuntu / Debian

```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-ayatanaappindicator3-0.1

# Install Python dependencies
pip3 install --user requests PyGObject
```

### Fedora / RHEL / CentOS

```bash
# Install system dependencies
sudo dnf install -y \
    python3 \
    python3-pip \
    python3-gobject \
    gtk3 \
    libappindicator-gtk3

# Install Python dependencies
pip3 install --user requests PyGObject
```

### Arch Linux / Manjaro

```bash
# Install system dependencies
sudo pacman -S \
    python \
    python-pip \
    python-gobject \
    gtk3 \
    libappindicator-gtk3

# Install Python dependencies
pip3 install --user requests PyGObject
```

## Setup Aplikasi

### Metode 1: Instalasi Manual (Direkomendasikan)

1. **Download atau clone repository**

```bash
cd ~/Documents/coding
# Jika menggunakan git
git clone <repository-url> myReminder

# Atau download manual dan ekstrak ke ~/Documents/coding/myReminder
cd myReminder
```

2. **Berikan permission execute pada script**

```bash
chmod +x src/panel_jadwal.py
chmod +x src/fetch_jadwal.py
chmod +x src/get_data_json.py
```

3. **Download data jadwal pertama kali**

Edit file `src/fetch_jadwal.py` dan ganti URL dengan ID kota Anda:

```python
URL = "https://api.myquran.com/v3/sholat/jadwal/YOUR_CITY_ID/2026-02"
```

Kemudian jalankan:

```bash
python3 src/src/fetch_jadwal.py
```

4. **Test aplikasi**

```bash
./jadwal-sholat
```

Jika system tray indicator muncul, instalasi berhasil!

5. **Install ke menu aplikasi**

```bash
# Buat direktori jika belum ada
mkdir -p ~/.local/share/applications

# Copy desktop file
cp jadwal-sholat.desktop ~/.local/share/applications/

# Update database menu
update-desktop-database ~/.local/share/applications/
```

### Metode 2: Instalasi Global (untuk semua user)

Jika Anda ingin menginstall aplikasi untuk semua user di sistem:

```bash
# Copy aplikasi ke /opt
sudo mkdir -p /opt/jadwal-sholat
sudo cp -r * /opt/jadwal-sholat/

# Berikan permission
sudo chmod +x /opt/jadwal-sholat/src/panel_jadwal.py
sudo chmod +x /opt/jadwal-sholat/src/fetch_jadwal.py

# Update desktop file untuk path global
sudo sed -i 's|.|/opt/jadwal-sholat|g' \
    /opt/jadwal-sholat/jadwal-sholat.desktop

# Copy ke system applications
sudo cp /opt/jadwal-sholat/jadwal-sholat.desktop /usr/share/applications/

# Update database menu
sudo update-desktop-database /usr/share/applications/
```

## Autostart

Agar aplikasi berjalan otomatis saat login:

### Linux Mint / XFCE

1. Buka **Settings** → **Session and Startup**
2. Tab **Application Autostart**
3. Klik **Add**
4. Isi:
   - **Name**: Jadwal Sholat
   - **Description**: Aplikasi penampil jadwal sholat
   - **Command**: `./jadwal-sholat`
5. Klik **OK**

### Command Line Method

```bash
# Buat autostart directory jika belum ada
mkdir -p ~/.config/autostart

# Buat desktop file untuk autostart
cat > ~/.config/autostart/jadwal-sholat.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Jadwal Sholat
Exec=./jadwal-sholat
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
```

### Verifikasi Autostart

Logout dan login kembali, aplikasi seharusnya berjalan otomatis.

## Uninstall

### Uninstall Instalasi Manual

```bash
# Hapus dari menu aplikasi
rm ~/.local/share/applications/jadwal-sholat.desktop

# Update database menu
update-desktop-database ~/.local/share/applications/

# Hapus autostart (jika ada)
rm ~/.config/autostart/jadwal-sholat.desktop

# Hapus direktori aplikasi (opsional)
rm -rf ~/Documents/coding/myReminder
```

### Uninstall Instalasi Global

```bash
# Hapus dari system applications
sudo rm /usr/share/applications/jadwal-sholat.desktop
sudo rm -rf /opt/jadwal-sholat

# Update database menu
sudo update-desktop-database /usr/share/applications/
```

## Troubleshooting Instalasi

### Error: `pip3: command not found`

```bash
sudo apt install python3-pip
```

### Error: `No module named 'gi'`

```bash
sudo apt install python3-gi python3-gi-cairo
```

### Error: `Namespace AyatanaAppIndicator3 not available`

```bash
sudo apt install gir1.2-ayatanaappindicator3-0.1
```

### Error: `requests module not found`

```bash
pip3 install --user requests
```

### Permission denied saat menjalankan script

```bash
chmod +x src/panel_jadwal.py
```

### Aplikasi tidak muncul di menu

```bash
# Pastikan desktop file valid
desktop-file-validate ~/.local/share/applications/jadwal-sholat.desktop

# Update database menu
update-desktop-database ~/.local/share/applications/

# Restart panel (XFCE)
xfce4-panel -r
```

## Verifikasi Instalasi

Setelah instalasi, verifikasi dengan menjalankan:

```bash
# Test dependencies
python3 -c "import gi; gi.require_version('Gtk', '3.0'); print('GTK3 OK')"
python3 -c "import gi; gi.require_version('AyatanaAppIndicator3', '0.1'); print('AppIndicator OK')"
python3 -c "import requests; print('Requests OK')"

# Test aplikasi
./jadwal-sholat &
```

Jika semua test berhasil dan system tray indicator muncul, instalasi berhasil!

---

**Butuh bantuan?** Silakan buat issue di repository GitHub atau hubungi maintainer.
