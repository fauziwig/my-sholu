const { BrowserWindow } = require('electron');
const path = require('path');

let notificationWindow = null;
let adzanProcess = null;

function showCustomNotification(title, body) {
  if (notificationWindow) {
    notificationWindow.close();
  }

  notificationWindow = new BrowserWindow({
    width: 400,
    height: 150,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, '../preload/notificationPreload.js'),
    },
  });

  // Position at top-right
  const { screen } = require('electron');
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  notificationWindow.setPosition(width - 420, 20);

  notificationWindow.loadFile(path.join(__dirname, '../renderer/notification.html'));
  
  notificationWindow.webContents.on('did-finish-load', () => {
    notificationWindow.webContents.send('notification-data', { title, body });
  });

  notificationWindow.on('closed', () => {
    stopAdzan();
    notificationWindow = null;
  });

  // No auto-close - user must click Tutup button
}

function setAdzanProcess(process) {
  adzanProcess = process;
}

function stopAdzan() {
  if (adzanProcess) {
    adzanProcess.kill();
    adzanProcess = null;
  }
}

module.exports = { showCustomNotification, setAdzanProcess, stopAdzan };
