# main.py

import asyncio
import random
from datetime import datetime, timedelta
import os
from agents.teacher import Teacher
from agents.student import Student
from schedule import DAILY_SCHEDULE
from config import STUDENTS_INFO, TEACHER_INFO, SPECIAL_EVENTS, ADDITIONAL_EVENTS
from school_rules import SchoolRules, weekly_rule_review
from report_generator import ReportGenerator
from scenarios import execute_random_scenario

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
    
    # 根据学生的个性特征和社会存在感选择学生
    student_weights = [s.event_probabilities[event_type] * s.social_presence for s in students]
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

async def simulate_school_day(teachers, students, school_rules, report_generator, day_count):
    start_time = datetime.strptime("05:00", "%H:%M")
    end_time = datetime.strptime("22:10", "%H:%M")
    current_time = start_time

    discipline_incidents = 0

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
                            discipline_incidents += 1
                else:
                    log_message(f"\n{time_slot} - {activity['activity']} ({activity['location']})")
                
                # 随机触发场景
                if random.random() < 0.1:  # 10% 的概率触发随机场景
                    scenario_result = await execute_random_scenario(teachers + students)
                    log_message(scenario_result)
                
                current_time = slot_end
                break
        else:
            current_time += timedelta(minutes=1)

    # 更新报告生成器的数据
    report_generator.update_term_data(students, discipline_incidents)

    # 每周进行校规审查
    if day_count % 1 == 0:
        await weekly_rule_review(teachers + students, school_rules, report_generator.term_data)

    log_message("\n学校一天结束")

async def simulate_school_term(teachers, students, days=90):
    school_rules = SchoolRules()
    report_generator = ReportGenerator()
    principal = Teacher("Principal Johnson", "校长", "有20年教育管理经验", "注重全面发展，鼓励创新")

    for day in range(1, days + 1):
        log_message(f"\n====== 第 {day} 天 ======")
        await simulate_school_day(teachers, students, school_rules, report_generator, day)

        # 随机添加特殊成就
        if random.random() < 0.05:  # 5% 的概率有特殊成就
            achievement = f"学生{random.choice(students).name}在{random.choice(['数学', '物理', '生物', '体育'])}比赛中获得优异成绩"
            report_generator.add_special_achievement(achievement)
            log_message(f"特殊成就: {achievement}")

    # 生成学期报告
    term_report = await report_generator.generate_term_report(principal)
    log_message("\n===== 学期总结报告 =====\n" + term_report)

async def main():
    log_message("模拟开始")
    
    teachers = [
        Teacher("Olivia Bennett", "数学", TEACHER_INFO["background"], TEACHER_INFO["initial_style"]),
        Teacher("Daniel Wright", "物理", TEACHER_INFO["background"], TEACHER_INFO["initial_style"]),
        Teacher("Rachel Foster", "生物", TEACHER_INFO["background"], TEACHER_INFO["initial_style"]),
        Teacher("Michael Chen", "体育", TEACHER_INFO["background"], TEACHER_INFO["initial_style"])
    ]

    students = [Student(s["name"], s["personality"], s["background"], s["event_probabilities"]) for s in STUDENTS_INFO]

    await simulate_school_term(teachers, students)
    
    log_message("模拟结束")

if __name__ == "__main__":
    asyncio.run(main())