class ManagerApi():
    async def getData(self, identifier: str, webSite):
        return await webSite.getData(identifier)