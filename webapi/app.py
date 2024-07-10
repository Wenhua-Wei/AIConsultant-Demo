import logging
from flask import Flask, request, jsonify, current_app
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from domain.Kimi import Kimi
from domain.Company import Company
from flask_cors import CORS
from threading import Thread, Event
import time
import json

from domain.utils import format_history, transform_specialized_questions, format_keywords, transform_data, timetable_data_jsonify
from domain.Sql import Sql
from domain.Mongo import Mongo
from domain.User import User


load_dotenv('.env')


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
kimi = Kimi()
company = Company()

mongo = Mongo()
sql = Sql(app)

chat_history = None
isGeneral = True
finished_specialized = False

if not app.debug:
    app.logger.setLevel(logging.DEBUG)

collect_events = {}


@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    telephone = request.args.get('telephone')
    current_app.logger.debug(
        f"Received telephone {telephone} for session ID: {session_id}")
    history = '以下为历史记录，user代表用户历史发送消息，assistant代表你之前的回复, system代表系统指令。以此作为生成本文的上下文环境。'
    mongo.insertChatHistory(telephone=telephone, new_context=history,
                            sessionID=session_id, company=Company().to_dict())
    emit('loadGeneralQuestion', 'isReady')


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    current_app.logger.debug(
        f"Disconnect===============User with session ID {session_id} disconnected")
    tel = mongo.getTelephoneBySessionID(session_id)
    mongo.deleteChatHistory(tel)
    current_app.logger.debug(
        f"Disconnect===============Cleared chat history for {tel}")


@socketio.on('message')
def handle_user_input(data):
    if data["purpose"] == "workshop":
        ans = json.loads(data["user_message"])
        transformed_ans = transform_data(ans)
        tel = "111"
        mongo.insertChatHistory(tel, "system: 以下是针对客户所在公司的个性化问卷问题和该客户的回答, ")
        mongo.insertChatHistory(tel, transformed_ans)
        result_stream = kimi.handle_messages(
            purpose=data["purpose"], isStream=True)
        mongo.insertChatHistory(
            tel, "system: 以下是针对客户所在公司的进行数字化智能化转型的design thinking workshop. Assistant: ")
        with open('result_stream_output.txt', 'w') as file:
            for idx, chunk in enumerate(result_stream):
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                file.write(chunk_message.content)
                mongo.insertChatHistory(
                    telephone=tel, new_context=chunk_message.content)
                socketio.emit('server-message', chunk_message.content)
                time.sleep(0.1)

    elif data["purpose"] == "requirementlists":
        process_requirementlists(data)

    elif data["purpose"] == "additionalQuery":
        process_additionalQuery(data)

@socketio.on('data-ready')
def handle_data_ready(data):
    tel = data['telephone']
    session_id = mongo.getSessionIDByTelephone(tel)
    company = Company.from_dict(mongo.getCompanyByTelephone(tel))
    if company.info_collected:
        mongo.insertChatHistory(
            telephone=tel, new_context="以下是为销售人员生成的针对目标客户的需求清单: ", sessionID=session_id)
        result_stream = kimi.handle_messages(
            purpose="list", company=company, isStream=True, tel=tel)
        for idx, chunk in enumerate(result_stream):
            chunk_message = chunk.choices[0].delta
            if chunk_message.content:
                mongo.insertChatHistory(
                    telephone=tel, new_context=chunk_message.content, sessionID=session_id)
                emit('list', chunk_message.content)
                time.sleep(0.1)
        socketio.emit('message-over', "over")
        socketio.emit('setstep')


def process_additionalQuery(data):
    tel = data["telephone"]
    session_id = mongo.getSessionIDByTelephone(tel)
    print(f"Current user's session ID: {session_id}")
    result_stream = kimi.handle_messages(
        user_message=data["user_message"], purpose=data["purpose"], tel=tel, isStream=True)
    for idx, chunk in enumerate(result_stream):
        chunk_message = chunk.choices[0].delta
        print(chunk_message)
        if not chunk_message.content:
            continue
        mongo.insertChatHistory(
            telephone=tel, new_context=chunk_message.content, sessionID=session_id)
        socketio.emit('server-message', chunk_message.content)
        time.sleep(0.1)
    socketio.emit('message-over', "over")
    socketio.emit('setstep')


