import aiohttp
import ssl
import xmltodict

class NBCISequense():
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self.params = ["db=nuccore", "retmode=xml"]

    async def readURL(self, identifier: str):
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}?{'&'.join(self.params)}&id={identifier}", ssl=ssl_context) as response:
                data = await response.text()
                arr = xmltodict.parse(data)
                return self.processing(arr['GBSet']['GBSeq'])

    def processing(self, response):
        seq = response['GBSeq_sequence'].upper()
        for elem in response['GBSeq_feature-table']['GBFeature']:
            if elem['GBFeature_key'] == 'CDS':
                utr5, utr3 = map(lambda x: int(x) - 1, elem['GBFeature_location'].split('..'))
                return (seq, utr5, utr3)

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

nbciSequense = NBCISequense()