from Api.WebSite.NBCIExons import nbciExons
from Api.WebSite.NBCISequense import nbciSequense
from Data.DictProtein.DictProtein import DictProtein
from Data.DictExons.Exon import Exon
from Data.DictExons.DictExons import DictExons
from Data.DictTranslation.DictTranslation import DictTranslation
from Api.ManagerApi import ensemblExons, ensemblSequense, uniProtDomains, uniProtSequense


class Data:
    def __init__(self):
        self.DictTranslation = DictTranslation()
        self.DictExons = None
        self.DictProtein = None
        self.__nucleotides = ""
        self.__protein = ""

    def isValid(self, protein, nucleotides):
        return protein == self.__protein and nucleotides == self.__nucleotides

    async def buildingData(self, managerApi, protein, nucleotides):
        self.__nucleotides = nucleotides
        self.__protein = protein
        self.DictExons = await self.__buildingDictExons(managerApi, nucleotides)
        self.DictProtein = await self.__buildingDictProtein(managerApi, protein)
        self.DictProtein.buildingProtein(self.DictExons, self.DictTranslation)
        self.DictProtein.buildingListObject()

    async def __buildingDictExons(self, managerApi, nucleotides):
        stream1 = await managerApi.getData(nucleotides, ensemblSequense if nucleotides.startswith('ENST') else nbciSequense)
        stream2 = await managerApi.getData(nucleotides, ensemblExons if nucleotides.startswith('ENST') else nbciExons)
        return DictExons(stream1, stream2)

    async def __buildingDictProtein(self, managerApi, protein):
        stream1 = await managerApi.getData(protein, uniProtSequense)
        stream2 = await managerApi.getData(protein, uniProtDomains)
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