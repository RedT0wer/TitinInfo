from Api.WebSite.EnsemblSequense import ensemblSequense
from Api.WebSite.EnsemblExons import ensemblExons
from Api.WebSite.UniProtSequense import uniProtSequense
from Api.WebSite.UniProtDomains import uniProtDomains

class ManagerApi():
    async def getData(self, identifier: str, webSite):
        return await webSite.getData(identifier)