def process_requirementlists(data):
    tel = data["telephone"]
    session_id = mongo.getSessionIDByTelephone(tel)
    current_app.logger.debug(
        "session_id in requirementlists:%s ", session_id)
    mongo.insertChatHistory(
        tel, "user:  " + data["user_message"] + " ", session_id)
    company = Company.from_dict(mongo.getCompanyByTelephone(tel))
    company.requirements = data["user_message"]
    socketio.emit('info-collected', {'message': 'Company info collected'})


@app.route("/getGeneralQuestion", methods=["POST"])
def getGeneralQuestion():
    data = '''
[   
    {"type": "short_answer", "text":"请问您的名字是","id":0},
    {"type": "short_answer", "text":"您所在的企业主要从事哪个行业","id":1},
    {"type": "short_answer", "text":"您的工作岗位","id":2},
    {"type":"SCQ", "text":"您对以ChatGPT等为代表的生成式人工智能（AIGC）的了解程度是怎样的？", "options":["不是太清楚，刚刚接触人工智能","从媒体上知道一些常见的人工智能技术","比较熟悉，在工作中应用过人工智能技术，但对现在AIGC能做什么还不清楚","非常熟悉，已经在很多场景应用人工智能技术"],"id":3},
    {"type":"SCQ", "text":"您是否亲自使用过生成式人工智能产品", "options":["从未使用过","尝试过几次","偶尔使用，频率不高（每周1-2次或更少）","频繁使用（基本每天作为常用工具使用"],"id":4},
    {"type":"MCQ", "text":"如使用过，您都用过哪些类型的生成式人工智能产品", "options":["文本生成（如ChatGPT，文心一言等）","文本生成图片（如DALL-E，Midjourney等）","文本生成音视频（如MusicLM，Pika等）","组合应用上述服务（如ChatGPT+Midjourney）","已经应用在财务、ERP等内部系统上","噢，我没使用过"],"id":5},
    {"type":"MCQ", "text":"就目前了解的情况而言，您认为人工智能对您的企业发展的影响是", "options":["积极影响，可以帮助企业提高效率和利润","积极影响，可以创造新的业务模式或产品","中性影响，对企业发展影响不大，可有可无","消极影响，可能会导致我所在的企业竞争力下降","消极影响，可能会导致我所在的企业赛道被挤压"],"id":6},
    {"type":"MCQ", "text":"您认为哪些企业部门会受到人工智能的较大影响", "options":["决策者","研发部门","生产部门","销售部门","市场部门","客服部门","其他部门（请指明）"],"id":7},
    {"type":"MCQ", "text":"您认为企业高管应该具备哪些人工智能知识", "options":["人工智能的基本原理","人工智能对创新的驱动","应用场景","合规性、风险和挑战", "投资策略"],"id":8},
    {"type":"MCQ", "text":"您认为目前您所在企业在应用人工智能方面遇到的最大挑战是", "options":["缺少这方面的技术人才","资金成本高","信息化水平不高","不清楚用在什么地方最有效", "不清楚建设人工智能应用中的风险"],"id":9},
    {"type":"MCQ", "text":"您希望通过新的人工智能技术解决哪些企业问题", "options":["加速产品设计，满足市场需要","做决策的参谋","提高生产效率","降低生产成本，或控制成本", "结合AIGC能力，推出创新产品", "提升产品质量", "优化售后服务，加强客户运营", "优化供应链管理", "进行行业变革"],"id":10},
    {"type":"MCQ", "text":"在今年的计划中，您的企业对人工智能的预算和用途是", "options":["需要进一步了解人工智能能力之后才能确定","5-50万，我们希望先做一些边缘创新的探索","50-200万，我们已经有比较确定的场景，赶紧实现","降低生产成本，或控制成本", "200万以上，对人工智能要重度投入，包括投资"],"id":11}
]
'''
    generalQuestions = json.loads(data)
    return generalQuestions


