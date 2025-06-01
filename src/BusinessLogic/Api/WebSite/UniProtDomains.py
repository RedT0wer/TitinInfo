from requests import get

class UniProtDomains:
    def __init__(self):
        self.url = "https://rest.uniprot.org/uniprotkb/"

    def readURL(self, identifier: str):
        response = get(f"{self.url}{identifier}.json?fields=ft_domain%2Cft_region%2Cft_repeat%2Cft_coiled%2Cft_compbias")
        arr = response.json()["features"]
        return self.processing(arr)

    def processing(self, response):
        arr = []
        for dom in response:
            arr.append((dom["location"]["start"]["value"] - 1, dom["location"]["end"]["value"] - 1, dom["description"]))
        return sorted(arr)

    def getData(self, identifier: str):
        return self.readURL(identifier)

uniProtDomains = UniProtDomains()