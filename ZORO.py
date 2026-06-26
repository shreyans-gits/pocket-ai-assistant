from core.brain import Brain
from core.voice import Voice

from modules.search import SearchModule
from modules.system import SystemModule
from modules.voice_note import VoiceNoteModule
from modules.reminder import ReminderModule
from modules.weather import WeatherModule
from modules.news import NewsModule
from modules.contacts import ContactsModule
from modules.sms import SmsModule
from modules.apps import AppsModule
from modules.alarm import AlarmModule

import config

def main():
    brain = Brain()
    voice = Voice()

    search = SearchModule()
    system = SystemModule()
    notes = VoiceNoteModule()
    reminder = ReminderModule()
    weather = WeatherModule()
    news = NewsModule()
    contacts = ContactsModule()
    sms = SmsModule()
    apps = AppsModule()
    alarm = AlarmModule()

    # Intent Handlers
    def handle_weather(item, query, context):
        return weather.getWeather()

    def handle_news(item, query, context):
        return news.get_news()

    def handle_system(item, query, context):
        return system.get_status()

    def handle_search(item, query, context):
        subject = item.get("subject")
        if subject:
            search.search(subject)
            return "Searching."

        return "What should I search for?"

    def handle_watch(item, query, context):
        subject = item.get("subject")
        if subject:
            search.watch(subject)
            return "Opening YouTube."
        return "What should I open?"

    def handle_wikipedia(item, query, context):
        subject = item.get("subject")
        if subject:
            return search.getWiki(subject)
        return "What should I search on Wikipedia?"

    def handle_note_add(item, query, context):
        subject = item.get("subject")
        if subject:
            return notes.save_note(subject)

        return "What should I note down?"

    def handle_note_read(item, query, context):
        return notes.get_notes()

    def handle_reminder(item, query, context):
        subject = item.get("subject")
        if not subject:
            return "What should I remind you about?"
        minutes = brain.extract_number(query, "REMINDER")
        if not minutes:
            minutes = 10
        return reminder.set_reminder(subject, minutes)

    def handle_conversation(item, query, context):
        return brain.chat(query)
    
    def handle_call(item, query, context):
        subject = item.get("subject")
        if not subject:
            return "Who should I call?"
        return contacts.call(subject)

    def handle_sms(item, query, context):
        subject = item.get("subject")
        if not subject or ":" not in subject:
            return "Who should I text, and what should it say?"
        
        name, message = subject.split(":", 1)
        return sms.send(name.strip(), message.strip())

    def handle_app_open(item, query, context):
        subject = item.get("subject")
        if not subject:
            return "Which app should I open?"
        return apps.open_app(subject)

    def handle_alarm(item, query, context):
        result = brain.extract_time(query)
        if not result:
            return "I couldn't understand what time you meant."
        
        hour, minute = result
        return alarm.set_alarm(hour, minute)

    INTENT_HANDLERS = {
        "WEATHER": handle_weather,
        "NEWS": handle_news,
        "SYSTEM": handle_system,
        "SEARCH": handle_search,
        "WATCH": handle_watch,
        "WIKIPEDIA": handle_wikipedia,
        "NOTE_ADD": handle_note_add,
        "NOTE_READ": handle_note_read,
        "REMINDER": handle_reminder,
        "CALL": handle_call,
        "SMS": handle_sms,
        "APP_OPEN": handle_app_open,
        "ALARM": handle_alarm,
        "CONVERSATION": handle_conversation
    }

    # Startup
    voice.speak(
        f"Hello {config.USER_NAME}, I am ZORO. How can I help?"
    )
    while True:
        text = voice.listen()
        if not text:
            continue

        print("You:", text)
        if text.lower() in ["exit", "quit"]:
            voice.speak("Goodbye.")
            break

        intents = brain.get_intents(text)
        responses = []

        for item in intents:
            intent = item.get("intent")
            handler = INTENT_HANDLERS.get(intent)
            if handler:
                result = handler(
                    item,
                    text,
                    {}
                )
                responses.append(result)

        final_response = ". ".join(r.strip() for r in responses if r)
        print("ZORO:", final_response)
        voice.speak(final_response)


if __name__ == "__main__":
    main()