const { fetchLocationData, fetchPrayerSchedule } = require('./locationService');

let prayerData = null;
let locationData = null;
let checkInterval = null;
let lastTriggered = {};

async function loadPrayerData() {
  try {
    const location = await fetchLocationData();
    locationData = location;
    prayerData = await fetchPrayerSchedule(location.city, location.timezone);
    console.log('[loadPrayerData] Loaded from myquran:', prayerData.kota);
    console.log('time: ',prayerData)
    return { location: locationData, schedule: prayerData };
  } catch (error) {
    console.error('Error loading prayer data:', error);
    return null;
  }
}

function getLocationData() {
  return locationData;
}

function getTodayData() {
  return prayerData;
}

function getMetadata() {
  return {
    title: 'Jadwal Sholat Hari Ini',
    location: prayerData ? prayerData.kota : '',
    organization: '',
    calculated_by: 'api.myquran.com',
  };
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

function checkPrayerTime(notifyCallback) {
  if (!prayerData) return;

  const now = new Date();
  const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  const currentDate = now.toISOString().split('T')[0];

  const prayers = ['subuh', 'dzuhur', 'ashar', 'maghrib', 'isya'];

  for (const prayer of prayers) {
    if (prayerData[prayer] === currentTime && lastTriggered[prayer] !== currentDate) {
      lastTriggered[prayer] = currentDate;
      if (notifyCallback) {
        notifyCallback(prayer.charAt(0).toUpperCase() + prayer.slice(1), currentTime);
      }
      break;
    }
  }
}

function startPrayerChecker(notifyCallback) {
  if (checkInterval) clearInterval(checkInterval);
  checkInterval = setInterval(() => {
    checkPrayerTime(notifyCallback);
  }, 30000);
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
  getLocationData,
  getNextPrayer,
  getMetadata,
  startPrayerChecker,
  stopPrayerChecker,
};
