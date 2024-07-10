from dotenv import load_dotenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
import os
import logging
import json
import random


load_dotenv('webapi\.env')


class Message:
    def __init__(self, current_app):
        self._apiUrl = os.getenv("Message_apiUrl")
        self._TemplateId = os.getenv("Messgae_templateId")
        self._SmsSdkAppId = os.getenv("Message_SDKAppId")
        self._Action = "SendSms"
        self._Version = "2021-01-11"
        self._Region = "ap-guangzhou"
        self.currentapp = current_app
        self.cred= credential.Credential(os.getenv("SecretId"), os.getenv("SecretKey"))

    def __init__(self):
        self._apiUrl = os.getenv("Message_apiUrl")
        self._TemplateId = os.getenv("Messgae_templateId")
        self._SmsSdkAppId = os.getenv("Message_SDKAppId")
        self._Action = "SendSms"
        self._Version = "2021-01-11"
        self._Region = "ap-guangzhou"
        self._SignName = "广东智用研究院"

    def sendMessage(self, telephone: str):
        PhoneNumberSet = ['+86' + telephone]
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "sms.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = sms_client.SmsClient(self.cred, self._Region, clientProfile)
            print(PhoneNumberSet)
            req = models.SendSmsRequest()
            random_number = str(random.randint(100000, 999999))
            params = {
                "Action": self._Action,
                "Version": self._Version,
                "PhoneNumberSet": PhoneNumberSet,
                "SmsSdkAppId": self._SmsSdkAppId,
                "TemplateId": self._TemplateId,
                "SignName": self._SignName,
                "TemplateParamSet": [random_number, "1"]
            }
            req.from_json_string(json.dumps(params))

            resp = client.SendSms(req)
            print(resp.to_json_string())
        except TencentCloudSDKException as err:
            # self.current_app.logger.debug(err)
            print(err)


test = Message()
test.sendMessage("13544340956")
