let prayerData = null;
let checkInterval = null;

async function loadData() {
    try {
        updateSystemDate();
        await updateCurrentLocation();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateSystemDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateStr = now.toLocaleDateString('id-ID', options);
    document.getElementById('systemDate').textContent = dateStr;
}

async function updateCurrentLocation() {
    const result = await window.electronAPI.getAutoLocation();
    
    if (result.success) {
        const { location, schedule } = result.data;
        document.getElementById('currentLocation').textContent = `📍 ${location.city}, ${location.region}`;
        prayerData = schedule;
        updateUI();
        updateMetadata(schedule);
        startCountdown();
    } else {
        document.getElementById('currentLocation').textContent = '📍 Lokasi tidak terdeteksi';
    }
}

function updateUI() {
    if (!prayerData) {
        document.getElementById('countdown').textContent = '⏰ Data tidak tersedia';
        return;
    }

    const prayers = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    const items = document.querySelectorAll('.prayer-item');

    prayers.forEach((prayer, index) => {
        if (items[index]) {
            const timeEl = items[index].querySelector('.prayer-time');
            timeEl.textContent = prayerData[prayer] || '--:--';
        }
    });
}

function updateMetadata(schedule) {
    if (!schedule) return;

    const content = `
        <div><strong>${schedule.tanggal}</strong></div>
        <div>📍 ${schedule.kota}, ${schedule.provinsi}</div>
        <div>👤 api.myquran.com</div>
    `;

    document.getElementById('metadataContent').innerHTML = content;
}

function updateCountdown() {
    if (!prayerData) return;
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const prayers = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    
    for (const prayer of prayers) {
        if (prayerData[prayer] && prayerData[prayer] > currentTime) {
            const [hour, minute] = prayerData[prayer].split(':').map(Number);
            const prayerTime = new Date();
            prayerTime.setHours(hour, minute, 0, 0);
            
            const diff = prayerTime - now;
            const minutes = Math.floor(diff / 60000);
            
            const countdownEl = document.getElementById('countdown');
            if (minutes < 60) {
                countdownEl.textContent = `⏰ ${prayer.charAt(0).toUpperCase() + prayer.slice(1)} dalam ${minutes} menit`;
            } else {
                const hours = Math.floor(minutes / 60);
                const mins = minutes % 60;
                countdownEl.textContent = `⏰ ${prayer.charAt(0).toUpperCase() + prayer.slice(1)} dalam ${hours} jam ${mins} menit`;
            }
            return;
        }
    }
    
    document.getElementById('countdown').textContent = '⏰ Tidak ada waktu sholat tersisa hari ini';
}

function startCountdown() {
    updateCountdown();
    if (checkInterval) clearInterval(checkInterval);
    checkInterval = setInterval(updateCountdown, 60000);
}

function refreshData() {
    loadData();
}

function testNotification() {
    window.electronAPI.showNotification('Test Notifikasi', 'Ini adalah test notifikasi dari MySholu');
}

window.electronAPI.onRefreshData(() => {
    refreshData();
});

window.electronAPI.onPrayerTime((data) => {
    // Only system notification, no in-app popup
});

window.addEventListener('DOMContentLoaded', () => {
    loadData();
});
