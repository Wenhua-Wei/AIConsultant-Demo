import json
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv('webapi\.env')


class Searcher:
    def __init__(self):
        self.subscriptionKey = os.getenv('BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY')
        self.endpoint = os.getenv('BING_CUSTOM_SEARCH_ENDPOINT')
        self.customConfigId = os.getenv("BING_CUSTOM_CONFIG")

    def search(self, searchTerm: str):
        headers = {"Ocp-Apim-Subscription-Key": self.subscriptionKey}
        params = {"q": searchTerm,
                  "textDecorations": True, "textFormat": "HTML"}
        print(self.endpoint)
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        pages = search_results["webPages"]
        results = pages["value"]

        for result in results[:10]:
            response = requests.get(result["url"])
            soup = BeautifulSoup(response.content, "html.parser")
            if(soup.find("body") is None): continue
            text = soup.find("body").get_text().strip()
            cleaned_text = " ".join(text.split('\n'))
            cleaned_text = " ".join(text.split())
            print(cleaned_text)
            print("=========================================")


searcher = Searcher()
searcher.search("千金药业")
