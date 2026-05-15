const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain, Notification, powerMonitor } = require('electron');
const path = require('path');
const fs = require('fs');
const prayerService = require('./prayerService');
const { showCustomNotification, setAdzanProcess } = require('./customNotification');

let mainWindow = null;
let tray = null;

const isDev = process.env.NODE_ENV === 'development';

function createMainWindow() {
  const isDev = !app.isPackaged;
  const iconPath = isDev
    ? path.join(__dirname, '../../../apps/assets/icon.png')
    : path.join(process.resourcesPath, 'assets/icon.png');
  
  mainWindow = new BrowserWindow({
    width: 450,
    height: 600,
    minWidth: 400,
    minHeight: 400,
    icon: iconPath,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    backgroundColor: '#f5f5f5',
    show: false,
  });

  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));

  mainWindow.on('close', (event) => {
    event.preventDefault();
    mainWindow.hide();
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  return mainWindow;
}

function createTray() {
  const isDev = !app.isPackaged;
  const iconPath = isDev
    ? path.join(__dirname, '../../../apps/assets/icon-tray.png')
    : path.join(process.resourcesPath, 'assets/icon-tray.png');
  
  let icon;
  if (fs.existsSync(iconPath)) {
    icon = nativeImage.createFromPath(iconPath);
  } else {
    icon = nativeImage.createEmpty();
  }
  
  tray = new Tray(icon);
  tray.setToolTip('MySholu - Jadwal Sholat');

  updateTrayMenu();

  tray.on('click', () => {
    if (!mainWindow) {
      mainWindow = createMainWindow();
    } else if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
      mainWindow.focus();
    }
  });

  return tray;
}

function updateTrayMenu() {
  const todayData = prayerService.getTodayData();
  const nextPrayer = prayerService.getNextPrayer(todayData);
  
  const menuTemplate = [
    {
      label: todayData ? `📅 ${todayData.tanggal}` : '📅 Data tidak tersedia',
      enabled: false,
    },
  ];

  if (nextPrayer) {
    menuTemplate.push({
      label: `⏰ ${nextPrayer.name.charAt(0).toUpperCase() + nextPrayer.name.slice(1)} dalam ${nextPrayer.minutes} menit`,
      enabled: false,
    });
  }

  menuTemplate.push({ type: 'separator' });

  if (todayData) {
    const prayers = ['imsak', 'subuh', 'terbit', 'dhuha', 'dzuhur', 'ashar', 'maghrib', 'isya'];
    prayers.forEach(prayer => {
      if (todayData[prayer]) {
        menuTemplate.push({
          label: `${prayer.charAt(0).toUpperCase() + prayer.slice(1)}: ${todayData[prayer]}`,
          enabled: false,
        });
      }
    });
  }

  menuTemplate.push(
    { type: 'separator' },
    {
      label: 'Show Window',
      click: () => {
        if (!mainWindow) {
          mainWindow = createMainWindow();
        } else {
          mainWindow.show();
          mainWindow.focus();
        }
      },
    },
    {
      label: 'Refresh Data',
      click: async () => {
        await prayerService.loadPrayerData();
        updateTrayMenu();
        if (mainWindow) {
          mainWindow.webContents.send('refresh-data');
        }
      },
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.isQuitting = true;
        if (tray) {
          tray.destroy();
        }
        app.quit();
      },
    }
  );

  const contextMenu = Menu.buildFromTemplate(menuTemplate);
  tray.setContextMenu(contextMenu);
}

ipcMain.handle('show-notification', async (event, { title, body }) => {
  showCustomNotification(title, body);
  
  const adzanPath = !app.isPackaged
    ? path.join(__dirname, '../../../../apps/assets/sound_adzan_alaqsa2_64_22.mp3')
    : path.join(process.resourcesPath, 'assets/sound_adzan_alaqsa2_64_22.mp3');
  
  if (fs.existsSync(adzanPath)) {
    const { spawn } = require('child_process');
    const process = spawn('mpg123', ['-q', adzanPath]);
    setAdzanProcess(process);
    
    process.on('error', (error) => {
      console.error('[Notification] Error playing adzan:', error);
    });
  }
  
  return { success: true };
});

ipcMain.handle('refresh-data', async () => {
  await prayerService.loadPrayerData();
  updateTrayMenu();
  return { success: true };
});

ipcMain.handle('get-auto-location', async () => {
  try {
    // Reuse data already fetched by prayerService
    let location = prayerService.getLocationData();
    let schedule = prayerService.getTodayData();

    if (!location || !schedule) {
      const result = await prayerService.loadPrayerData();
      if (!result) throw new Error('Gagal mengambil data jadwal sholat');
      location = result.location;
      schedule = result.schedule;
    }

    return { success: true, data: { location, schedule } };
  } catch (error) {
    return { success: false, message: error.message };
  }
});

app.on('ready', async () => {
  createMainWindow();
  createTray();
  await prayerService.loadPrayerData();
  updateTrayMenu();
  
  const notifyPrayer = (prayerName, time) => {
    showCustomNotification(
      `Waktu Sholat ${prayerName}`,
      `Telah masuk waktu sholat ${prayerName} pada ${time}`
    );
    
    const adzanPath = !app.isPackaged
      ? path.join(__dirname, '../../../../apps/assets/sound_adzan_alaqsa2_64_22.mp3')
      : path.join(process.resourcesPath, 'assets/sound_adzan_alaqsa2_64_22.mp3');
    
    if (fs.existsSync(adzanPath)) {
      const { spawn } = require('child_process');
      const process = spawn('mpg123', ['-q', adzanPath]);
      setAdzanProcess(process);
    }
  };
  
  prayerService.startPrayerChecker(notifyPrayer);
  
  powerMonitor.on('resume', async () => {
    console.log('[PowerMonitor] Laptop woke up, refreshing prayer data...');
    await prayerService.loadPrayerData();
    updateTrayMenu();
  });
  
  powerMonitor.on('suspend', () => {
    console.log('[PowerMonitor] Laptop going to sleep...');
  });
  
  setInterval(() => {
    updateTrayMenu();
  }, 60000);
});

app.on('window-all-closed', () => {
  // Keep app running in tray
});

app.on('activate', () => {
  if (mainWindow === null) {
    createMainWindow();
  }
});

app.on('before-quit', () => {
  prayerService.stopPrayerChecker();
  if (tray) {
    tray.destroy();
  }
});

module.exports = {
  createMainWindow,
  createTray,
  getMainWindow: () => mainWindow,
  getTray: () => tray,
};
