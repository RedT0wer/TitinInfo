from PyQt5.QtCore import QThread, pyqtSignal, QObject

from BusinessLogic.Api.ManagerApi import ManagerApi
from BusinessLogic.Controller.Controller import Controller
from BusinessLogic.Controller.Function.DeleteExon import deleteExon
from BusinessLogic.Controller.Function.Find import find
from BusinessLogic.Controller.Function.Replacement import replacement
from BusinessLogic.Controller.Function.Insert import insert
from BusinessLogic.Controller.Function.DeleteNucleotide import deleteNucleotide
from BusinessLogic.Data.Data import Data
from BusinessLogic.Settings.Settings import settings
import asyncio

class Application:
    def __init__(self):
        self.ManagerApi = ManagerApi()
        self.Data = Data()
        self.Controller = Controller()
        self.FunctionObject = {
            settings.find: find,
            settings.insert: insert,
            settings.replacement: replacement,
            settings.delete_nucleotide: deleteNucleotide,
            settings.delete_exon: deleteExon,
        }

    def __parsingRequest(self, request):
        protein = request["origin"]
        nucleotides = request["isoform"]
        return (protein, nucleotides)

    def __buildingData(self, request):
        protein, nucleotides = self.__parsingRequest(request)
        if not self.Data.isValid(protein, nucleotides):
            asyncio.run(self.Data.buildingData(self.ManagerApi, protein, nucleotides))

    def getData(self, request):
        self.__buildingData(request)

        nameFunction = request["function"]
        function = self.FunctionObject[nameFunction]
        self.Controller.setFunction(function)
        return self.Controller.getResponse(self.Data, request)