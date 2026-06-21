from jnius import autoclass

class AlarmModule:
    def set_alarm(self, hour: int ,minute: int ,label: str = "ZORO Alarm") -> str:
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            AlarmClock = autoclass("android.provider.AlarmClock")
            Intent = autoclass("android.content.Intent")
            intent = Intent(AlarmClock.ACTION_SET_ALARM)
            intent.putExtra(AlarmClock.EXTRA_HOUR, hour)
            intent.putExtra(AlarmClock.EXTRA_MINUTES, minute)
            intent.putExtra(AlarmClock.EXTRA_MESSAGE, label)
            activity.startActivity(intent)
            formatted_time = f"{hour:02d}:{minute:02d}"
            return f"Alarm set for {formatted_time}."

        except Exception as e:
            print("Alarm Error:", e)
            return "Unable to set alarm."