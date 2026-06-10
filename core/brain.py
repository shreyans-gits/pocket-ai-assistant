from groq import Groq
import config

class Brain:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.AI_MODEL

        self.system_prompt = f"""
        You are {config.ASSISTANT_NAME}, a smart, and witty AI desktop assistant.
        You are talking to {config.USER_NAME}.
        Keep responses short(one to two lines unless you need to have a bigger response) and conversational — you are being spoken aloud.
        No bullet points or markdown. Just natural sentences.
        """

    def chat(self, user_input: str) -> str:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        
        return response.choices[0].message.content
