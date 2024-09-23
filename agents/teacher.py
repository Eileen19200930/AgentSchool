# agents/teacher.py

from .base_agent import Agent
from teacher_prompts import *

class Teacher(Agent):
    def __init__(self, name, subject):
        super().__init__(name, "教师")
        self.subject = subject
        if subject == "数学":
            self.prompt = MATH_TEACHER_PROMPT
        elif subject == "物理":
            self.prompt = PHYSICS_TEACHER_PROMPT
        elif subject == "生物":
            self.prompt = BIOLOGY_TEACHER_PROMPT
        elif subject == "体育":
            self.prompt = PE_TEACHER_PROMPT
        else:
            raise ValueError(f"未知科目: {subject}")

    async def teach(self, time_slot, special_event=None):
        prompt = f"{self.prompt}\n\n当前是{time_slot}，你正在教授{self.subject}课。"
        if special_event:
            prompt += f" 特殊情况：{special_event}"
        prompt += "\n请描述你的教学内容和方法。"

        return await self.get_response(prompt)

    async def assess_student(self, student_name, performance):
        prompt = TEACHER_ASSESS_PROMPT.format(
            student_name=student_name,
            performance=performance
        )
        return await self.get_response(prompt)

    async def facilitate_group_discussion(self, topic, students):
        prompt = TEACHER_DISCUSSION_PROMPT.format(
            topic=topic,
            students=', '.join([s.name for s in students])
        )
        return await self.get_response(prompt)

    async def handle_classroom_discussion(self, student_name, controversial_opinion):
        prompt = CLASSROOM_DISCUSSION_PROMPT.format(
            student_name=student_name,
            controversial_opinion=controversial_opinion
        )
        return await self.get_response(prompt)

    async def handle_group_conflict(self, group_members, conflict_reason):
        prompt = GROUP_CONFLICT_PROMPT.format(
            group_members=", ".join(group_members),
            conflict_reason=conflict_reason
        )
        return await self.get_response(prompt)

    async def handle_cheating_incident(self, student_name):
        prompt = CHEATING_INCIDENT_PROMPT.format(student_name=student_name)
        return await self.get_response(prompt)

    async def handle_homework_followup(self, student_name, excuse):
        prompt = HOMEWORK_FOLLOW_UP_PROMPT.format(
            student_name=student_name,
            excuse=excuse
        )
        return await self.get_response(prompt)
    
    async def handle_classroom_discussion(self, student_name, controversial_opinion):
        prompt = f"{self.prompt}\n\n学生{student_name}提出了一个有争议的观点：{controversial_opinion}。请描述你如何引导讨论。"
        return await self.get_response(prompt)

    async def handle_group_conflict(self, group_members, conflict_reason):
        prompt = f"{self.prompt}\n\n{', '.join(group_members)}之间因为{conflict_reason}发生了争执。请描述你如何介入调解。"
        return await self.get_response(prompt)

    async def handle_cheating_incident(self, student_name):
        prompt = f"{self.prompt}\n\n你发现学生{student_name}在考试中作弊。请描述你如何处理这个情况。"
        return await self.get_response(prompt)

    async def handle_homework_followup(self, student_name, excuse):
        prompt = f"{self.prompt}\n\n学生{student_name}没有完成作业，并提出了以下借口：{excuse}。请描述你如何督促学生完成作业。"
        return await self.get_response(prompt)