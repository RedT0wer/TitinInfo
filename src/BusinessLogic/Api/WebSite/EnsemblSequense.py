from typing import Dict
from requests import get


class EnsemblSequense:
    def __init__(self):
        self.url = "https://rest.ensembl.org/sequence/id/"
        self.params = ["mask_feature=1", "type=cdna", "content-type=application/json"]

    def readURL(self, identifier: str):
        response = get(f"{self.url}{identifier}?{';'.join(self.params)}")
        return self.processing(response.json())

    def processing(self, response: Dict):
        return (response["seq"], -1, -1)

    def getData(self, identifier: str):
        return self.readURL(identifier)

ensemblSequense = EnsemblSequense()