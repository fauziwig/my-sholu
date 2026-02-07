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

    def __init__(self, callback, reminder_callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.reminder_callback = reminder_callback
        self.prayer_times = {}
        self.prayer_datetimes = {}
        self.running = False
        self.last_triggered = {}
        self.reminder_20_triggered = {}
        self.reminder_10_triggered = {}
        self.reminder_64_triggered = {}
        self.lock = threading.Lock()

    def set_prayer_times(self, prayer_dict, prayer_datetimes=None):
        with self.lock:
            self.prayer_times = prayer_dict.copy()
            if prayer_datetimes:
                self.prayer_datetimes = prayer_datetimes.copy()

    def run(self):
        self.running = True

        while self.running:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%Y-%m-%d")

            with self.lock:
                for prayer_name, prayer_time in self.prayer_times.items():
                    if (current_time == prayer_time and
                        self.last_triggered.get(prayer_name) != current_date):

                        self.last_triggered[prayer_name] = current_date
                        GLib.idle_add(self.callback, prayer_name)
                        break

                for prayer_name, prayer_datetime in self.prayer_datetimes.items():
                    if prayer_datetime <= now:
                        continue

                    time_diff = prayer_datetime - now
                    minutes_until = int(time_diff.total_seconds() // 60)

                    if minutes_until == 20:
                        reminder_key = f"{prayer_name}_20"
                        if self.reminder_20_triggered.get(reminder_key) != current_date:
                            self.reminder_20_triggered[reminder_key] = current_date
                            GLib.idle_add(self.reminder_callback, prayer_name, 20)

                    elif minutes_until == 10:
                        reminder_key = f"{prayer_name}_10"
                        if self.reminder_10_triggered.get(reminder_key) != current_date:
                            self.reminder_10_triggered[reminder_key] = current_date
                            GLib.idle_add(self.reminder_callback, prayer_name, 10)
                    
                    elif minutes_until == 60:
                        reminder_key = f"{prayer_name}_60"
                        if self.reminder_64_triggered.get(reminder_key) != current_date:
                            self.reminder_64_triggered[reminder_key] = current_date
                            GLib.idle_add(self.reminder_callback, prayer_name, 64)

            time.sleep(30)

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


class ReminderNotificationDialog(Gtk.Dialog):
    """Dialog popup untuk pengingat waktu sholat (10 & 20 menit sebelum)."""

    def __init__(self, prayer_name, minutes_before):
        super().__init__(
            title="Pengingat Waktu Sholat",
            parent=None,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
        )

        self.prayer_name = prayer_name
        self.minutes_before = minutes_before

        self.set_default_size(350, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)

        content_area = self.get_content_area()
        content_area.set_spacing(10)

        # Icon
        icon_label = Gtk.Label()
        icon_label.set_markup("<span size='xx-large'>⏰</span>")
        icon_label.set_alignment(0.5, 0.5)
        content_area.pack_start(icon_label, False, False, 10)

        # Title
        title_label = Gtk.Label()
        title_label.set_markup(
            f"<span size='large' weight='bold'>Pengingat Sholat {prayer_name}</span>"
        )
        title_label.set_alignment(0.5, 0.5)
        content_area.pack_start(title_label, False, False, 5)

        # Message
        msg_label = Gtk.Label()
        msg_label.set_markup(
            f"<span size='medium'>{minutes_before} menit lagi menuju waktu sholat {prayer_name}.</span>\n"
            f"<span size='small'>Siap-siap untuk sholat.</span>"
        )
        msg_label.set_alignment(0.5, 0.5)
        content_area.pack_start(msg_label, False, False, 10)

        # Button
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)

        close_button = Gtk.Button(label="OK")
        close_button.set_size_request(100, 35)
        close_button.connect("clicked", lambda _: self.destroy())
        button_box.pack_start(close_button, False, False, 0)

        content_area.pack_start(button_box, False, False, 15)

        self.show_all()


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
        self.prayer_times = {}
        
        # Inisialisasi audio manager
        self.audio_manager = AudioManager(self.audio_file)
        
        # Inisialisasi prayer checker
        self.prayer_checker = PrayerTimeChecker(self.on_prayer_time, self.on_reminder)
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
        
        # Start countdown update timer
        GLib.timeout_add_seconds(60, self.update_countdown)
    
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
            self.prayer_times = prayer_times

            now = datetime.datetime.now()
            prayer_datetimes = {}
            for prayer_name, prayer_time in prayer_times.items():
                try:
                    prayer_hour, prayer_minute = map(int, prayer_time.split(':'))
                    prayer_datetime = now.replace(hour=prayer_hour, minute=prayer_minute, second=0, microsecond=0)
                    prayer_datetimes[prayer_name] = prayer_datetime
                except (ValueError, AttributeError):
                    continue

            self.prayer_checker.set_prayer_times(prayer_times, prayer_datetimes)
            print(f"Jadwal sholat hari ini diupdate: {prayer_times}")
    
    def get_time_until_next_prayer(self):
        """Hitung selisih waktu ke sholat berikutnya.
        
        Returns:
            tuple: (prayer_name, minutes) atau (None, None) jika tidak ada
        """
        if not hasattr(self, 'prayer_times') or not self.prayer_times:
            return None, None
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Daftar waktu sholat dalam urutan
        prayer_order = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya']
        today_data = self.get_today_data()
        
        if not today_data:
            return None, None
        
        # Cari waktu sholat berikutnya
        for prayer_key in prayer_order:
            if prayer_key in today_data:
                prayer_time = today_data[prayer_key]
                if prayer_time > current_time:
                    # Hitung selisih
                    prayer_hour, prayer_minute = map(int, prayer_time.split(':'))
                    prayer_datetime = now.replace(hour=prayer_hour, minute=prayer_minute, second=0)
                    
                    if prayer_datetime > now:
                        diff = prayer_datetime - now
                        minutes = int(diff.total_seconds() // 60)
                        return prayer_key.capitalize(), minutes
        
        return None, None
    
    def format_countdown(self, prayer_name, minutes):
        """Format teks countdown.
        
        Args:
            prayer_name: Nama waktu sholat
            minutes: Jumlah menit
            
        Returns:
            str: Teks countdown yang diformat
        """
        if minutes < 60:
            return f"⏰ {prayer_name} dalam {minutes} menit"
        else:
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"⏰ {prayer_name} dalam {hours} jam"
            else:
                return f"⏰ {prayer_name} dalam {hours} jam {mins} menit"
    
    def update_countdown(self):
        """Update countdown setiap 60 detik."""
        prayer_name, minutes = self.get_time_until_next_prayer()
        
        if prayer_name and minutes is not None:
            print(f"Countdown: {prayer_name} dalam {minutes} menit")
        
        # Update menu untuk menampilkan countdown terbaru
        self.update_menu()
        
        # Schedule update lagi setelah 60 detik
        GLib.timeout_add_seconds(60, self.update_countdown)
        return False
    
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

    def on_reminder(self, prayer_name, minutes_before):
        print(f"Pengingat: {minutes_before} menit lagi menuju waktu sholat {prayer_name}")
        dialog = ReminderNotificationDialog(prayer_name, minutes_before)
        dialog.run()
    
    def update_menu(self):
        menu = Gtk.Menu()
        today_data = self.get_today_data()
        
        if today_data:
            header = Gtk.MenuItem(label=f"📅 {today_data['tanggal']}")
            header.set_sensitive(False)
            menu.append(header)
            
            # Tambahkan countdown ke sholat berikutnya
            prayer_name, minutes = self.get_time_until_next_prayer()
            if prayer_name and minutes is not None:
                countdown_text = self.format_countdown(prayer_name, minutes)
                countdown_item = Gtk.MenuItem(label=countdown_text)
                countdown_item.set_sensitive(False)
                menu.append(countdown_item)
            
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
