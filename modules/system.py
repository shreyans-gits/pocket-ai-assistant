import psutil

class SystemModule:
    def get_status(self) -> str:
        battery = psutil.sensors_battery()
        if battery:
            battery_percent = int(battery.percent)

            if battery.power_plugged:
                charging = "and charging"
            else:
                charging = "and not charging"
        else:
            battery_percent = "unknown"
            charging = ""

        cpu = psutil.cpu_percent(interval=1)

        memory = psutil.virtual_memory()
        ram = int(memory.percent)

        return (
            f"Battery is at {battery_percent}% {charging}. "
            f"CPU usage is {cpu}% and RAM usage is {ram}%."
        )