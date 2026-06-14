import json
import os
from datetime import datetime


class VoiceNoteModule:

    def __init__(self):
        self.notes_file = "notes.json"
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, "w", encoding="utf-8") as file:
                json.dump([], file)

    def save_note(self, text: str) -> str:
        note = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "note": text
        }

        with open(self.notes_file, "r", encoding="utf-8") as file:
            notes = json.load(file)

        notes.append(note)

        with open(self.notes_file, "w", encoding="utf-8") as file:
            json.dump(notes, file, indent=4)

        return "Note saved."

    def get_notes(self) -> str:
        try:
            with open(self.notes_file, "r", encoding="utf-8") as file:
                notes = json.load(file)

        except Exception:
            return "Could not read notes."

        if not notes:
            return "No notes found."
        result = []

        for note in notes:
            result.append(
                f"{note['time']}: {note['note']}"
            )
        return "\n".join(result)