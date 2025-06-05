from requests import get
from BusinessLogic.Settings.UrlsEnv import UrlsEnv

class UniProtDomains:
    def __init__(self):
        self.url = "https://rest.uniprot.org/uniprotkb/"

    def readURL(self, identifier: str):
        response = get(f"{self.url}{identifier}.json?{self.getFields(identifier)}")
        arr = response.json()["features"]
        return self.processing(arr)

    def getFields(self, identifier):
        urlsEnv = UrlsEnv()
        dictionary = urlsEnv.model_dump()
        return f"fields={dictionary[identifier.lower()]}" if identifier.lower() in dictionary else ''

    def processing(self, response):
        arr = []
        for dom in response:
            arr.append((dom["location"]["start"]["value"] - 1, dom["location"]["end"]["value"] - 1, dom["description"]))
        return sorted(arr)

    def getData(self, identifier: str):
        return self.readURL(identifier)

uniProtDomains = UniProtDomains()