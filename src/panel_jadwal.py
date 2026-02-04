#!/usr/bin/env python3
"""
Aplikasi Jadwal Sholat - System Tray Indicator dengan Notifikasi Adzan.

Aplikasi ini menampilkan jadwal sholat harian melalui system tray
indicator menggunakan GTK3 dan Ayatana AppIndicator. Dilengkapi dengan
fitur notifikasi popup dan audio adzan saat masuk waktu sholat.
"""

import gi
import json
import datetime
import signal
import os
import threading
import time

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3 as AppIndicator, GLib

# Audio imports
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame tidak terinstall. Fitur audio tidak akan berfungsi.")


class AudioManager:
    """Manager untuk audio playback menggunakan pygame."""
    
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.lock = threading.Lock()
        
        if PYGAME_AVAILABLE and os.path.exists(audio_file):
            try:
                pygame.mixer.init()
            except pygame.error as e:
                print(f"Error menginisialisasi pygame: {e}")
    
    def play(self):
        if not PYGAME_AVAILABLE:
            return False
        
        if not os.path.exists(self.audio_file):
            print(f"Error: File audio tidak ditemukan: {self.audio_file}")
            return False
        
        with self.lock:
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
                return True
            except pygame.error as e:
                print(f"Error memutar audio: {e}")
                return False
    
    def stop(self):
        if not PYGAME_AVAILABLE:
            return False
        
        with self.lock:
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                return True
            except pygame.error as e:
                print(f"Error menghentikan audio: {e}")
                return False
    
    def is_busy(self):
        """Cek apakah audio sedang diputar."""
        if not PYGAME_AVAILABLE:
            return False
        return pygame.mixer.music.get_busy()


class PrayerTimeChecker(threading.Thread):
    """Thread untuk memeriksa waktu sholat setiap menit."""
    
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.prayer_times = {}
        self.running = False
        self.last_triggered = {}
        self.lock = threading.Lock()
    
    def set_prayer_times(self, prayer_dict):
        with self.lock:
            self.prayer_times = prayer_dict.copy()
    
    def run(self):
        self.running = True
        
        while self.running:
            current_time = datetime.datetime.now().strftime("%H:%M")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            with self.lock:
                for prayer_name, prayer_time in self.prayer_times.items():
                    if (current_time == prayer_time and 
                        self.last_triggered.get(prayer_name) != current_date):
                        
                        self.last_triggered[prayer_name] = current_date
                        GLib.idle_add(self.callback, prayer_name)
                        break
            
            time.sleep(60)
    
    def stop(self):
        self.running = False


class PrayerNotificationDialog(Gtk.Dialog):
    """Dialog popup untuk notifikasi waktu sholat."""
    
    def __init__(self, prayer_name, on_close_callback=None):
        super().__init__(
            title="Waktu Sholat",
            parent=None,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        )
        
        self.prayer_name = prayer_name
        self.on_close_callback = on_close_callback
        
        self.set_default_size(400, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)
        
        content_area = self.get_content_area()
        content_area.set_spacing(10)
        
        # Icon
        icon_label = Gtk.Label()
        icon_label.set_markup("<span size='xx-large'>🕌</span>")
        icon_label.set_alignment(0.5, 0.5)
        content_area.pack_start(icon_label, False, False, 10)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup(
            f"<span size='x-large' weight='bold'>Waktu Sholat {prayer_name}</span>"
        )
        title_label.set_alignment(0.5, 0.5)
        content_area.pack_start(title_label, False, False, 5)
        
        # Message
        msg_label = Gtk.Label()
        current_time = datetime.datetime.now().strftime("%H:%M")
        msg_label.set_markup(
            f"<span size='medium'>Telah masuk waktu sholat {prayer_name}.</span>\n"
            f"<span size='small'>Waktu saat ini: {current_time}</span>"
        )
        msg_label.set_alignment(0.5, 0.5)
        content_area.pack_start(msg_label, False, False, 10)
        
        # Button
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        
        close_button = Gtk.Button(label="Tutup & Hentikan Adzan")
        close_button.set_size_request(200, 40)
        close_button.connect("clicked", self.on_close_clicked)
        button_box.pack_start(close_button, False, False, 0)
        
        content_area.pack_start(button_box, False, False, 20)
        
        self.connect("destroy", self.on_destroy)
        self.show_all()
    
    def on_close_clicked(self, button):
        self.destroy()
    
    def on_destroy(self, widget):
        if self.on_close_callback:
            self.on_close_callback()


