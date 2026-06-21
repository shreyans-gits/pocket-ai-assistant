from jnius import autoclass
from modules.contacts import ContactsModule

class SmsModule:
    def __init__(self):
        self.contacts = ContactsModule()

    def send(self, name: str, message: str) -> str:
        number = self.contacts.find_contact(name)
        if not number:
            return f"I couldn't find {name}."

        try:
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            activity = PythonActivity.mActivity

            Intent = autoclass(
                "android.content.Intent"
            )

            Uri = autoclass(
                "android.net.Uri"
            )

            intent = Intent(
                Intent.ACTION_SENDTO
            )

            intent.setData(
                Uri.parse(
                    f"smsto:{number}"
                )
            )

            intent.putExtra(
                "sms_body",
                message
            )

            activity.startActivity(intent)
            return f"Opening messages for {name}."

        except Exception as e:
            print("SMS Error:", e)
            return "Unable to open messages."