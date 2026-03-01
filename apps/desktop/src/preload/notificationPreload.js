const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('notificationAPI', {
  closeWindow: () => window.close(),
});