class JadwalSholatPanel:
    """Kelas utama aplikasi jadwal sholat dengan system tray indicator."""
    
    def __init__(self):
        self.app_id = "jadwal_sholat_indicator"
        
        # Lokasi file
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.base_path, "../assets/jadwal.json")
        self.audio_file = os.path.join(self.base_path, "../assets/sound_adzan_alaqsa2_64_22.mp3")
        
        # Load data
        self.data_sholat = self.load_data()
        
        # Inisialisasi audio manager
        self.audio_manager = AudioManager(self.audio_file)
        
        # Inisialisasi prayer checker
        self.prayer_checker = PrayerTimeChecker(self.on_prayer_time)
        self.update_prayer_checker_schedule()
        self.prayer_checker.start()
        
        # Inisialisasi indicator
        self.indicator = AppIndicator.Indicator.new(
            self.app_id,
            "appointment-soon-symbolic", 
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        
        # Setup menu
        self.update_menu()
    
    def load_data(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File {self.json_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print("Error: Format JSON tidak valid.")
            return {}
    
    def get_today_data(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.data_sholat.get(today, None)
    
    def update_prayer_checker_schedule(self):
        today_data = self.get_today_data()
        
        if today_data:
            prayer_times = {
                "Subuh": today_data.get("subuh", ""),
                "Dzuhur": today_data.get("dzuhur", ""),
                "Ashar": today_data.get("ashar", ""),
                "Maghrib": today_data.get("maghrib", ""),
                "Isya": today_data.get("isya", "")
            }
            prayer_times = {k: v for k, v in prayer_times.items() if v}
            self.prayer_checker.set_prayer_times(prayer_times)
            print(f"Jadwal sholat hari ini diupdate: {prayer_times}")
    
    def on_prayer_time(self, prayer_name):
        print(f"Waktu sholat {prayer_name} telah tiba!")
        print(f"PYGAME_AVAILABLE: {PYGAME_AVAILABLE}")
        print(f"Audio file exists: {os.path.exists(self.audio_file)}")
        
        # Play audio
        play_result = self.audio_manager.play()
        print(f"Play result: {play_result}")
        print(f"Is audio playing: {self.audio_manager.is_busy()}")
        
        if play_result:
            print(f"✓ Memutar adzan untuk {prayer_name}")
        else:
            print(f"✗ Gagal memutar adzan untuk {prayer_name}")
        
        # Show notification dialog
        dialog = PrayerNotificationDialog(
            prayer_name,
            on_close_callback=self.on_notification_close
        )
        dialog.run()
    
    def on_notification_close(self):
        print("Notifikasi ditutup, menghentikan audio adzan")
        self.audio_manager.stop()
    
    def update_menu(self):
        menu = Gtk.Menu()
        today_data = self.get_today_data()
        
        if today_data:
            header = Gtk.MenuItem(label=f"📅 {today_data['tanggal']}")
            header.set_sensitive(False)
            menu.append(header)
            menu.append(Gtk.SeparatorMenuItem())

            for key in ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya']:
                label_text = f"{key.capitalize():<10} : {today_data.get(key, '-')}"
                item = Gtk.MenuItem(label=label_text)
                menu.append(item)
        else:
            menu.append(Gtk.MenuItem(label="⚠️ Data hari ini tidak ditemukan"))

        menu.append(Gtk.SeparatorMenuItem())
        
        item_refresh = Gtk.MenuItem(label="Refresh Data")
        item_refresh.connect('activate', lambda _: self.refresh())
        menu.append(item_refresh)
        
        item_test = Gtk.MenuItem(label="Test Notifikasi")
        item_test.connect('activate', lambda _: self.test_notification())
        menu.append(item_test)

        item_quit = Gtk.MenuItem(label="Keluar")
        item_quit.connect('activate', lambda _: self.quit())
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)
    
    def test_notification(self):
        print("Testing notifikasi dan audio...")
        self.on_prayer_time("Subuh (Test)")
    
    def refresh(self):
        self.data_sholat = self.load_data()
        self.update_prayer_checker_schedule()
        self.update_menu()
    
    def quit(self):
        print("Menutup aplikasi...")
        self.audio_manager.stop()
        self.prayer_checker.stop()
        Gtk.main_quit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = JadwalSholatPanel()
    Gtk.main()


if __name__ == "__main__":
    main()
