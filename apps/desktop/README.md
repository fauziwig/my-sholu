# MySholu Desktop (Electron)

Aplikasi desktop jadwal sholat menggunakan Electron untuk Linux.

## Instalasi

```bash
# Install dependencies
npm install

# Run app
npm start

# Build distributable
npm run build
```

## Struktur Proyek

```
apps/desktop/
├── src/
│   ├── main/
│   │   ├── index.js           # Main process
│   │   ├── prayerService.js   # Prayer time checker
│   │   └── controllers/       # IPC controllers
│   ├── preload/
│   │   └── index.js           # Preload script
│   └── renderer/
│       ├── index.html         # UI
│       └── app.js             # Renderer logic
assets/
├── jadwal.json                # Prayer schedule data
└── sound_adzan_alaqsa2_64_22.mp3  # Adzan audio
```

## Fitur

- ✅ System tray indicator
- ✅ Prayer time notifications
- ✅ Adzan audio playback
- ✅ Countdown to next prayer
- ✅ Auto-refresh data
- ✅ Minimal UI

## Requirements

- Node.js 16+
- Electron 28+
- mpg123 (for audio playback)

```bash
sudo apt install mpg123
```

## Cara Build
- Run for build app
```
# Build distributable
npm run build
```
- Setelah itu, test hasil build 
```
./dist/<filename>.AppImage 

```
- Pindah ke directory ~/Application/ di root dan berikan akses execute untuk file AppImage tersebut
```
mv dist/MySholu-1.0.0.AppImage ~/Applications/
chmod +x ~/Applications/MySholu-1.0.0.AppImage
```
- Buat desktop entry untuk MySholu app agar bisa terlihat di list app Window
`nano ~/.local/share/applications/mysholu.desktop`
```
[Desktop Entry]
Name=MySholu
Comment=Jadwal Sholat Desktop App
Exec=/home/fauziwig/Applications/MySholu-1.0.0.AppImage
Icon=/home/fauziwig/Documents/coding/MySholu/apps/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;
```
- Buat MySholu app otomatis dijalankan ketika laptop menyala (auto-start)
`cp ~/.local/share/applications/mysholu.desktop ~/.config/autostart/`
