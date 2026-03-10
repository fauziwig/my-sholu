/**
 * Mengambil data lokasi berdasarkan IP publik
 * @returns {Promise<Object>} Data lokasi dari ipinfo.io
 */
async function fetchLocationData() {
  try {
    const response = await fetch('https://ipinfo.io/json');
    
    if (!response.ok) {
      throw new Error(`Gagal mengambil data: ${response.status}`);
    }

    const data = await response.json();
    
    // Tips: Koordinat di ipinfo berupa string "lat,long"
    // Kita bisa split jika dibutuhkan untuk library jadwal salat
    const [latitude, longitude] = data.loc.split(',');

    return {
      city: data.city,
      region: data.region,
      country: data.country,
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      timezone: data.timezone
    };
  } catch (error) {
    console.error("Location Service Error:", error);
    throw error;
  }
}

module.exports = { fetchLocationData };
