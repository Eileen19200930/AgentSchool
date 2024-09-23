# agents/base_agent.py

from openai import AsyncOpenAI
from config import API_BASE_URL, API_KEY, MODEL_NAME

client = AsyncOpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    async def get_response(self, prompt):
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API调用出错：{e}")
            return "无法获取回应。"