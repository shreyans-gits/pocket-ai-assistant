from threading import Timer
from plyer import notification

class ReminderModule:
    def notify(self, message : str):
        notification.notify(
            title = "ZORO",
            message = message
        )

    def set_reminder(self, message : str, minutes : int) -> str:
        timer = Timer(
            minutes*60,
            self.notify,
            args = [message]
        )

        timer.start()
        return f"Reminder set for {minutes} minutes from now."