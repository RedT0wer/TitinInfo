from requests import get
import xmltodict

class NBCISequense:
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self.params = ["db=nuccore", "retmode=xml"]

    def readURL(self, identifier: str):
        response = get(f"{self.url}?{'&'.join(self.params)}&id={identifier}")
        data = response.text
        arr = xmltodict.parse(data)
        return self.processing(arr['GBSet']['GBSeq'])

    def processing(self, response):
        seq = response['GBSeq_sequence'].upper()
        for elem in response['GBSeq_feature-table']['GBFeature']:
            if elem['GBFeature_key'] == 'CDS':
                utr5, utr3 = map(lambda x: int(x) - 1, elem['GBFeature_location'].split('..'))
                return (seq, utr5, utr3)

    def getData(self, identifier: str):
        return self.readURL(identifier)

nbciSequense = NBCISequense()