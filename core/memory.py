import json
import os

from config import MEMORY_FILE

class Memory:
    def __init__(self):
        self.memory = {}
        self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                    self.memory = json.load(file)
            except Exception:
                self.memory = {}
        else:
            self.memory = {}

    def save(self, key: str, value: str):
        self.memory[key] = value
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(self.memory, file, indent=4)

    def get(self, key: str):
        return self.memory.get(key)

    def get_all_as_text(self) -> str:
        if not self.memory:
            return "No stored memory."

        lines = []
        for key, value in self.memory.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)