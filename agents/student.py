# agents/student.py

from .base_agent import Agent

class Student(Agent):
    def __init__(self, name, personality, background, event_probabilities):
        super().__init__(name, "学生", background, personality)
        self.event_probabilities = event_probabilities
        self.scores = {
            "学术表现": 5,
            "参与度": 5,
            "创造力": 5,
            "团队合作": 5
        }

    async def learn(self, lesson, special_event=None):
        situation = f"老师刚刚教授了以下内容：{lesson}"
        if special_event:
            situation += f"\n特殊情况：{special_event}"
        
        response = await self.react_to_situation(situation)
        self.add_memory(f"学习：{lesson}\n反应：{response}")
        
        if "积极参与" in response:
            self.update_social_presence(0.1)
        elif "表现消极" in response:
            self.update_social_presence(-0.1)
        
        return response

    async def interact_with_peers(self, topic, peers):
        situation = f"你正在参与一个关于{topic}的小组讨论。其他参与的同学有：{', '.join([p.name for p in peers if p.name != self.name])}"
        response = await self.react_to_situation(situation)
        self.add_memory(f"小组讨论：{topic}\n反应：{response}")
        return response

    def update_scores(self, assessment):
        for category, score in assessment.items():
            if category in self.scores:
                self.scores[category] = score