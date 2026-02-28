const fs = require('fs');
const path = require('path');

let prayerData = {};
let metadata = {};
let checkInterval = null;
let lastTriggered = {};

function loadPrayerData() {
    const isDev = !require('electron').app.isPackaged;
    const jsonPath = isDev 
        ? path.join(__dirname, '../../../assets/jadwal_imsakiyah.json')
        : path.join(process.resourcesPath, 'assets/jadwal_imsakiyah.json');
    
    try {
        const data = fs.readFileSync(jsonPath, 'utf8');
        const parsed = JSON.parse(data);
        
        // Store metadata
        metadata = {
            title: parsed.title || '',
            location: parsed.location || '',
            organization: parsed.organization || '',
            calculated_by: parsed.calculated_by || ''
        };
        
        // Convert array format to date-keyed object
        prayerData = {};
        if (parsed.schedule && Array.isArray(parsed.schedule)) {
            parsed.schedule.forEach(item => {
                const dateStr = item.calendar_date;
                const date = parseDateString(dateStr);
                if (date) {
                    prayerData[date] = {
                        tanggal: item.calendar_date,
                        imsak: item.imsak,
                        subuh: item.subuh,
                        terbit: item.terbit,
                        dhuha: item.duha,
                        dzuhur: item.zuhur,
                        ashar: item.ashar,
                        maghrib: item.maghrib,
                        isya: item.isya
                    };
                }
            });
        }
        
        return getTodayData();
    } catch (error) {
        console.error('Error loading prayer data:', error);
        return null;
    }
}

function parseDateString(dateStr) {
    // Convert "18 Februari 2026" to "2026-02-18"
    const months = {
        'Januari': '01', 'Februari': '02', 'Maret': '03', 'April': '04',
        'Mei': '05', 'Juni': '06', 'Juli': '07', 'Agustus': '08',
        'September': '09', 'Oktober': '10', 'November': '11', 'Desember': '12'
    };
    
    const parts = dateStr.split(' ');
    if (parts.length === 3) {
        const day = parts[0].padStart(2, '0');
        const month = months[parts[1]];
        const year = parts[2];
        if (month) {
            return `${year}-${month}-${day}`;
        }
    }
    return null;
}

function getTodayData() {
    const today = new Date().toISOString().split('T')[0];
    return prayerData[today] || null;
}

function getNextPrayer(todayData) {
    if (!todayData) return null;
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const prayers = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    
    for (const prayer of prayers) {
        if (todayData[prayer] && todayData[prayer] > currentTime) {
            const [hour, minute] = todayData[prayer].split(':').map(Number);
            const prayerTime = new Date();
            prayerTime.setHours(hour, minute, 0, 0);
            
            const diff = prayerTime - now;
            const minutes = Math.floor(diff / 60000);
            
            return { name: prayer, minutes, time: todayData[prayer] };
        }
    }
    
    return null;
}

function checkPrayerTime(mainWindow) {
    const todayData = getTodayData();
    if (!todayData) return;
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const currentDate = now.toISOString().split('T')[0];
    
    const prayers = ['subuh', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    
    for (const prayer of prayers) {
        if (todayData[prayer] === currentTime && lastTriggered[prayer] !== currentDate) {
            lastTriggered[prayer] = currentDate;
            
            if (mainWindow) {
                mainWindow.webContents.send('prayer-time', { 
                    name: prayer.charAt(0).toUpperCase() + prayer.slice(1),
                    time: currentTime 
                });
            }
            
            playAdzan();
            break;
        }
    }
}

function playAdzan() {
    const isDev = !require('electron').app.isPackaged;
    const adzanPath = isDev
        ? path.join(__dirname, '../../../assets/sound_adzan_alaqsa2_64_22.mp3')
        : path.join(process.resourcesPath, 'assets/sound_adzan_alaqsa2_64_22.mp3');
    
    if (fs.existsSync(adzanPath)) {
        const { exec } = require('child_process');
        exec(`mpg123 -q "${adzanPath}"`, (error) => {
            if (error) console.error('Error playing adzan:', error);
        });
    }
}

function startPrayerChecker(mainWindow) {
    if (checkInterval) clearInterval(checkInterval);
    
    checkInterval = setInterval(() => {
        checkPrayerTime(mainWindow);
    }, 30000); // Check every 30 seconds
}

function stopPrayerChecker() {
    if (checkInterval) {
        clearInterval(checkInterval);
        checkInterval = null;
    }
}

module.exports = {
    loadPrayerData,
    getTodayData,
    getNextPrayer,
    getMetadata: () => metadata,
    startPrayerChecker,
    stopPrayerChecker,
};
