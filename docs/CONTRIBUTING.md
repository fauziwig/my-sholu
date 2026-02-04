# Contributing to Jadwal Sholat

Terima kasih atas minat Anda untuk berkontribusi pada proyek Jadwal Sholat! Dokumen ini berisi panduan untuk berkontribusi.

## Daftar Isi

1. [Code of Conduct](#code-of-conduct)
2. [Cara Berkontribusi](#cara-berkontribusi)
3. [Development Setup](#development-setup)
4. [Standar Kode](#standar-kode)
5. [Pull Request Process](#pull-request-process)
6. [Reporting Issues](#reporting-issues)

## Code of Conduct

Proyek ini menggunakan [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
Dengan berpartisipasi, Anda diharapkan untuk menjaga lingkungan yang ramah dan inklusif.

## Cara Berkontribusi

### Anda bisa berkontribusi dengan:

- 🐛 **Report bugs** - Laporkan bug yang Anda temukan
- 💡 **Suggest features** - Usulkan fitur baru
- 📝 **Improve documentation** - Perbaiki dokumentasi
- 🔧 **Fix bugs** - Perbaiki bug yang ada
- ✨ **Add features** - Tambahkan fitur baru
- 🌍 **Translate** - Terjemahkan dokumentasi ke bahasa lain

### Langkah-langkah Kontribusi

1. **Fork repository**
2. **Clone fork Anda**
   ```bash
   git clone https://github.com/YOUR_USERNAME/myReminder.git
   cd myReminder
   ```
3. **Buat branch baru**
   ```bash
   git checkout -b feature/nama-fitur-anda
   ```
4. **Lakukan perubahan**
5. **Commit perubahan**
   ```bash
   git commit -m "feat: tambahkan fitur X"
   ```
6. **Push ke fork**
   ```bash
   git push origin feature/nama-fitur-anda
   ```
7. **Buat Pull Request**

## Development Setup

### Prerequisites

```bash
# Install dependencies pengembangan
sudo apt install python3 python3-pip python3-venv

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Struktur Proyek

```
myReminder/
├── src/panel_jadwal.py         # GUI utama
├── src/fetch_jadwal.py         # API client
├── src/get_data_json.py        # Data utilities
├── jadwal.json             # Data storage
├── jadwal-sholat.desktop   # Desktop entry
├── docs/                   # Dokumentasi tambahan
├── tests/                  # Unit tests
└── README.md
```

## Standar Kode

### Python Style Guide

Ikuti [PEP 8](https://pep8.org/) dengan konvensi berikut:

```python
# ✅ Good - Gunakan docstrings
"""
Aplikasi penampil jadwal sholat.

Aplikasi ini menampilkan jadwal sholat harian
melalui system tray indicator menggunakan GTK3.
"""

# ✅ Good - Nama fungsi dengan snake_case
def fetch_prayer_schedule(city_id):
    """Fetch jadwal sholat dari API."""
    pass

# ✅ Good - Nama class dengan PascalCase
class PrayerScheduleApp:
    """Aplikasi utama jadwal sholat."""
    pass

# ❌ Bad - Nama tidak deskriptif
def f():
    pass

class app:
    pass
```

### Docstring Format

Gunakan format Google-style atau NumPy-style:

```python
def get_today_schedule(data: dict) -> dict:
    """
    Ambil jadwal sholat untuk hari ini.

    Args:
        data (dict): Dictionary berisi data jadwal bulanan.

    Returns:
        dict: Data jadwal untuk hari ini, atau None jika tidak ditemukan.

    Examples:
        >>> data = {"2026-02-04": {"subuh": "04:30"}}
        >>> get_today_schedule(data)
        {"subuh": "04:30"}
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return data.get(today)
```

### Commit Message Convention

Gunakan [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Fitur baru
- `fix`: Perbaikan bug
- `docs`: Perubahan dokumentasi
- `style`: Formatting, tanpa perubahan kode
- `refactor`: Refactoring kode
- `test`: Menambah/memperbaiki tests
- `chore`: Maintenance tasks

**Contoh:**
```
feat(gui): tambahkan fitur notifikasi waktu sholat

Menambahkan popup notifikasi 10 menit sebelum waktu sholat.
Notifikasi dapat diaktifkan/nonaktifkan melalui menu.

Closes #123
```

## Pull Request Process

### Sebelum Membuat PR

1. **Sync dengan upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test perubahan Anda**
   ```bash
   ./jadwal-sholat
   # Pastikan aplikasi berjalan tanpa error
   ```

3. **Update dokumentasi** jika diperlukan

4. **Periksa code style**
   ```bash
   flake8 src/panel_jadwal.py
   pylint src/panel_jadwal.py
   ```

### PR Checklist

- [ ] Kode berjalan tanpa error
- [ ] Tidak ada regression
- [ ] Dokumentasi diupdate
- [ ] Commit messages mengikuti convention
- [ ] PR description menjelaskan perubahan

### PR Template

```markdown
## Description
Deskripsi singkat perubahan yang dilakukan.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Cara menguji perubahan ini:
1. ...
2. ...

## Checklist
- [ ] Kode di-test secara lokal
- [ ] Tidak ada error
- [ ] Dokumentasi diupdate

## Related Issues
Closes #123
```

## Reporting Issues

### Bug Reports

Gunakan template berikut:

```markdown
**Deskripsi Bug**
Deskripsi singkat bug yang ditemukan.

**Cara Reproduce**
Langkah-langkah:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
Apa yang seharusnya terjadi.

**Screenshots**
Jika ada, tambahkan screenshot.

**Environment:**
 - OS: [e.g. Linux Mint 21]
 - Desktop: [e.g. XFCE]
 - Python Version: [e.g. 3.10]
 - App Version: [e.g. 1.0.0]

**Additional Context**
Informasi tambahan.
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
Deskripsi masalah.

**Describe the solution you'd like**
Solusi yang diinginkan.

**Describe alternatives you've considered**
Alternatif lain yang sudah dipertimbangkan.

**Additional context**
Konteks tambahan.
```

## Development Guidelines

### Menambah Fitur Baru

1. Diskusikan dulu di Issue
2. Buat branch dengan nama deskriptif
3. Tulis kode dengan docstrings lengkap
4. Update dokumentasi terkait
5. Test secara menyeluruh

### Memperbaiki Bug

1. Verifikasi bug dengan reproduce steps
2. Buat test case jika memungkinkan
3. Perbaiki bug
4. Verifikasi fix tidak merusak fitur lain

### Refactoring

1. Pastikan ada tests sebelum refactor
2. Lakukan refactoring secara bertahap
3. Commit setiap perubahan kecil
4. Verifikasi tidak ada regression

## Testing

### Manual Testing Checklist

- [ ] Aplikasi berjalan tanpa error
- [ ] System tray indicator muncul
- [ ] Menu context berfungsi
- [ ] Data jadwal terbaca dengan benar
- [ ] Refresh data berfungsi
- [ ] Aplikasi keluar dengan aman

### Supported Platforms

Test aplikasi di:
- Linux Mint XFCE
- Ubuntu
- Distribusi berbasis Debian lainnya

## Code Review

Semua PR akan direview sebelum di-merge. Reviewer akan memeriksa:

- Kualitas kode
- Functional correctness
- Documentation completeness
- Test coverage
- Security concerns

## Getting Help

Jika Anda membutuhkan bantuan:

1. Baca dokumentasi di `docs/` dan `README.md`
2. Cari issue yang sudah ada
3. Tanyakan di discussions
4. Kontak maintainer

## Recognition

Kontributor akan diakui di:
- File `CONTRIBUTORS.md`
- Release notes
- README.md

---

Terima kasih telah berkontribusi! 🎉
