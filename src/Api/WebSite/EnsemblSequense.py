from typing import Dict
from Settings.NucleotideIdentifier import nucleotideIdentifier
import aiohttp
import ssl

class EnsemblSequense():
    def __init__(self):
        self.url = "https://rest.ensembl.org/sequence/id/"
        self.identifier = ''
        self.params = ["mask_feature=1", "type=cdna", "content-type=application/json"]

    async def readURL(self, identifier: str):
        self.identifier = identifier
        async with aiohttp.ClientSession() as session:
            ssl_context = ssl._create_unverified_context()
            async with session.get(f"{self.url}{identifier}?{';'.join(self.params)}", ssl=ssl_context) as response:
                return await self.processing(response.json())

    async def processing(self, response: Dict):
        seq = (await response)["seq"]
        if hasattr(nucleotideIdentifier, f"{self.identifier.lower()}_utr5"):
            seq = eval(f"nucleotideIdentifier.{self.identifier.lower()}_utr5") + seq
        return seq

    async def getData(self, identifier: str):
        return await self.readURL(identifier)

ensemblSequense = EnsemblSequense()