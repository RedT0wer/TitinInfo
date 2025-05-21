from Controller.Classes.StructProtein import StructProtein
from Controller.Classes.StructExon import StructExon

class Find():
    def __init__(self):
        self.StructExon = None
        self.StructProtein = None

    def __parsingRequest(self, request):
        numNucleotide = int(request["number"]) - 1
        return numNucleotide

    def __building(self, Data, request):
        numNucleotide = self.__parsingRequest(request)
        self.StructExon = self.buildingStructExon(Data, numNucleotide)
        self.StructProtein = self.buildingStructProtein(Data, numNucleotide)

    def buildingStructExon(self, Data, numNucleotide):
        indexExon = Data.getIndexExon(numNucleotide)
        exon = Data.getExon(indexExon)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotide)
        structExon = StructExon(exon.sequense, "", indexExon + 1, -1, indexNucleotideInExon, indexNucleotideInExon, -1, -1)
        return structExon

    def buildingStructProtein(self, Data, numNucleotide):
        numAminoacid = numNucleotide // 3
        indexObject = Data.getIndexObject(numAminoacid)

        arrayStructProtein = []
        protein = Data.getObject(indexObject)
        nameObject = Data.DictProtein.getFullName(indexObject)
        indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
        arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, "", indexAminoacidInDomain, -1))

        left_indexObject = indexObject
        while left_indexObject > 0:
            left_indexObject -= 1
            left = Data.getObject(indexObject - 1)
            if not left.indexSt <= numAminoacid <= left.indexEnd:
                break
            protein = left
            nameObject = Data.DictProtein.getFullName(left_indexObject)
            indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, "", indexAminoacidInDomain, -1))

        right_indexObject = indexObject
        while right_indexObject + 1 < len(Data.DictProtein.listObject):
            right_indexObject += 1
            right = Data.getObject(right_indexObject)
            if not right.indexSt <= numAminoacid <= right.indexEnd:
                break
            protein = right
            nameObject = Data.DictProtein.getFullName(right_indexObject)
            indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, "", indexAminoacidInDomain, -1))
        return arrayStructProtein

    def buildingResponse(self, Data, request):
        self.__building(Data, request)
        response = {
            "function" : "find",
            "Exon" : self.StructExon,
            "Protein" : self.StructProtein,   
        }
        return response

find = Find()