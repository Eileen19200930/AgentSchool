import random
import asyncio
from openai import AsyncOpenAI
from config import *
import datetime
import os

client = AsyncOpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# 创建日志目录
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 创建日志文件
log_file = os.path.join(log_dir, f'simulation_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

def log_message(message):
    print(message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

class Agent:
    def __init__(self, name, role, attributes, background):
        self.name = name
        self.role = role
        self.attributes = attributes
        self.background = background
        self.memory = []

    async def get_response(self, prompt):
        full_prompt = AGENT_PROMPT_TEMPLATE.format(
            name=self.name,
            role=self.role,
            background=self.background,
            attributes=self.attributes,
            memory=' '.join(self.memory[-5:]),
            situation=prompt
        )

        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            error_message = f"API调用出错：{e}"
            log_message(error_message)
            return "无法获取回应。"

    def update_memory(self, event):
        self.memory.append(event)

class Teacher(Agent):
    def __init__(self, name, teaching_style, background):
        super().__init__(name, "教师", f"教学风格: {teaching_style}", background)
        self.teaching_style = teaching_style

    async def teach(self, topic, special_event=None):
        prompt = TEACHER_TEACH_PROMPT.format(
            topic=topic,
            special_event=f"特殊情况：{special_event}。" if special_event else "",
            teaching_style=self.teaching_style
        )
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

class Student(Agent):
    def __init__(self, name, personality, background):
        super().__init__(name, "学生", f"性格: {personality}", background)
        self.personality = personality
        self.scores = {"学术表现": 0, "参与度": 0, "创造力": 0, "团队合作": 0}

    async def learn(self, lesson, special_event=None):
        prompt = STUDENT_LEARN_PROMPT.format(
            lesson=lesson,
            special_event=f"特殊情况：{special_event}。" if special_event else ""
        )
        return await self.get_response(prompt)

    async def interact_with_peers(self, topic, peers):
        prompt = STUDENT_INTERACT_PROMPT.format(
            topic=topic,
            peers=', '.join([p.name for p in peers if p.name != self.name])
        )
        return await self.get_response(prompt)

    def update_scores(self, assessment):
        for category in self.scores:
            if category in assessment:
                try:
                    # 查找类别名称后的数字
                    start = assessment.index(category) + len(category)
                    end = assessment.index('/', start)
                    score_str = assessment[start:end].strip().strip('：:')
                    self.scores[category] = int(score_str)
                except (ValueError, IndexError):
                    log_message(f"无法解析 {category} 的分数")
                    continue

async def simulate_class(teacher, students, special_event=None):
    log_message(f"\n开始 {teacher.name} 的数学课")
    if special_event:
        log_message(f"特殊事件: {special_event}")
    
    lesson = await teacher.teach("数学", special_event)
    teacher.update_memory(f"教授了课程: {lesson}")
    log_message(f"{teacher.name}: {lesson}")

    for student in students:
        reaction = await student.learn(lesson, special_event)
        student.update_memory(f"学习了课程: {lesson}")
        log_message(f"{student.name}: {reaction}")
        
        assessment = await teacher.assess_student(student.name, reaction)
        teacher.update_memory(f"评估了{student.name}: {assessment}")
        log_message(f"{teacher.name}对{student.name}的评估: {assessment}")
        
        log_message(f"原始评估内容: {assessment}")
        
        student.update_scores(assessment)

    log_message("\n开始小组讨论")
    teacher_observation = await teacher.facilitate_group_discussion("今天学习的数学概念", students)
    log_message(f"{teacher.name}的观察: {teacher_observation}")
    
    for student in students:
        interaction = await student.interact_with_peers("今天学习的数学概念", [s for s in students if s != student])
        log_message(f"{student.name}的互动: {interaction}")

    log_message("课程结束\n")

async def main():
    log_message("模拟开始")
    log_message(f"使用模型: {MODEL_NAME}")
    
    math_teacher = Teacher(
        TEACHER_INFO["name"],
        TEACHER_INFO["initial_style"],
        TEACHER_INFO["background"]
    )
    
    students = [Student(s["name"], s["personality"], s["background"]) for s in STUDENTS_INFO]

    for i in range(5):
        log_message(f"\n第 {i+1} 节课:")
        await simulate_class(math_teacher, students, SPECIAL_EVENTS[i])

        if i == 2:
            log_message("教学风格转变")
            math_teacher.teaching_style = "素质教育，注重理解和应用，鼓励创新思维"
            math_teacher.attributes = f"教学风格: {math_teacher.teaching_style}"

    log_message("\n最终评估:")
    for student in students:
        log_message(f"{student.name}的成绩:")
        for category, score in student.scores.items():
            log_message(f"  {category}: {score}")
    
    log_message("\n模拟结束")

if __name__ == "__main__":
    asyncio.run(main())