const fs = require('fs');
const path = require('path');

/**
 * Membaca dan parsing file JSON
 * @param {string} filePath - Path ke file JSON
 * @returns {Promise<Object>} Data JSON yang sudah diparsing
 */
async function loadJsonFile(filePath) {
  try {
    const data = await fs.promises.readFile(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error loading JSON file ${filePath}:`, error);
    throw error;
  }
}

/**
 * Menyimpan data ke file JSON
 * @param {string} filePath - Path file tujuan
 * @param {Object} data - Data yang akan disimpan
 */
async function saveJsonFile(filePath, data) {
  try {
    await fs.promises.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
  } catch (error) {
    console.error(`Error saving JSON file ${filePath}:`, error);
    throw error;
  }
}

/**
 * Mengambil data JSON dari URL
 * @param {string} url - URL API endpoint
 * @returns {Promise<Object>} Data JSON dari API
 */
async function fetchJsonData(url) {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching JSON from ${url}:`, error);
    throw error;
  }
}

module.exports = {
  loadJsonFile,
  saveJsonFile,
  fetchJsonData
};