@app.route("/getSpecializedQuestion", methods=["POST"])
def getSpecializedQuestion():
    req = request.get_json()
    tel = req['telephone']
    session_id = mongo.getSessionIDByTelephone(tel)
    current_app.logger.debug(
        "session_id in getSpecializedQuestion: %s ", session_id)
    while (sql.isCompleted(tel)):
        time.sleep(3)
    print("结束")
    company_data = mongo.getCompanyByTelephone(tel)
    print(company_data)
    company = Company.from_dict(data=company_data)
    company.info = sql.getCompanyInfoByTelephone(tel)

    print("====Answers of General Questionnaire====")
    name = ("未知", req['answers'][0]['answer'])[
        req['answers'][0]['answer'] != ""]
    print(req['answers'][2]['answer'])
    position = ("未知", req['answers'][2]['answer'])[
        req['answers'][2]['answer'] != ""]
    sql.supplement(tel, name, position)
    mongo.insertChatHistory(
        telephone=tel, new_context="system: 以下是有关生成式人工智能理解的调查问卷问题和该客户的回答, ", sessionID=session_id)
    print(req['answers'])
    transformed_req = transform_data(req['answers'])
    mongo.insertChatHistory(
        telephone=tel, new_context=transformed_req, sessionID=session_id)
    print("==============1===================")
    specialized_qestions = kimi.handle_messages(purpose="question", tel=tel)
    print(specialized_qestions)
    print("===============2===============")
    specialized_qestions = transform_specialized_questions(
        specialized_qestions)

    return specialized_qestions


@app.route("/keywords", methods=["POST"])
def areKeywords():
    req = request.get_json()
    response = kimi.handle_messages(
        user_message=req['user_message'], purpose=req['purpose'], tel=req['telephone'])
    if response == 'True':
        process_requirementlists(req)
    else:
        socketio.emit('readyforaddQuestion')
        process_additionalQuery(req)
    return jsonify({"status": "happy"})


@app.route("/clientInfo", methods=["POST"])
def test():
    req = request.get_json()
    tel = req["telephone"]
    session_id = mongo.getSessionIDByTelephone(tel)
    company = Company()
    company.name = req['user_input']
    mongo.insertChatHistory(tel, "user: " + company.name + " ", session_id)

    company.industry = "AI咨询"
    company.info_collected = False
    collect_company_info(company.name, tel, True)
    keywords = kimi.handle_messages(purpose="demand", company=company, tel=tel)
    keywords = format_keywords(keywords)

    msg = "为确保我们能够满足[company_name]的需求，请根据我们目前的业务方向和技术能力，提出几个与潜在客户需求紧密相关的关键词。可从下面提示中选取关键词，也可以自己写关键词：\n"
    msg = msg.replace("[company_name]", company.name)
    for i in range(len(keywords)):
        if i != len(keywords) - 1:
            msg += keywords[i] + ", "
        else:
            msg += keywords[i]
    mongo.insertChatHistory(tel, "assistant: " + msg + "。 ", session_id)

    return jsonify({"status": "processing", "message": msg})


def collect_company_info(name: str, tel: str, isRegister: bool):
    print(name+"   "+tel)
    company_info = kimi.handle_messages(
        user_message=name, purpose="collect", tel=tel)
    session_id = mongo.getSessionIDByTelephone(tel)
    mongo.insertChatHistory(tel, new_context="assistant: 以下是客户公司的详细信息: " + company_info + " ",
                            sessionID=session_id, company=Company(name=name, info=company_info, info_collected=True).to_dict())
    return company_info


def after_collect(name, telephone, isRegister):
    company_info = collect_company_info(name, telephone, isRegister)
    print(company_info)
    sql.insertCompanyInfo(telephone, company_info, app)
    sql.updateStauts(telephone, app)


