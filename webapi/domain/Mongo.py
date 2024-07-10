import pymongo
from domain.Company import Company


class Mongo:
    def __init__(self):
        myclient = pymongo.MongoClient(
            "mongodb://ai4c:Ai4c!@119.91.19.12:27017/consultant?authSource=consultant")
        self.mydb = myclient["consultant"]
        self.qcol = self.mydb['Questions']
        self.tcol = self.mydb['Timetable']
        self.scol = self.mydb['Session']
        self.ccol = self.mydb['ChatHistory']

    def insertQuestions(self, questions: list, telephone: str):
        id=0
        for question in questions:
            answer = question['answers'] if 'answers' in question else [
                question.get('answer', '')]

            question_data = {
                "telephone": telephone,
                "question_id": id,
                "question_type": question["type"],
                "question": question["subject"],
                "answer": answer,
                "status": "incomplete"
            }

            insert_result = self.qcol.insert_one(question_data)

            if insert_result.inserted_id is None:
                print(insert_result.inserted_id)
                return False
            id+=1

        update_result = self.qcol.update_many(
            {"telephone": telephone}, {"$set": {"status": "complete"}})
        return update_result.matched_count == len(questions)

    def selecQuestionsByTel(self, telephone: str):
        questions = []
        mongo_questions = self.qcol.find(
            {"telephone": telephone, "status": "complete"})
        for x in mongo_questions:
            question = self.to_questiondict(x)
            questions.append(question)
        return questions

    def insertTimetable(self, timetable: list, telephone: str):
        for row in timetable:
            row_data = {
                "telephone": telephone,
                "row_id": row.get("row_id", 0),
                "time": row["time"],
                "activity": row["activity"],
                "description": row["description"],
                "status": "incomplete"
            }
            insert_result = self.tcol.insert_one(row_data)
            if insert_result.inserted_id is None:
                return False

        update_result = self.tcol.update_many(
            {"telephone": telephone}, {"$set": {"status": "complete"}})

        return update_result.matched_count == len(timetable)

    def selecTimetableByTel(self, telephone: str):
        timetable = []
        mongo_rows = self.tcol.find(
            {"telephone": telephone, "status": "complete"})
        for row in mongo_rows:
            row = self.to_rowdict(row)
            timetable.append(row)
        return timetable

    def selectAllQuestions(self):
        return self.qcol.find()

    def to_questiondict(self, question):
        return {
            'question_id': question["question_id"],
            "question_type": question["question_type"],
            "question": question["question"],
            "answer": question["answer"]
        }

    def to_rowdict(self, row):
        return {
            "row_id": row["row_id"],
            "time": row["time"],
            "activity": row["activity"],
            "description": row["description"]
        }

    def insertChatHistory(self, telephone: str, new_context: str, sessionID: str, company:dict=None):
        document = {"sessionID":sessionID }

        if company is not None:
            document["company"] = company

        result = self.mydb['ChatHistory'].update_one(
        {"telephone": telephone},
        {
            "$push": {"contexts": new_context},
            "$set": document
        },
        upsert=True
    )
        return result.matched_count > 0 or result.upserted_id


    def getChatHistory(self, telephone: str):
        document = self.ccol.find_one(
            {"telephone": telephone}, {"_id": 0, "contexts": 1})

        if document and "contexts" in document:
            return document["contexts"]
        else:
            return []

    def deleteChatHistory(self, telephone: str):
        result = self.ccol.delete_one({"telephone": telephone})
        print(result)
        if result.deleted_count > 0:
            return True
        else:
            return False

    def getSessionIDByTelephone(self, telephone: str):
        document = self.ccol.find_one(
            {"telephone": telephone})

        if document and "sessionID" in document:
            return document["sessionID"]
        else:
            return None

    def getTelephoneBySessionID(self, session_id: str):
        document = self.ccol.find_one(
            {"sessionID": session_id}, {"telephone": 1, "_id": 0})

        if document and "telephone" in document:
            return document["telephone"]
        else:
            return None


    def getCompanyByTelephone(self, telephone:str):
        document= self.ccol.find_one({"telephone": telephone})
        return (None,document["company"])[document is not None]
        