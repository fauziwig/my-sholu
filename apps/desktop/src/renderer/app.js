let prayerData = null;
let metadata = null;
let checkInterval = null;

async function loadData() {
    try {
        const response = await window.electronAPI.loadPrayerData();
        prayerData = response.todayData;
        metadata = response.metadata;
        updateSystemDate();
        updateCurrentLocation();
        updateUI();
        updateMetadata();
        startCountdown();
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
        const loc = result.data;
        document.getElementById('currentLocation').textContent = `📍 ${loc.city}, ${loc.region}`;
    } else {
        document.getElementById('currentLocation').textContent = '📍 Lokasi tidak terdeteksi';
    }
}

function getTodayData() {
    return prayerData;
}

function updateUI() {
    if (!prayerData) {
        document.getElementById('date').textContent = 'Data tidak tersedia untuk hari ini';
        return;
    }
    
    document.getElementById('date').textContent = '';
    
    const prayers = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    const items = document.querySelectorAll('.prayer-item');
    
    prayers.forEach((prayer, index) => {
        if (items[index]) {
            const timeEl = items[index].querySelector('.prayer-time');
            timeEl.textContent = prayerData[prayer] || '--:--';
        }
    });
}

function updateMetadata() {
    if (!metadata) return;
    
    const content = `
        <div><strong>${metadata.title}</strong></div>
        <div>📍 ${metadata.location}</div>
        <div>🏢 ${metadata.organization}</div>
        <div>👤 ${metadata.calculated_by}</div>
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

function showPrayerNotification(name, time) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
        text-align: center;
        min-width: 300px;
    `;
    
    notification.innerHTML = `
        <div style="font-size: 48px; margin-bottom: 15px;">🕌</div>
        <h2 style="margin: 0 0 10px 0; color: #2c3e50;">Waktu Sholat ${name}</h2>
        <p style="margin: 0 0 20px 0; color: #7f8c8d;">Telah masuk waktu sholat ${name}<br>Waktu: ${time}</p>
        <button onclick="this.parentElement.remove()" style="
            padding: 10px 30px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        ">Tutup</button>
    `;
    
    document.body.appendChild(notification);
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
