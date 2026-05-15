/**
 * Mengambil data lokasi (city & timezone) berdasarkan IP publik
 */
async function fetchLocationData() {
  const response = await fetch('https://ipinfo.io/json');
  if (!response.ok) throw new Error(`ipinfo error: ${response.status}`);
  const data = await response.json();
  return {
    city: data.city,
    region: data.region,
    timezone: data.timezone,
  };
}

/**
 * Mengambil jadwal sholat hari ini dari api.myquran.com berdasarkan kota
 */
async function fetchPrayerSchedule(city, timezone) {
  // Step 1: Cari ID kota
  const searchRes = await fetch(`https://api.myquran.com/v3/sholat/kabkota/cari/${encodeURIComponent(city)}`);
  if (!searchRes.ok) throw new Error(`myquran search error: ${searchRes.status}`);
  const searchData = await searchRes.json();

  if (!searchData.status || !searchData.data || searchData.data.length === 0) {
    throw new Error(`Kota "${city}" tidak ditemukan di myquran`);
  }

  const kotaId = searchData.data[0].id;
  const kotaName = searchData.data[0].lokasi;

  // Step 2: Ambil jadwal hari ini
  const tz = encodeURIComponent(timezone);
  const scheduleRes = await fetch(`https://api.myquran.com/v3/sholat/jadwal/${kotaId}/today?tz=${tz}`);
  if (!scheduleRes.ok) throw new Error(`myquran jadwal error: ${scheduleRes.status}`);
  const scheduleData = await scheduleRes.json();

  if (!scheduleData.status || !scheduleData.data || !scheduleData.data.jadwal) {
    throw new Error('Jadwal tidak tersedia');
  }

  // jadwal is keyed by date string e.g. "2026-05-15"
  const jadwalObj = scheduleData.data.jadwal;
  const todayKey = Object.keys(jadwalObj)[0];
  const jadwal = jadwalObj[todayKey];

  return {
    kota: kotaName,
    provinsi: scheduleData.data.prov || '',
    tanggal: jadwal.tanggal,
    imsak: jadwal.imsak,
    subuh: jadwal.subuh,
    terbit: jadwal.terbit,
    dhuha: jadwal.dhuha,
    dzuhur: jadwal.dzuhur,
    ashar: jadwal.ashar,
    maghrib: jadwal.maghrib,
    isya: jadwal.isya,
  };
}

module.exports = { fetchLocationData, fetchPrayerSchedule };
