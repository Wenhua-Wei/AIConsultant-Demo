
import json
import re

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
    

s="""
根据您提供的信息，以下是针对华润燃气公司所处行业和公司核心业务的详细问卷设计：

```json
[
  {
    "type": "SCQ",
    "text": "您认为华润燃气在行业内的市场份额如何？（单选题）",
    "options": ["非常高", "较高", "一般", "较低", "非常低"],
    "id": 0
  },
  {
    "type": "MCQ",
    "text": "华润燃气在人工智能方面的主要应用场景是哪些？（多选题）",
    "options": ["客户服务", "供应链管理", "智能调度", "设备维护", "财务管理"],
    "id": 1
  },
  {
    "type": "SCQ",
    "text": "您认为华润燃气的核心竞争力是什么？（单选题）",
    "options": ["品牌影响力", "技术创新", "成本控制", "服务质量", "市场覆盖"],
    "id": 2
  },
  {
    "type": "MCQ",
    "text": "华润燃气在提升服务质量方面采取了哪些措施？（多选题）",
    "options": ["员工培训", "服务流程优化", "客户反馈机制", "技术投入", "合作伙伴关系强化"],
    "id": 3
  },
  {
    "type": "SCQ",
    "text": "华润燃气在技术创新方面的投入程度如何？（单选题）",
    "options": ["非常大", "较大", "一般", "较小", "非常小"],
    "id": 4
  },
  {
    "type": "MCQ",
    "text": "华润燃气在市场拓展方面主要关注哪些领域？（多选题）",
    "options": ["新区域开发", "新客户群体", "新业务模式", "国际市场", "线上市场"],
    "id": 5
  },
  {
    "type": "SCQ",
    "text": "您认为华润燃气在客户满意度方面的表现如何？（单选题）",
    "options": ["非常好", "较好", "一般", "较差", "非常差"],
    "id": 6
  },
  {
    "type": "MCQ",
    "text": "华润燃气在环保和社会责任方面采取了哪些措施？（多选题）",
    "options": ["节能减排", "绿色能源推广", "社区支持项目", "教育和培训", "慈善捐助"],
    "id": 7
  },
  {
    "type": "SCQ",
    "text": "华润燃气在应对市场变化和风险管理方面的表现如何？（单选题）",
    "options": ["非常出色", "出色", "一般", "较差", "非常差"],
    "id": 8
  },
  {
    "type": "short_answer",
    "text": "华润燃气目前拥有的人工智能相关专利数量为（填空题）。",
    "id": 9
  },
  {
    "type": "short_answer",
    "text": "华润燃气在未来五年内的主要发展目标是什么（填空题）？",
    "id": 10
  },
  {
    "type": "short_answer",
    "text": "华润燃气在提高运营效率方面采取了哪些具体措施（填空题）？",
    "id": 11
  },
  {
    "type": "short_answer",
    "text": "华润燃气在客户服务方面有哪些创新的尝试（填空题）？",
    "id": 12
  }
]
```

这份问卷旨在通过收集华润燃气在市场定位、技术创新、服务质量、环保责任、风险管理等方面的数据，结合行业内同类数据，提出有价值的建议。问卷包含8个选择题和4个填空题，选择题中混合了单选和多选题型，每个选择题提供了4到5个选项，避免了开放式回答的选项。
"""

print(transform_specialized_questions(s))