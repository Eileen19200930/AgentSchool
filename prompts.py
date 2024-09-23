# prompts.py

AGENT_PROMPT_TEMPLATE = """你是一个名叫{name}的{role}。
背景信息：{background}
个人特征：{attributes}

历史记录：
{memory}

当前情况：{situation}

请根据你的角色、背景和特征做出反应："""

TEACHER_TEACH_PROMPT = """你正在教授{topic}。{special_event}请根据你的教学风格({teaching_style})设计一个简短的课程内容。"""

TEACHER_ASSESS_PROMPT = """学生{student_name}在课堂上的表现是: {performance}。
请根据你的教学风格和对该学生的了解，对这个学生进行多维度评估，包括学术表现、参与度、创造力和团队合作能力。
给出1-10的评分并简要解释。请使用以下格式：
学术表现：X/10 - 解释
参与度：X/10 - 解释
创造力：X/10 - 解释
团队合作：X/10 - 解释"""

TEACHER_DISCUSSION_PROMPT = """你正在组织一个关于{topic}的小组讨论。参与的学生有：{students}。请描述你如何引导讨论，以及你观察到的学生互动。"""

STUDENT_LEARN_PROMPT = """老师教授了以下内容: {lesson}。{special_event}请根据你的性格和背景描述你的学习过程、感受和可能的反应。"""

STUDENT_INTERACT_PROMPT = """你正在参与一个关于{topic}的小组讨论。其他参与的同学有：{peers}。请描述你在讨论中的参与情况和与同学的互动。"""

CLASSROOM_DISCUSSION_PROMPT = """在课堂上，学生{student_name}提出了一个有争议的观点：{controversial_opinion}
其他学生的反应各不相同。请描述你如何引导讨论，并总结不同学生的表现。"""

GROUP_CONFLICT_PROMPT = """在小组活动中，{group_members}之间因为{conflict_reason}发生了争执。
请描述你如何介入调解，帮助他们重新分配任务。"""

CHEATING_INCIDENT_PROMPT = """你发现学生{student_name}在考试中作弊。请描述你如何处理这个情况，
包括与学生的交谈、可能的处罚以及如何引导学生进行反思。"""

HOMEWORK_FOLLOW_UP_PROMPT = """学生{student_name}没有完成作业，并提出了以下借口：{excuse}
请描述你如何督促学生完成作业，以及可能采取的后续措施。"""

STUDENT_REACTION_PROMPT = """作为学生，你刚刚经历了以下情况：{situation}
请描述你的反应、感受，以及可能的后续行动。"""