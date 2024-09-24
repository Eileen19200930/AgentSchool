# agents/base_agent.py

from openai import AsyncOpenAI
from config import API_BASE_URL, API_KEY, MODEL_NAME

client = AsyncOpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

class Agent:
    def __init__(self, name, role, background, attributes):
        self.name = name
        self.role = role
        self.background = background
        self.attributes = attributes
        self.memory = []
        self.social_presence = 5  # 初始社会存在感为5（范围1-10）

    async def get_response(self, prompt):
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API调用出错：{e}")
            return "无法获取回应。"

    def add_memory(self, event):
        self.memory.append(event)
        if len(self.memory) > 10:  # 保留最近的10条记忆
            self.memory.pop(0)

    def get_memory_string(self):
        return "\n".join(self.memory)

    def update_social_presence(self, change):
        self.social_presence = max(1, min(10, self.social_presence + change))

    async def react_to_situation(self, situation):
        prompt = f"""你是一个名叫{self.name}的{self.role}。
        背景信息：{self.background}
        个人特征：{self.attributes}

        历史记录：
        {self.get_memory_string()}

        当前情况：{situation}

        请根据你的角色、背景和特征做出反应："""
        
        response = await self.get_response(prompt)
        self.add_memory(f"情况：{situation}\n反应：{response}")
        return response