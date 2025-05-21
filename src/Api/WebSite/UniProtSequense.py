from typing import Dict
import aiohttp
import ssl

class UniProtSequense():
    def __init__(self):
        self.url = "https://rest.uniprot.org/uniprotkb/"

    async def readURL(self, identifier: str):
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}{identifier}.json", ssl=ssl_context) as response:
                return await self.processing(response.json())

    async def processing(self, response: Dict):
        return (await response)["sequence"]["value"]

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

uniProtSequense = UniProtSequense()