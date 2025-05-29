import aiohttp
import ssl

class EnsemblExons():
    def __init__(self):
        self.url = "https://rest.ensembl.org/lookup/id/"
        self.params = ["expand=1", "content-type=application/json"]

    async def readURL(self, identifier: str):
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}{identifier}?{';'.join(self.params)}", ssl=ssl_context) as response:
                arr = (await response.json())["Exon"]
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

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

ensemblExons = EnsemblExons()