# agents/student.py

from .base_agent import Agent

class Student(Agent):
    def __init__(self, name, personality, background, event_probabilities):
        super().__init__(name, "学生")
        self.personality = personality
        self.background = background
        self.event_probabilities = event_probabilities

    async def learn(self, lesson, special_event=None):
        prompt = f"""你是一个名叫{self.name}的学生。
        个性特征：{self.personality}
        背景：{self.background}
        
        老师刚刚教授了以下内容：{lesson}
        """
        if special_event:
            prompt += f"\n特殊情况：{special_event}"
        
        prompt += "\n请描述你的学习过程、感受和可能的反应。"

        return await self.get_response(prompt)

    async def interact_with_peers(self, topic, peers):
        prompt = STUDENT_INTERACT_PROMPT.format(
            topic=topic,
            peers=', '.join([p.name for p in peers if p.name != self.name])
        )
        return await self.get_response(prompt)

    async def react_to_situation(self, situation):
        prompt = STUDENT_REACTION_PROMPT.format(situation=situation)
        return await self.get_response(prompt)

    def update_scores(self, assessment):
        for category in self.scores:
            if category in assessment:
                try:
                    start = assessment.index(category) + len(category)
                    end = assessment.index('/', start)
                    score_str = assessment[start:end].strip().strip('：:')
                    self.scores[category] = int(score_str)
                except (ValueError, IndexError):
                    log_message(f"无法解析 {category} 的分数")
                    continue
    
    async def react_to_situation(self, situation):
        prompt = f"""你是一个名叫{self.name}的学生。
        个性特征：{self.personality}
        背景：{self.background}
        
        你刚刚经历了以下情况：{situation}
        请描述你的反应、感受，以及可能的后续行动。"""
        return await self.get_response(prompt)