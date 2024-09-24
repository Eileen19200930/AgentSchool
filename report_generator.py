# report_generator.py

class ReportGenerator:
    def __init__(self):
        self.term_data = {
            "average_academic_performance": 0,
            "average_participation": 0,
            "average_creativity": 0,
            "average_teamwork": 0,
            "discipline_incidents": 0,
            "special_achievements": []
        }

    def update_term_data(self, students, incidents):
        self.term_data["average_academic_performance"] = sum(s.scores["学术表现"] for s in students) / len(students)
        self.term_data["average_participation"] = sum(s.scores["参与度"] for s in students) / len(students)
        self.term_data["average_creativity"] = sum(s.scores["创造力"] for s in students) / len(students)
        self.term_data["average_teamwork"] = sum(s.scores["团队合作"] for s in students) / len(students)
        self.term_data["discipline_incidents"] = incidents

    def add_special_achievement(self, achievement):
        self.term_data["special_achievements"].append(achievement)

    async def generate_term_report(self, principal):
        report_prompt = f"""作为校长{principal.name}，请根据以下数据生成本学期的总结报告：

平均学术表现：{self.term_data['average_academic_performance']:.2f}
平均参与度：{self.term_data['average_participation']:.2f}
平均创造力：{self.term_data['average_creativity']:.2f}
平均团队合作：{self.term_data['average_teamwork']:.2f}
纪律事件数量：{self.term_data['discipline_incidents']}
特殊成就：
{chr(10).join(self.term_data['special_achievements'])}

请提供一份简洁的学期总结报告，包括：
1. 总体表现评估
2. 值得表扬的方面
3. 需要改进的领域
4. 对下学期的期望和建议

请以校长的身份撰写这份报告。"""

        report = await principal.get_response(report_prompt)
        return report