@app.route("/getTimetable", methods=["POST"])
def getTimetable():
    req = request.get_json()
    tel = req['telephone']
    session_id = mongo.getSessionIDByTelephone(tel)
    company = Company.from_dict(mongo.getCompanyByTelephone(tel))
    transformed_ans = transform_data(req['questions'])
    mongo.insertQuestions(req['questions'], tel)
    mongo.insertChatHistory(
        tel, "system: 以下是针对客户所在公司的个性化问卷问题和该客户的回答, ", session_id)
    mongo.insertChatHistory(tel, transformed_ans, session_id)
    timetable = kimi.handle_messages(
        purpose="workshop", tel=tel, company=company)
    print("timetale======================"+timetable)
    result = timetable_data_jsonify(timetable)
    mongo.insertTimetable(result, telephone=tel)
    print(result)
    result_str = '\n'.join(
        f"Activity: {activity['activity']}, Description: {activity['description']}, Time: {activity['time']}"
        for activity in result
    )

    mongo.insertChatHistory(
        tel, "system: 以下是针对客户所在公司的进行数字化智能化转型的design thinking workshop. Assistant: " + result_str + " ", session_id)
    return jsonify({"timetable": result})


@app.route("/register", methods=['POST'])
def register():
    req = request.get_json()
    telephone = req["telephone"]
    result = sql.isTelephoneExist(telephone)
    if result is None:
        company_name = req["compName"]
        identity = req["idCode"]
        user_type = (identity == "ai4c0621")
        if not user_type:
            Thread(target=after_collect, args=(
                company_name, telephone, True)).start()
        sql.addUser(telephone, company_name, user_type)
        if (user_type):
            print(user_type)
            sql.changeStatus(telephone)
        return jsonify({'msg': 'True', 'status': 200, 'UserType': (0, 1)[user_type]})
    else:
        return jsonify({'msg': 'False', 'status': 1002, "Error": "账号已存在"})


@app.route("/login", methods=['POST'])
def login():
    req = request.get_json()
    telephone = req["telephone"]
    result = sql.isTelephoneExist(telephone)
    if result is None:
        return jsonify({'msg': 'False', 'status': 1001, "Error": "账号不存在"})
    else:
        return jsonify({'msg': 'success', 'status': 200, "UserType": result[2]})


@app.route("/getUsers", methods=['POST'])
def getUsers():
    results = sql.selectCustomers()
    users = []
    for result in results:
        user = User(result[0], result[1], result[3], result[4])
        users.append(user)
    users_dict = [user.to_dict() for user in users]
    return jsonify({"users": users_dict})


@app.route("/insertQuestions", methods=['POST'])
def insert_Questions_mongo():
    req = request.get_json()
    questions = req['questions']
    telephone = req['telephone']
    return jsonify({"status": ("1100", "200")[mongo.insertQuestions(questions, telephone)]})


@app.route("/selectQuestions", methods=['POST'])
def select_Questionsbytel_mongo():
    req = request.get_json()
    telephone = req["telephone"]
    result = mongo.selecQuestionsByTel(telephone)
    return jsonify({"telephone": telephone, "questions": result})


@app.route("/selectTimetable", methods=['POST'])
def select_Timetablebytel_mongo():
    req = request.get_json()
    telephone = req["telephone"]
    result = mongo.selecTimetableByTel(telephone)
    return jsonify({"telephone": telephone, "timetable": result})


@app.route("/insertTimetable", methods=['POST'])
def insert_Timetable_mongo():
    req = request.get_json()
    timetable = req['timetable']
    telephone = req['telephone']
    return jsonify({"status": ("1100", "200")[mongo.insertTimetable(timetable, telephone)]})


@app.route("/getCompanyNameByTelephone", methods=['POST'])
def get_company_name_by_telephone():
    try:
        req = request.get_json()
        telephone = req.get("telephone")
        if not telephone:
            return jsonify({'message': 'Telephone number is missing', 'status': 400})

        user = sql.selectUser(telephone)
        if user is None:
            return jsonify({'message': 'User not found', 'status': 404})

        company_name = user[1]

        return jsonify({'companyName': company_name, 'status': 200})
    except Exception as e:
        return jsonify({'message': str(e), 'status': 500})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5200, debug=True, log_output=True)
