import json
import os
from datetime import datetime

from config import NOTES_FILE

class VoiceNoteModule:

    def save_note(self, text: str) -> str:
        note = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": text
        }

        notes = []

        if os.path.exists(NOTES_FILE):
            try:
                with open(NOTES_FILE, "r", encoding="utf-8") as file:
                    notes = json.load(file)
            except Exception:
                notes = []

        notes.append(note)

        with open(NOTES_FILE, "w", encoding="utf-8") as file:
            json.dump(notes, file, indent=4)

        return "Note saved."

    def get_notes(self) -> str:
        if not os.path.exists(NOTES_FILE):
            return "No notes found."

        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as file:
                notes = json.load(file)

            if not notes:
                return "No notes found."

            result = []

            for note in notes:
                result.append(
                    f"{note['time']}: {note['note']}"
                )

            return "\n".join(result)

        except Exception:
            return "Could not read notes."