const { ipcMain } = require('electron');

class RefreshController {
  static readonly groupName = 'refresh';

  refreshData() {
    return { success: true };
  }
}

module.exports = RefreshController;
