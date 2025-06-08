from BusinessLogic.Api.WebSite.NBCIExons import nbciExons
from BusinessLogic.Api.WebSite.NBCISequense import nbciSequense
from BusinessLogic.Data.DictProtein.DictProtein import DictProtein
from BusinessLogic.Data.DictExons.Exon import Exon
from BusinessLogic.Data.DictExons.DictExons import DictExons
from BusinessLogic.Data.DictTranslation.DictTranslation import DictTranslation
from BusinessLogic.Api.WebSite.EnsemblExons import ensemblExons
from BusinessLogic.Api.WebSite.EnsemblSequense import ensemblSequense
from BusinessLogic.Api.WebSite.UniProtSequense import uniProtSequense
from BusinessLogic.Api.WebSite.UniProtDomains import uniProtDomains


class Data:
    def __init__(self):
        self.DictTranslation = DictTranslation()
        self.DictExons = None
        self.DictProtein = None
        self.__nucleotides = ""
        self.__protein = ""

    def isValidProtein(self, protein):
        return protein == self.__protein

    def isValidNucleotide(self, nucleotides):
        return nucleotides == self.__nucleotides

    def buildingDataNucleotide(self, managerApi, nucleotides):
        self.__nucleotides = nucleotides
        self.DictExons = self.__buildingDictExons(managerApi, nucleotides)

    def buildingDataProtein(self, managerApi, protein):
        self.__protein = protein
        self.DictProtein = self.__buildingDictProtein(managerApi, protein)
        self.DictProtein.buildingProtein(self.DictExons, self.DictTranslation)
        self.DictProtein.buildingListObject()

    def buildingDataNucleotidePath(self, path):
        nucleotides = path.split('/')[-1]
        self.__nucleotides = nucleotides
        self.DictExons = self.__buildingDictExonsPath(path)

    def buildingDataProteinPath(self, path):
        protein = path.split('/')[-1]
        self.__protein = protein
        self.DictProtein = self.__buildingDictProteinPath(path)
        self.DictProtein.buildingProtein(self.DictExons, self.DictTranslation)
        self.DictProtein.buildingListObject()

    def __buildingDictExonsPath(self, path):
        with open(path, "r") as f:
            stream1 = (f.readline().strip(),-1,-1)
            stream2 = [tuple(map(int, obj.split())) for obj in f.readlines()]
        return DictExons(stream1, stream2)

    def __buildingDictProteinPath(self, path):
        with open(path, "r") as f:
            stream1 = f.readline().strip()
            stream2 = []
            for line in f.readlines():
                arr = line.split()
                st,end = map(int, arr[:2])
                name = " ".join(arr[2:])
                stream2.append((st,end,name))
        return DictProtein(stream1, stream2)

    def __buildingDictExons(self, managerApi, nucleotides):
        stream1 = managerApi.getData(nucleotides, ensemblSequense if nucleotides.startswith('ENST') else nbciSequense)
        stream2 = managerApi.getData(nucleotides, ensemblExons if nucleotides.startswith('ENST') else nbciExons)
        return DictExons(stream1, stream2)

    def __buildingDictProtein(self, managerApi, protein):
        stream1 = managerApi.getData(protein, uniProtSequense)
        stream2 = managerApi.getData(protein, uniProtDomains)
        return DictProtein(stream1, stream2)

    def indexNucleotideInExon(self, numNucleotide):
        return self.DictExons.indexNucleotideInExon(numNucleotide)

    def indexAminoacidInDomain(self, domain, numAminoacid):
        return self.DictProtein.indexAminoacidInDomain(domain, numAminoacid)

    def getFullName(self, indexObject):
        return self.DictProtein.getFullName(indexObject)

    def getIndexObject(self, numNucleotide: int) -> int:
        return self.DictProtein.getIndexObject(numNucleotide)

    def getObject(self, indexObject: int):
        return self.DictProtein.getObject(indexObject)

    def getIndexExon(self, numNucleotide: int) -> int:
        return self.DictExons.getIndexExon(numNucleotide)

    def getExon(self, indexExon: int) -> Exon:
        return self.DictExons.getExon(indexExon)