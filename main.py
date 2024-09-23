# main.py

import asyncio
import random
from datetime import datetime, timedelta
import os
from agents.teacher import Teacher
from agents.student import Student
from schedule import DAILY_SCHEDULE
from config import STUDENTS_INFO, SPECIAL_EVENTS, ADDITIONAL_EVENTS

# 创建日志目录
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 创建日志文件
log_file = os.path.join(log_dir, f'simulation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

def log_message(message):
    print(message)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

async def simulate_special_event(teacher, students):
    event_type = random.choice(ADDITIONAL_EVENTS)
    
    # 根据学生的个性特征选择学生
    student_weights = [s.event_probabilities[event_type] for s in students]
    student = random.choices(students, weights=student_weights, k=1)[0]
    
    log_message(f"\n特殊事件发生: {event_type}")

    if event_type == "课堂讨论事件":
        controversial_opinion = "数学在现实生活中并不重要"
        teacher_response = await teacher.handle_classroom_discussion(student.name, controversial_opinion)
        log_message(f"{teacher.name}: {teacher_response}")
        for s in students:
            reaction = await s.react_to_situation(f"{student.name}提出了观点：{controversial_opinion}")
            log_message(f"{s.name}: {reaction}")

    elif event_type == "小组合作冲突":
        group = [student] + random.sample([s for s in students if s != student], 2)
        conflict_reason = "任务分配不均"
        teacher_response = await teacher.handle_group_conflict([s.name for s in group], conflict_reason)
        log_message(f"{teacher.name}: {teacher_response}")
        for s in group:
            reaction = await s.react_to_situation(f"小组内因{conflict_reason}发生冲突")
            log_message(f"{s.name}: {reaction}")

    elif event_type == "考试作弊事件":
        teacher_response = await teacher.handle_cheating_incident(student.name)
        log_message(f"{teacher.name}: {teacher_response}")
        reaction = await student.react_to_situation("被发现在考试中作弊")
        log_message(f"{student.name}: {reaction}")

    elif event_type == "课后作业督促":
        excuse = "我的电脑坏了，无法完成在线作业"
        teacher_response = await teacher.handle_homework_followup(student.name, excuse)
        log_message(f"{teacher.name}: {teacher_response}")
        reaction = await student.react_to_situation(f"因为{excuse}没有完成作业")
        log_message(f"{student.name}: {reaction}")

async def simulate_school_day(teachers, students):
    start_time = datetime.strptime("05:00", "%H:%M")
    end_time = datetime.strptime("22:10", "%H:%M")
    current_time = start_time

    while current_time <= end_time:
        for time_slot, activity in DAILY_SCHEDULE.items():
            slot_start, slot_end = map(lambda x: datetime.strptime(x.strip(), "%H:%M"), time_slot.split('-'))
            if slot_start <= current_time < slot_end:
                if "subject" in activity:
                    subject = activity["subject"]
                    location = activity["location"]
                    teacher = next((t for t in teachers if t.subject == subject), None)
                    if teacher:
                        special_event = random.choice(SPECIAL_EVENTS) if random.random() < 0.2 else None
                        lesson = await teacher.teach(time_slot, special_event)
                        log_message(f"\n{time_slot} - {subject}课 ({location}):")
                        log_message(f"{teacher.name}: {lesson}")

                        for student in students:
                            reaction = await student.learn(lesson, special_event)
                            log_message(f"{student.name}: {reaction}")

                        if random.random() < 0.3:  # 30% 的概率触发特殊事件
                            await simulate_special_event(teacher, students)
                else:
                    log_message(f"\n{time_slot} - {activity['activity']} ({activity['location']})")
                
                current_time = slot_end
                break
        else:
            current_time += timedelta(minutes=1)

    log_message("\n学校一天结束")

async def main():
    log_message("模拟开始")
    
    teachers = [
        Teacher("Olivia Bennett", "数学"),
        Teacher("Daniel Wright", "物理"),
        Teacher("Rachel Foster", "生物"),
        Teacher("Michael Chen", "体育")
    ]

    students = [Student(s["name"], s["personality"], s["background"], s["event_probabilities"]) for s in STUDENTS_INFO]

    await simulate_school_day(teachers, students)
    
    log_message("模拟结束")

if __name__ == "__main__":
    asyncio.run(main())