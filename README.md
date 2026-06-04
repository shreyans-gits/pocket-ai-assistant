# ZORO 🤖
### Zero-Overhead Responsive Operative

> A standalone voice AI assistant for Android, built entirely in Python. No cloud lock-in. No shortcuts. Just a guy in your pocket.

---

## What is ZORO?

ZORO is a fully standalone AI assistant that runs on your Android phone. It uses Groq's LLM API for intelligence and controls your phone by voice — calls, reminders, search, SMS, and more. Unlike most assistant apps, ZORO runs its entire brain on-device logic in Python, with no dependency on a laptop or external server.

This is the mobile counterpart to [NOVA](https://github.com/shreyans-gits/voice-controlled-laptop-system) — but ZORO is its own product. It doesn't need NOVA to function.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| UI Framework | KivyMD |
| AI / LLM | Groq API (Llama 3) |
| Android Bridge | jnius + plyer |
| Packaging | Buildozer |
| Voice Input | SpeechRecognition (Google backend) |
| Voice Output | plyer TTS (Android native) |
| Memory | JSON (on-device persistent storage) |

---

## Features (Planned by Phase)

### Phase 1 — Core Brain
- Voice input → Groq intent engine → voice response
- Chat UI with live status indicator (IDLE / LISTENING / THINKING / SPEAKING)
- Persistent memory — ZORO remembers facts about you across sessions
- Built-in modules: weather, news, web search, reminders, voice notes, battery & system info
- Push notifications for reminders via `plyer`

### Phase 2 — Phone Control
- **Contacts + Calls** — "Call Mom", "What's Rohan's number"
- **SMS** — "Text Tani saying I'll be late"
- **Open apps by voice** — "Open Instagram", "Open Maps"
- **Set alarms** — "Set an alarm for 7am"
- **Flashlight toggle** — "Turn on torch"

### Phase 3 — Intelligence Layer
- Context-aware conversations (session memory across turns)
- Multi-intent handling — "Text Rohan and set a reminder in 20 minutes"
- Proactive alerts — ZORO notices low battery, upcoming reminders, etc.
- Location-aware responses — weather and search auto-use current city via GPS
- Daily briefing — "Good morning" triggers weather + news + pending reminders

### Phase 4 — Mobile Exclusives
- **Wake word** — "Hey ZORO" triggers hands-free from background
- **WhatsApp messaging** — "Send a WhatsApp to Tani"
- **OCR via camera** — point at text, ZORO reads and explains it
- **Clipboard AI** — copy anything, ask ZORO to summarize or translate

---


## Status

> 🚧 Currently in development — Phase 1 in progress.

---

## Author

Built by [Shreyans](https://github.com/shreyans-gits) — part of a broader personal AI ecosystem alongside NOVA.
