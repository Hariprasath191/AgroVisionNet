from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("chatbot_api")
)

def ask_farmer_bot(question, disease=None, weather=None):

    system = f"""
You are an agriculture assistant helping farmers.

Disease: {disease}
Weather: {weather}

Explain simply.
Suggest low-cost solutions.
Be short and clear.
"""

    res = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":question}
        ]
    )

    return res.choices[0].message.content
