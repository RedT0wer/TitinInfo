from requests import get


class EnsemblExons:
    def __init__(self):
        self.url = "https://rest.ensembl.org/lookup/id/"
        self.params = ["expand=1", "content-type=application/json"]

    def readURL(self, identifier: str):
        response = get(f"{self.url}{identifier}?{';'.join(self.params)}")
        arr = response.json()["Exon"]
        return self.processing(arr)

    def processing(self, response):
        arr = []
        value = 0
        for exon in response:
            if arr:
                value = arr[-1][1] + 1
            st,end = value, exon["end"] - exon["start"] + value
            arr.append((st, end))
        return arr

    def getData(self, identifier: str):
        return self.readURL(identifier)

ensemblExons = EnsemblExons()