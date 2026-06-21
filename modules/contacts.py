try:
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission  # type: ignore
    ANDROID = True

except ImportError:
    ANDROID = False


class ContactsModule:
    def __init__(self):
        if ANDROID:
            self.request_permissions()
        else:
            print("Contacts module only works on Android")

    def request_permissions(self):
        try:
            request_permissions([
                Permission.READ_CONTACTS,
                Permission.CALL_PHONE
            ])

        except Exception:
            pass

    def find_contact(self, name: str) -> str:
        try:
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            activity = PythonActivity.mActivity
            ContactsContract = autoclass(
                "android.provider.ContactsContract$Contacts"
            )
            resolver = activity.getContentResolver()
            cursor = resolver.query(
                ContactsContract.CONTENT_URI,
                None,
                None,
                None,
                None
            )
            if cursor:
                while cursor.moveToNext():
                    name_index = cursor.getColumnIndex(
                        ContactsContract.DISPLAY_NAME
                    )
                    contact_name = cursor.getString(
                        name_index
                    )

                    if contact_name and name.lower() in contact_name.lower():
                        contact_id_index = cursor.getColumnIndex(
                            ContactsContract._ID
                        )
                        contact_id = cursor.getString(
                            contact_id_index
                        )
                        cursor.close()
                        return self.get_phone_number(
                            resolver,
                            contact_id
                        )
                cursor.close()
            return None

        except Exception as e:
            print("Contact Error:", e)
            return None

    def get_phone_number(self, resolver, contact_id):
        Phone = autoclass(
            "android.provider.ContactsContract$CommonDataKinds$Phone"
        )
        cursor = resolver.query(
            Phone.CONTENT_URI,
            None,
            f"{Phone.CONTACT_ID}=?",
            [contact_id],
            None
        )
        if cursor:
            while cursor.moveToNext():
                number_index = cursor.getColumnIndex(
                    Phone.NUMBER
                )
                number = cursor.getString(
                    number_index
                )
                cursor.close()
                return number
            cursor.close()
        return None

    def call(self, name: str) -> str:
        number = self.find_contact(name)
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
                Intent.ACTION_CALL
            )
            intent.setData(
                Uri.parse(
                    f"tel:{number}"
                )
            )
            activity.startActivity(intent)
            return f"Calling {name}."
        
        except Exception as e:
            print("Call Error:", e)
            return "Unable to make call."