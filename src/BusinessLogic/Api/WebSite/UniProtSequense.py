from typing import Dict
from requests import get

class UniProtSequense:
    def __init__(self):
        self.url = "https://rest.uniprot.org/uniprotkb/"

    def readURL(self, identifier: str):
        response = get(f"{self.url}{identifier}.json")
        return self.processing(response.json())

    def processing(self, response: Dict):
        return response["sequence"]["value"]

    def getData(self, identifier: str):
        return self.readURL(identifier)

uniProtSequense = UniProtSequense()