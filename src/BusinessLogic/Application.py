import os.path
from PyQt5.QtCore import QThread, pyqtSignal

from BusinessLogic.Api.ManagerApi import ManagerApi
from BusinessLogic.Controller.Controller import Controller
from BusinessLogic.Controller.Function.DeleteExon import deleteExon
from BusinessLogic.Controller.Function.Find import find
from BusinessLogic.Controller.Function.Replacement import replacement
from BusinessLogic.Controller.Function.Insert import insert
from BusinessLogic.Controller.Function.DeleteNucleotide import deleteNucleotide
from BusinessLogic.Data.Data import Data
from BusinessLogic.Settings.Settings import settings

class Application(QThread):
    finished = pyqtSignal(dict)
    collect = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self):
        super(Application, self).__init__()
        self.ManagerApi = ManagerApi()
        self.Data = Data()
        self.Controller = Controller()
        self.request = None
        self.operation = None
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
        type_collect_prot = os.path.isfile(protein)
        type_collect_nuc = os.path.isfile(nucleotides)
        return (protein, nucleotides, type_collect_prot, type_collect_nuc)

    def __buildingData(self, request):
        protein, nucleotides, type_collect_prot, type_collect_nuc = self.__parsingRequest(request)
        if not self.Data.isValidNucleotide(nucleotides):
            if type_collect_nuc:
                self.Data.buildingDataNucleotidePath(nucleotides)
            else:
                self.Data.buildingDataNucleotide(self.ManagerApi, nucleotides)
        if not self.Data.isValidProtein(protein):
            if type_collect_prot:
                self.Data.buildingDataProteinPath(protein)
            else:
                self.Data.buildingDataProtein(self.ManagerApi, protein)

    def run(self):
        if self.operation == 'collect_data':
            try:
                self.__buildingData(self.request)
                self.collect.emit("Данные успешно собраны")
            except Exception as e:
                self.error.emit(str(e))
        else:
            try:
                nameFunction = self.request["function"]
                function = self.FunctionObject[nameFunction]
                self.Controller.setFunction(function)
                response = self.Controller.getResponse(self.Data, self.request)
                self.finished.emit(response)
            except Exception as e:
                self.error.emit(str(e))

    def start_request(self, request):
        self.request = request
        self.operation = request['operation']
        self.start()