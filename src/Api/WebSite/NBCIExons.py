import aiohttp
import ssl
import xmltodict

class NBCIExons():
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self.params = ["db=nuccore", "retmode=xml"]

    async def readURL(self, identifier: str):
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}?{'&'.join(self.params)}&id={identifier}", ssl=ssl_context) as response:
                data = await response.text()
                arr = xmltodict.parse(data)
                return self.processing(arr['GBSet']['GBSeq']['GBSeq_feature-table']['GBFeature'])

    def processing(self, response):
        arr = []
        for elem in response:
            if elem['GBFeature_key'] == 'exon':
                st, end = map(lambda x: int(x) - 1, elem['GBFeature_location'].split('..'))
                arr.append((st, end))
        return arr

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

nbciExons = NBCIExons()