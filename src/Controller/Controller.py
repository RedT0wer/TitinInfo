class Controller:
    def __init__(self):
        self.function = None

    def getResponse(self, Data, request):
        return self.function.buildingResponse(Data, request)

    def setFunction(self, function):
        self.function = function