# agents/teacher.py

from .base_agent import Agent

class Teacher(Agent):
    def __init__(self, name, subject, background, attributes):
        super().__init__(name, "教师", background, attributes)
        self.subject = subject

    async def teach(self, time_slot, special_event=None):
        situation = f"当前是{time_slot}，你正在教授{self.subject}课。"
        if special_event:
            situation += f" 特殊情况：{special_event}"
        
        response = await self.react_to_situation(situation)
        self.add_memory(f"教学：{time_slot} {self.subject}\n内容：{response}")
        return response

    async def assess_student(self, student_name, performance):
        situation = f"学生{student_name}在课堂上的表现是: {performance}。请进行多维度评估，包括学术表现、参与度、创造力和团队合作能力。给出1-10的评分并简要解释。"
        response = await self.react_to_situation(situation)
        self.add_memory(f"评估学生：{student_name}\n评估：{response}")
        return response

    async def handle_classroom_discussion(self, student_name, controversial_opinion):
        situation = f"学生{student_name}提出了一个有争议的观点：{controversial_opinion}。请描述你如何引导讨论。"
        response = await self.react_to_situation(situation)
        self.add_memory(f"课堂讨论：{controversial_opinion}\n处理：{response}")
        return response

    async def handle_group_conflict(self, group_members, conflict_reason):
        situation = f"{', '.join(group_members)}之间因为{conflict_reason}发生了争执。请描述你如何介入调解。"
        response = await self.react_to_situation(situation)
        self.add_memory(f"小组冲突：{conflict_reason}\n处理：{response}")
        return response

    async def handle_cheating_incident(self, student_name):
        situation = f"你发现学生{student_name}在考试中作弊。请描述你如何处理这个情况。"
        response = await self.react_to_situation(situation)
        self.add_memory(f"作弊事件：{student_name}\n处理：{response}")
        return response

    async def handle_homework_followup(self, student_name, excuse):
        situation = f"学生{student_name}没有完成作业，并提出了以下借口：{excuse}。请描述你如何督促学生完成作业。"
        response = await self.react_to_situation(situation)
        self.add_memory(f"作业督促：{student_name}\n处理：{response}")
        return response