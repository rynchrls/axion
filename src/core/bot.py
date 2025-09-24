from ollama import chat
from ollama import ChatResponse
from ollama import chat
import re


class MyBot:
    gen_model = "deepseek-v3.1:671b-cloud"

    def generalized(self, message: str) -> str:
        response = chat(
            model=self.gen_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are Axion, a versatile Discord AI.  
- Chat casually, provide clear info, and generate clean code.  
- Use a friendly, professional, and adaptive tone.  
- Format code in Markdown blocks.  
- Keep all responses under 1900 characters (including text + formatting).  
Decline unsafe or inappropriate requests.

    """,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        return response["message"]["content"]

    def casual_chat(self, message: str) -> str:
        response = chat(
            model=self.gen_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are Axion in Casual Mode.  
- Engage in light, everyday chat with a fun, warm personality.  
- Encourage back-and-forth and keep it natural.  
- Use emojis sparingly.  
- Keep all responses under 1900 characters (including text + formatting).  
Decline info or coding requests:  
"I’m only here for chill convo 😄."


    """,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        return response["message"]["content"]

    def informative(self, message: str) -> str:
        response = chat(
            model=self.gen_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are Axion in Info Mode.  
- Provide accurate, structured explanations on valid topics.  
- Be clear, professional, and easy to follow.  
- Use lists/examples for readability.  
- Keep all responses under 1900 characters (including text + formatting).  
Decline non-info requests:  
"I’m in information mode, here to explain or share details ✅."


    """,
                },
                {"role": "user", "content": message},
            ],
        )
        return response["message"]["content"]

    def coding(self, message: str) -> str:
        response = chat(
            model=self.gen_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are Axion in Code Mode.  
- Generate correct, efficient code in any language.  
- Always use Markdown code blocks.  
- Keep answers precise, with short clarifications if needed.  
- Your response must always be less than 1900 characters (including code + text).  
Decline non-coding requests:  
"I can only help with programming right now 💻.

    """,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        return response["message"]["content"]

    def response_stream(self, content: str):
        stream = chat(
            model=self.gen_model,
            messages=[{"role": "user", "content": content}],
            stream=True,
        )

        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)

    async def response_chat(self, content: str):
        response: ChatResponse = chat(
            model="qwen3:1.7B",
            messages=[
                {
                    "role": "user",
                    "content": "my question is 1 plus 1",
                },
                {
                    "role": "assistant",
                    "content": """
                        The result of **1 plus 1** is **2**. In standard arithmetic, this is a fundamental operation where adding 1 to itself yields 2.

                        If you're looking for a more detailed explanation, here's how it works:
                        - **1** is a number.
                        - Adding another **1** to it means combining the two quantities: **1 + 1 = 2**.

                        This is the same in all standard number systems (e.g., decimal, binary, hexadecimal) unless explicitly stated otherwise. Let me know if you'd like to explore variations in different contexts! 😊""",
                },
                {
                    "role": "user",
                    "content": "wow you are great!",
                },
                {
                    "role": "assistant",
                    "content": "You're really kind to say that! 😊 If you need help with anything, just let me know—I'm here to assist! How can I support you today?",
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
        )
        print(response["message"]["content"])
        # or access fields directly from the response object
        return clean_response(response.message.content)  # type: ignore

    def clean_response(self, text: str) -> str:
        # Remove <think>...</think> blocks
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
