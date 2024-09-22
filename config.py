# config.py

# API配置
API_BASE_URL = "https://api.lqqq.ltd/v1"
API_KEY = "sk-9ng5J6z9XTWD74aEBdE3Ca36E2954b26A87bCeE9Ef008d6a"
MODEL_NAME = "gpt-4o-mini"

# Prompt模板
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

# 特殊事件列表
SPECIAL_EVENTS = [
    "学校停电，需要在自然光下上课",
    "有一位新同学加入班级",
    "学校举办数学竞赛，鼓励学生参加",
    None,
    "教育局领导来访，观摩课堂"
]

# 教师信息
TEACHER_INFO = {
    "name": "王老师",
    "initial_style": "传统教学，注重考试技巧，但正在尝试转向更注重理解和应用的教学方式",
    "background": "王老师有20年的教学经验，最近参加了一些教育创新研讨会，开始思考如何将新的教学理念融入到自己的课堂中。"
}

# 学生信息
STUDENTS_INFO = [
    {
        "name": "Sophia Lee",
        "personality": "温柔，善于倾听，热爱文学和自然",
        "background": "Sophia的家庭非常重视教育，父母都是教师。她从小在学习氛围中长大，热爱阅读和写作。她对一位文学老师的指导印象深刻，老师的鼓励让她在写作方面取得了很大的进步。她喜欢写诗和短篇故事，常常参加学校的写作比赛。她还热爱自然，喜欢在周末去徒步旅行，寻找灵感。"
    },
    {
        "name": "Jack Wilson",
        "personality": "活泼，爱开玩笑，有时过于顽皮",
        "background": "Jack来自单亲家庭，母亲忙于工作，常常缺乏陪伴。他在学校中常常表现得调皮捣蛋，以此来吸引注意。他喜欢玩电子游戏和滑板，特别擅长街头滑板。"
    },
    {
        "name": "Ava Martinez",
        "personality": "坚韧，乐观向上，热爱烹饪",
        "background": "Ava的父母移民来到这个国家，生活条件并不宽裕。尽管如此，她依然努力学习，争取奖学金。她对一位帮助她的老师充满感激。她喜欢和朋友分享美食，常常尝试制作不同国家的菜肴。"
    }
]