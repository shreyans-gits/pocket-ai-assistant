from groq import Groq
import config
from core.memory import Memory

class Brain:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.AI_MODEL
        self.memory = Memory()

    def chat(self, user_input: str) -> str:
        memory_text = self.memory.get_all_as_text()

        system_prompt = f"""
        You are {config.ASSISTANT_NAME}, a smart and witty AI mobile assistant.
        You are talking to {config.USER_NAME}.
        Keep responses short (one to two lines unless you need a bigger response) and conversational — you are being spoken aloud.
        No bullet points or markdown. Just natural sentences.

        What you remember about the user:
        {memory_text}
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content

    def get_intent(self,query):
        try:
            intent_prompt = f"""
            You are an intent classifier. Classify the following query into exactly one of these intents:
            WEATHER, NEWS, SYSTEM, SEARCH, WATCH, WIKIPEDIA, NOTE_ADD, NOTE_READ, REMINDER, CONVERSATION

            Rules:
            - Reply with just the intent word, nothing else
            - No punctuation, no explanation
            - If unsure, return CONVERSATION

            Query: {query}
            """
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": intent_prompt}
                ],
                temperature=0, 
                max_tokens=10 
            )
            intent = response.choices[0].message.content.strip().upper()
            print(f"--- Intent Detected: {intent} ---")
            return intent
        
        except Exception as e:
            print(f"Intent Error: {e}")
            return "CONVERSATION"
        
    def get_intents(self, query):
        import json
        try:
            intents_prompt = f"""
            You are an expert multi-intent semantic parsing engine. Your job is to break down a user's mobile assistant query into a structured JSON array of execution steps.

            Valid Intent List:
            WEATHER, NEWS, SYSTEM, SEARCH, WATCH, WIKIPEDIA, NOTE_ADD, NOTE_READ, REMINDER, CONVERSATION

            Structural Rules:
            1. Return a raw, clean JSON array of objects. Do not include markdown code blocks, do not wrap in ```json, do not write explanations. Just the raw text array.
            2. Max 3 intents per query.
            3. If a query only represents a single intent, still return a list containing exactly one object.
            4. If a query does not match any specific intent, classify it as CONVERSATION.

            Dependency & Subject Rules:
            - "subject": Extract the target entity or payload if applicable (e.g., search query, note text, reminder message, wiki topic), otherwise null.
            - "depends_on": Set this to null if the intent can run instantly on its own. Set it to another intent's string name only if this intent requires that intent's output first.

            Output Examples:
            Query: "check my battery and tell me the weather"
            [
            {{"intent": "SYSTEM", "depends_on": null, "subject": null}},
            {{"intent": "WEATHER", "depends_on": null, "subject": null}}
            ]

            Query: "search for the nearest pizza place"
            [
            {{"intent": "SEARCH", "depends_on": null, "subject": "nearest pizza place"}}
            ]

            Query: "note down buy groceries tomorrow and read my notes"
            [
            {{"intent": "NOTE_ADD", "depends_on": null, "subject": "buy groceries tomorrow"}},
            {{"intent": "NOTE_READ", "depends_on": null, "subject": null}}
            ]

            Query: "remind me to call mom in 10 minutes"
            [
            {{"intent": "REMINDER", "depends_on": null, "subject": "call mom"}}
            ]

            Query: "what's the capital of france"
            [
            {{"intent": "CONVERSATION", "depends_on": null, "subject": null}}
            ]

            Query: {query}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": intents_prompt}
                ],
                temperature=0,
                max_tokens=150
            )
            raw_content = response.choices[0].message.content.strip()
            if raw_content.startswith("```"):
                raw_content = raw_content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            if raw_content.startswith("json"):
                raw_content = raw_content.split("json", 1)[1].strip()

            intent_list = json.loads(raw_content)
            print(f"--- Multi-Intent Graph Parsed ---\n{json.dumps(intent_list, indent=2)}\n---------------------------------")
            return intent_list
        
        except Exception as e:
            print(f"Multi-Intent Parsing Error: {e}")
            fallback_intent = self.get_intent(query)
            return [{"intent": fallback_intent, "depends_on": None, "subject": None}]
        

    def extract_number(self, query, intent):
        try:
            extract_prompt = f"""
            Extract only the number out of the query.
            Return just the subject, nothing else, no punctuation.

            Examples:
            'Increase the volume by 10' -> '10'
            'Decrease the brighteness by 20' -> '20'

            Query: {query}
            Intent: {intent}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": extract_prompt}
                ],
                temperature=0,
                max_tokens=20
            )

            subject = response.choices[0].message.content.strip()
            
            print(f"--- Value Extracted: {subject} ---")
            
            return int(subject)

        except Exception as e:
            print(f"Extraction Error: {e}")
            return None