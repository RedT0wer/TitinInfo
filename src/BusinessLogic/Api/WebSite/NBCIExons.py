from requests import get
import xmltodict

class NBCIExons:
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self.params = ["db=nuccore", "retmode=xml"]

    def readURL(self, identifier: str):
        response = get(f"{self.url}?{'&'.join(self.params)}&id={identifier}")
        data = response.text
        arr = xmltodict.parse(data)
        return self.processing(arr['GBSet']['GBSeq']['GBSeq_feature-table']['GBFeature'])

    def processing(self, response):
        arr = []
        for elem in response:
            if elem['GBFeature_key'] == 'exon':
                st, end = map(lambda x: int(x) - 1, elem['GBFeature_location'].split('..'))
                arr.append((st, end))
        return arr

    def getData(self, identifier: str):
        return self.readURL(identifier)

nbciExons = NBCIExons()