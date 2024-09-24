# school_rules.py
import random

class SchoolRules:
    def __init__(self):
        self.rules = [
            "尊重他人，互帮互助",
            "按时上课，不迟到不早退",
            "保持校园整洁，爱护公共设施",
            "努力学习，追求进步",
            "遵守课堂纪律，认真听讲"
        ]

    def add_rule(self, new_rule):
        if new_rule not in self.rules:
            self.rules.append(new_rule)

    def remove_rule(self, rule):
        if rule in self.rules:
            self.rules.remove(rule)

    def modify_rule(self, old_rule, new_rule):
        if old_rule in self.rules:
            index = self.rules.index(old_rule)
            self.rules[index] = new_rule

    def get_rules(self):
        return "\n".join(f"{i+1}. {rule}" for i, rule in enumerate(self.rules))

async def propose_rule_change(agent, current_rules, school_performance):
    prompt = f"""作为{agent.role} {agent.name}，你正在参与学校规则的修订。
当前的学校规则如下：
{current_rules}

学校的表现如下：
{school_performance}

根据学校的表现和你的经验，你认为应该如何修改学校规则？
请提出一项具体的修改建议（添加新规则、删除现有规则或修改现有规则），并解释原因。

格式：
建议：[你的建议]
原因：[你的解释]
"""
    response = await agent.get_response(prompt)
    return response

async def weekly_rule_review(agents, school_rules, school_performance):
    log_message = []
    log_message.append("\n===== 每周校规审查 =====")
    for agent in random.sample(agents, 3):  # 随机选择3个agent参与
        suggestion = await propose_rule_change(agent, school_rules.get_rules(), school_performance)
        log_message.append(f"{agent.name}的建议：\n{suggestion}")
    
    # 这里可以添加一个机制来决定是否采纳建议，例如让校长做最后决定
    # 为简化起见，这里随机选择一个建议并执行
    if random.random() < 0.5:  # 50%的概率修改规则
        # 解析建议并修改规则（这需要更复杂的自然语言处理，这里简化处理）
        new_rule = "新规则：促进创新思维和实践能力的培养"
        school_rules.add_rule(new_rule)
        log_message.append(f"新规则已添加：{new_rule}")
    
    return "\n".join(log_message)