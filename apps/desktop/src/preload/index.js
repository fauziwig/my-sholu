const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  loadPrayerData: () => ipcRenderer.invoke('load-prayer-data'),
  showNotification: (title, body) => ipcRenderer.invoke('show-notification', { title, body }),
  refreshData: () => ipcRenderer.invoke('refresh-data'),
  onRefreshData: (callback) => ipcRenderer.on('refresh-data', callback),
  onPrayerTime: (callback) => ipcRenderer.on('prayer-time', (event, data) => callback(data)),
  getAutoLocation: () => ipcRenderer.invoke('get-auto-location'),
});
