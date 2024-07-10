import os
from openai import OpenAI
import json
from pathlib import Path
from docx import Document
from dotenv import load_dotenv
from domain.Mongo import Mongo

load_dotenv()

mongo = Mongo()


class Kimi:
    def __init__(self):
        self.client = OpenAI(
            api_key="sk-l7SwfDjENQtiP0R7GXK0MaafaR1JP2ceEJBXP9vCkYql7DWw",
            base_url="https://api.moonshot.cn/v1",
        )

    def handle_messages(self, user_message: any = None, purpose: any = None, isStream: bool = False, company: any = None, tel: any = None):
        session_id = mongo.getSessionIDByTelephone(tel)
        with open('prompts.json', 'r', encoding='UTF-8') as file:
            prompts = json.load(file)
            match purpose:
                case "collect":
                    prompt = prompts["prompt_companyInfo"]
                case "demand":
                    prompt = prompts["prompt_demandKeywords"]
                    prompt = prompt.replace("[company_name]", company.name)
                case "list":
                    prompt = prompts["prompt_list"]
                    prompt = prompt.replace("[company_name]", company.name).replace("[company_info]", company.info).replace("[requirements]", company.requirements)
                case "question":
                    prompt = prompts["prompt_qestionsCreation"]
                case "summarize":
                    prompt = prompts["prompt_requirementsSummary"]
                case "workshop":
                    prompt = prompts["prompt_agendaCreation"]
                case "proposal":
                    prompt = prompts["prompt_proposalCreation"]
                case "additionalQuery":
                    prompt = prompts["prompt_additionalQuery"]
                case "isKeywords":
                    prompt = prompts["prompt_isKeywords"]

            messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ]
            chat_history = mongo.getChatHistory(tel)
            if chat_history != []:
                chat_history = ''.join(chat_history)
                if chat_history != []:
                    messages.append({"role": "system", "content": chat_history})

            if user_message is not None and user_message != "":
                messages.append({"role": "user", "content": user_message})
                if purpose != "collect" and chat_history != []:
                    mongo.insertChatHistory(tel, "user: " + user_message + " ", session_id)

            response = self.client.chat.completions.create(
                model="moonshot-v1-128k",
                messages=messages,
                temperature=0.3,
                stream=isStream,
            )
            

        return response if isStream else response.choices[0].message.content

    # def handle_messages(self, user_message: any = None, purpose: any = None, isStream: bool = False, company: any = None, tel: any = None):
    #     session_id = mongo.getSessionIDByTelephone(tel)
    #     with open('prompts.json', 'r', encoding='UTF-8') as file:
    #         prompts = json.load(file)
    #         match purpose:
    #             case "collect":
    #                 prompt = prompts["prompt_companyInfo"]
    #             case "demand":
    #                 prompt = prompts["prompt_demandKeywords"]
    #                 prompt = prompt.replace("[company_name]", company.name)
    #             case "list":
    #                 prompt = prompts["prompt_list"]
    #                 prompt = prompt.replace("[company_name]", company.name).replace(
    #                     "[company_info]", company.info).replace("[requirements]", company.requirements)
    #             case "question":
    #                 prompt = prompts["prompt_qestionsCreation"]
    #             case "summarize":
    #                 prompt = prompts["prompt_requirementsSummary"]
    #             case "workshop":
    #                 prompt = prompts["prompt_agendaCreation"]
    #             case "proposal":
    #                 prompt = prompts["prompt_proposalCreation"]
    #             case "additionalQuery":
    #                 prompt = prompts["prompt_additionalQuery"]
    #             case "isKeywords":
    #                 prompt = prompts["prompt_isKeywords"]
    #             case "check":
    #                 prompt = prompts["prompt_checkTimetable"]
    #         messages = [
    #             {
    #                 "role": "system",
    #                 "content": prompt,
    #             }
    #         ]
    #         chat_history = mongo.getChatHistory(tel)
    #         if chat_history != []:
    #             chat_history = ''.join(chat_history)
    #             if chat_history != []:
    #                 messages.append(
    #                     {"role": "system", "content": chat_history})

    #         if user_message is not None and user_message != "":
    #             messages.append({"role": "user", "content": user_message})
    #             if purpose != "collect" and chat_history != []:
    #                 mongo.insertChatHistory(
    #                     tel, "user: " + user_message + " ", session_id)

    #         response = self.client.chat.completions.create(
    #             model="moonshot-v1-128k",
    #             messages=messages,
    #             temperature=0.3,
    #             stream=isStream,
    #         )

    #     return response if isStream else response.choices[0].message.content
