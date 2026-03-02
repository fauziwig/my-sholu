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
        
        console.log('[loadPrayerData] Total dates loaded:', Object.keys(prayerData).length);
        console.log('[loadPrayerData] Sample dates:', Object.keys(prayerData).slice(0, 3));
        console.log('[loadPrayerData] Last dates:', Object.keys(prayerData).slice(-3));
        
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
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const today = `${year}-${month}-${day}`;
    
    console.log('System - Local : ',today, '- Type : ', (typeof today));
    console.log('prayerData : ',prayerData[today]);
    console.log('formattedData : ',today);
    console.log('path : ', String(path.join(__dirname, '../../../assets/sound_adzan_alaqsa2_64_22.mp3')));
    
    const mypath = path.join(__dirname, '../../../assets/sound_adzan_alaqsa2_64_22.mp3');
    console.log('typeof path : ',typeof(mypath));

        
    const result = prayerData[today] || null;
    console.log('[Result] Found data:', result ? 'YES' : 'NO');
    if (result) console.log('[Result] Data:', result);
    console.log('========================');
    
    return result;
}


function getIniCobaPath(){
    const mypath = path.join(__dirname, '../../../assets/sound_adzan_alaqsa2_64_22.mp3');
    console.log('typeof path : ',typeof(mypath));
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

function checkPrayerTime(notificationCallback) {
    const todayData = getTodayData();
    if (!todayData) {
        console.log('[checkPrayerTime] No data for today');
        return;
    }
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const currentDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    
    console.log(`[checkPrayerTime] Current time: ${currentTime}, Date: ${currentDate}`);
    
    const prayers = ['imsak', 'subuh', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    
    for (const prayer of prayers) {
        const prayerTime = todayData[prayer];
        console.log(`[checkPrayerTime] ${prayer}: ${prayerTime}, Match: ${prayerTime === currentTime}, Already triggered: ${lastTriggered[prayer] === currentDate}`);
        
        if (prayerTime === currentTime && lastTriggered[prayer] !== currentDate) {
            lastTriggered[prayer] = currentDate;
            
            console.log(`[Prayer Time] ✅ TRIGGERED: ${prayer} at ${currentTime}`);
            
            // Call notification callback
            if (notificationCallback) {
                notificationCallback(prayer.charAt(0).toUpperCase() + prayer.slice(1), currentTime);
            } else {
                console.error('[Prayer Time] ❌ No notification callback!');
            }
            
            break;
        }
    }
}

function playAdzan() {
    // Removed - adzan is now played by notification handler
}

function startPrayerChecker(notificationCallback) {
    if (checkInterval) clearInterval(checkInterval);
    
    checkInterval = setInterval(() => {
        checkPrayerTime(notificationCallback);
    }, 30000); // Check every 30 seconds
}

function stopPrayerChecker() {
    if (checkInterval) {
        clearInterval(checkInterval);
        checkInterval = null;
    }
}

function checkMissedPrayers(notificationCallback) {
    const todayData = getTodayData();
    if (!todayData) return;
    
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const currentDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    
    const prayers = ['imsak', 'subuh', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    
    console.log('[checkMissedPrayers] Checking for missed prayers after wake...');
    
    for (const prayer of prayers) {
        const prayerTime = todayData[prayer];
        if (!prayerTime) continue;
        
        // Check if prayer time has passed and not yet triggered today
        if (prayerTime < currentTime && lastTriggered[prayer] !== currentDate) {
            console.log(`[checkMissedPrayers] Found missed prayer: ${prayer} at ${prayerTime}`);
            lastTriggered[prayer] = currentDate;
            
            if (notificationCallback) {
                notificationCallback(
                    prayer.charAt(0).toUpperCase() + prayer.slice(1), 
                    prayerTime
                );
            }
            
            // Only notify the most recent missed prayer
            break;
        }
    }
}

module.exports = {
    loadPrayerData,
    getTodayData,
    getNextPrayer,
    getMetadata: () => metadata,
    startPrayerChecker,
    stopPrayerChecker,
    checkMissedPrayers,
};
