import aiohttp
import ssl

class UniProtDomains():
    def __init__(self):
        self.url = "https://rest.uniprot.org/uniprotkb/"

    async def readURL(self, identifier: str):
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}{identifier}.json?fields=ft_domain%2Cft_region%2Cft_repeat%2Cft_coiled%2Cft_compbias", ssl=ssl_context) as response:
                arr = (await response.json())["features"]
                return self.processing(arr)

    def processing(self, response):
        arr = []
        for dom in response:
            arr.append((dom["location"]["start"]["value"] - 1, dom["location"]["end"]["value"] - 1, dom["description"]))
        return sorted(arr)

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

uniProtDomains = UniProtDomains()