# scenarios.py

import random

class Scenario:
    def __init__(self, name, description, participants, probability):
        self.name = name
        self.description = description
        self.participants = participants
        self.probability = probability

    async def execute(self, agents):
        participants = [agent for agent in agents if agent.role in self.participants]
        if not participants:
            return "没有合适的参与者，场景无法执行。"

        prompt = f"""场景：{self.name}
        描述：{self.description}
        参与者：{', '.join([agent.name for agent in participants])}

        请描述这个场景是如何展开的，以及每个参与者的反应和行动。"""

        responses = []
        for agent in participants:
            response = await agent.get_response(prompt)
            responses.append(f"{agent.name}: {response}")

        return "\n".join(responses)

scenarios = [
    Scenario("科技创新展览", "学校举办了一场科技创新展览，学生们展示自己的发明创造。", ["学生", "教师"], 0.1),
    Scenario("校园清洁日", "学校组织了一次全校范围的清洁活动，所有师生一起参与。", ["学生", "教师", "校长"], 0.2),
    Scenario("跨学科教学实验", "学校尝试一种新的跨学科教学方法，融合多个学科的内容。", ["教师", "学生"], 0.15),
    Scenario("校园欺凌事件", "有学生报告遭受校园欺凌，学校需要进行调查和处理。", ["学生", "教师", "校长"], 0.05),
    Scenario("学生社团活动日", "学校举办学生社团展示活动，展现学生的课外才能。", ["学生", "教师"], 0.2),
]

async def execute_random_scenario(agents):
    scenario = random.choices(scenarios, weights=[s.probability for s in scenarios], k=1)[0]
    result = await scenario.execute(agents)
    return f"===== 场景：{scenario.name} =====\n{result}"

