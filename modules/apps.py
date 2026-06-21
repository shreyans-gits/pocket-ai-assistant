from jnius import autoclass

class AppsModule:
    def __init__(self):
        self.apps = self.get_installed_apps()

    def get_installed_apps(self):
        apps = {}
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            Intent = autoclass("android.content.Intent")
            intent = Intent(
                Intent.ACTION_MAIN,
                None
            )

            intent.addCategory(
                Intent.CATEGORY_LAUNCHER
            )

            resolve_infos = pm.queryIntentActivities(
                intent,
                0
            )

            for info in resolve_infos:
                label = str(
                    info.loadLabel(pm)
                )
                package = str(
                    info.activityInfo.packageName
                )
                apps[label.lower()] = package

        except Exception as e:
            print("App loading error:", e)
        return apps

    def open_app(self, name: str) -> str:
        name = name.lower().strip()
        if not self.apps:
            return "I couldn't load installed apps."

        try:
            matched_package = None
            matched_name = None
            for app_name, package in self.apps.items():
                if name in app_name:
                    matched_package = package
                    matched_name = app_name
                    break

            if not matched_package:
                return f"I couldn't find {name}."

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            launch_intent = pm.getLaunchIntentForPackage(matched_package)

            if launch_intent:
                activity.startActivity(
                    launch_intent
                )
                return f"Opening {matched_name}."
            return "App cannot be opened."
        
        except Exception as e:
            print("Open app error:", e)
            return "Unable to open app."