from core.brain import Brain
from core.voice import Voice

from modules.search import SearchModule
from modules.system import SystemModule
from modules.voice_note import VoiceNoteModule
from modules.reminder import ReminderModule
from modules.weather import WeatherModule
from modules.news import NewsModule


def main():
    brain = Brain()
    voice = Voice()

    search = SearchModule()
    system = SystemModule()
    notes = VoiceNoteModule()
    reminder = ReminderModule()
    weather = WeatherModule()
    news = NewsModule()

    voice.speak(
        f"Hello {brain.memory.get('name') or 'there'}, I am ZORO. How can I help?"
    )

    while True:

        text = voice.listen()
        if not text:
            continue

        print("You:", text)
        text = text.lower()

        if "exit" in text or "quit" in text:
            voice.speak("Goodbye.")
            break

        elif "weather" in text:
            response = weather.getWeather()

        elif "news" in text:
            response = news.get_news()

        elif "system" in text or "battery" in text:
            response = system.get_status()

        elif "search" in text:
            query = text.replace("search", "").strip()
            search.search(query)
            response = "Searching."

        elif "youtube" in text or "watch" in text:
            query = text.replace("watch", "").replace("youtube", "").strip()
            search.watch(query)
            response = "Opening YouTube."

        elif "wikipedia" in text or "wiki" in text:
            query = (
                text.replace("wikipedia", "")
                .replace("wiki", "")
                .strip()
            )
            response = search.getWiki(query)

        elif "note" in text:
            if "read" in text or "show" in text:
                response = notes.get_notes()
            else:
                note_text = text.replace("note", "").strip()
                response = notes.save_note(note_text)

        elif "remind" in text:
            response = reminder.set_reminder(
                "Reminder",
                10
            )

        else:
            response = brain.chat(text)

        print("ZORO:", response)
        voice.speak(response)


if __name__ == "__main__":
    main()