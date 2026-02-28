const { ipcMain, Notification } = require('electron');

class NotificationController {
  static readonly groupName = 'notification';

  @IpcMethod()
  async showNotification(params) {
    const { title, body } = params;

    if (!Notification.isSupported()) {
      return { success: false, error: 'Notifications not supported' };
    }

    try {
      const notification = new Notification({ title, body });
      notification.show();
      return { success: true };
    } catch (error) {
      console.error('[NotificationController] Failed:', error);
      return { success: false, error: error.message };
    }
  }
}

module.exports = NotificationController;
