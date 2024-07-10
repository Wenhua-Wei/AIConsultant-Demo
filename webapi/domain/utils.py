import re
import json
import os

from domain.Company import Company

company = Company()

def transform_data(data_list):
    transformed_data = ""
    for item in data_list:
        transformed_data = transformed_data + \
            "assistant:" + item['subject'] + ", " + "user:"
        if (item["type"] == "MCQ"):
            for answer in item["answers"]:
                transformed_data += answer+" "
            transformed_data += ","
        else:
            transformed_data += item['answer'] + ", "

    return transformed_data

def format_history (company_name, company_info, answers):
    history = ""
    file_path = 'webapi/history.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            history = file.read()
        history += "system: " + "以下是针对性问卷的问题和用户回答, "
        answers = transform_data(answers)
        history += answers
        os.remove(file_path)

    else:
        history = "system: 你是一位企业分析专家，专业从事对各个大中小企业进行全面信息采集及分析，从业多年，有丰富且专业的经验，下面我希望你能针对输入的这家公司去做全面的背景信息收集和分析，越详细越好, " + "user: " + company_name + ", " + "assistant: " + company_info + ", " + "system: " + "一位客户想要摸清上述公司的需求，以下是针对这位客户有关生成式人工智能理解的调查问卷问题和客户的回答, "
        # answers.pop(0)
        answers = transform_data(answers)
        history += answers
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(history)

    return history


def transform_specialized_questions(specialized_questions):
    patterns_to_remove = [
    r'\（填空题\）',
    r'\（单选题\）',
    r'\（多选题\）'
    ]
    specialized_questions = re.sub('|'.join(patterns_to_remove), '', specialized_questions)
    specialized_questions = specialized_questions.replace("'",'"')
    start_index = specialized_questions.find('[')
    end_index = specialized_questions.rfind(']')
    
    json_text = specialized_questions[start_index:end_index+1]
    return json.loads(json_text)


def complete_prompt(prompt):
    completed_prompt = prompt.replace("[company_name]", company.name).replace("[company_info]", company.info).replace("")
    return completed_prompt

def format_keywords(keywords):
    keywords = keywords.split("\n")
    keywords = [keyword.split('. ', 1)[1] if '. ' in keyword else keyword for keyword in keywords]
    return keywords

def timetable_data_jsonify(timetable_str: str):
    extracted_str=extract_between_braces(timetable_str)
    if extracted_str:
        print(extracted_str)
    else:
        print("没有找到有效的JSON对象")
        return None

    json_array_str = f'[{extracted_str}]'
    try:
        json_obj = json.loads(json_array_str)
        return json_obj
    except json.JSONDecodeError as e:
        print(f"解析失败，错误信息：{e}")
        error_pos = e.pos
        print(f"错误附近的内容：{json_array_str[max(0, error_pos-10):error_pos+10]}")



def extract_between_braces(input_str):
    first_brace_pos = re.search(r'\{\s*"', input_str)
    if not first_brace_pos:
        return False
    
    all_last_brace_matches = list(re.finditer(r'"\s*\}', input_str))
    if not all_last_brace_matches:
        return False
    last_brace_pos = all_last_brace_matches[-1]
    
    extracted_content = input_str[first_brace_pos.start():last_brace_pos.end()]
    return extracted_content




# timetable_str = """
# 据您提供的信息，我为您制定了一个为期一天的Design Thinking Workshop日程安排：

# {"activity": "开场和破冰", "description": "介绍工作坊目的和日程，进行破冰游戏以促进交流。", "row_id": 0, "time": "9:00 - 9:30"},
# {"activity": "AI和设计思维介绍", "description": "为不同了解程度的参与者提供适当的AI和设计思维理论介绍，确保每个人都能理解基本概念。", "row_id": 1, "time": "9:30 - 10:30"},
# {"activity": "行业特定案例研究", "description": "针对不同行业的特点，提供相关的AI应用案例。", "row_id": 2, "time": "10:30 - 11:30"},
# {"activity": "午餐休息", "description": "为参与者提供午餐和休息时间。", "row_id": 3, "time": "11:30 - 13:00"},
# {"activity": "分组工作", "description": "根据企业规模和行业分组，让参与者共同探讨AI在各自领域的应用。", "row_id": 4, "time": "13:00 - 14:30"},
# {"activity": "设计思维实践", "description": "通过设计思维的方法，引导参与者解决实际问题。", "row_id": 5, "time": "14:30 - 15:30"},
# {"activity": "原型制作和测试", "description": "鼓励参与者创建AI解决方案的原型，并进行小组内测试。", "row_id": 6, "time": "15:30 - 16:30"},
# {"activity": "反馈和总结", "description": "收集参与者的反馈，总结工作坊的成果和学习点。", "row_id": 7, "time": "16:30 - 17:00"},
# {"activity": "后续行动计划", "description": "帮助参与者制定将设计思维和AI应用到实际工作中的行动计划。", "row_id": 8, "time": "17:00 - 17:30"}

# 请注意，此日程安排可能需要根据实际情况进行调整。希望这对您的工作坊有所帮助。
# 您提供的timetable数据格式是正确的，无需修正。
# 没有找到有效的JSON对象
# """

# result_str = '\n'.join(
#         f"Activity: {activity['activity']}, Description: {activity['description']}, Time: {activity['time']}"
#         for activity in timetable_data_jsonify(timetable_str)
#     )


# print(result_str)

