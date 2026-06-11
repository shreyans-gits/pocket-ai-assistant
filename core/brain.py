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