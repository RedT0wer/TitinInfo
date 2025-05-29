from BusinessLogic.Controller.Classes.StructExon import StructExon
from BusinessLogic.Controller.Classes.StructProtein import StructProtein

class Replacement:
    def __init__(self):
        self.StructExon = None
        self.StructProtein = None

    def __parsingRequest(self, request):
        numNucleotide = int(request["number"]) - 1
        newNucleotide = request["nucleotide"]
        return (numNucleotide, newNucleotide)

    def __building(self, Data, request):
        numNucleotide, newNucleotide = self.__parsingRequest(request)
        self.StructExon = self.buildingStructExon(Data, numNucleotide, newNucleotide)
        self.StructProtein = self.buildingStructProtein(Data, numNucleotide, newNucleotide)

    def buildingStructExon(self, Data, numNucleotide, newNucleotide):
        indexExon = Data.getIndexExon(numNucleotide)
        exon = Data.getExon(indexExon)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotide)
        structExon = StructExon(exon.sequense, newNucleotide, indexExon + 1, -1, indexNucleotideInExon, indexNucleotideInExon, -1, -1)
        return structExon

    def buildingStructProtein(self, Data, numNucleotide, newNucleotide):
        numAminoacid = numNucleotide // 3
        indexObject = Data.getIndexObject(numAminoacid)

        arrayStructProtein = []
        protein = Data.getObject(indexObject)
        nameObject = Data.DictProtein.getFullName(indexObject)        
        aminoacid = self.createAmicoacid(Data, numNucleotide, newNucleotide)
        indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
        arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, aminoacid, indexAminoacidInDomain, -1))

        left_indexObject = indexObject
        while left_indexObject > 0:
            left_indexObject -= 1
            left = Data.getObject(indexObject - 1)
            if not left.indexSt <= numAminoacid <= left.indexEnd:
                break
            protein = left
            nameObject = Data.DictProtein.getFullName(indexObject)
            aminoacid = self.createAmicoacid(Data, numNucleotide, newNucleotide)
            indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, aminoacid, indexAminoacidInDomain, -1))

        right_indexObject = indexObject
        while right_indexObject + 1 < len(Data.DictProtein.listObject):
            right_indexObject += 1
            right = Data.getObject(right_indexObject)
            if not right.indexSt <= numAminoacid <= right.indexEnd:
                break
            protein = right
            nameObject = Data.DictProtein.getFullName(indexObject)
            aminoacid = self.createAmicoacid(Data, numNucleotide, newNucleotide)
            indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append(StructProtein(protein.sequense, "", nameObject, aminoacid, indexAminoacidInDomain, -1))
        return arrayStructProtein

    def createAmicoacid(self, Data, numNucleotide, newNucleotide):
        codon = Data.DictExons.getCodon(numNucleotide)
        codon[numNucleotide % 3] = newNucleotide
        aminoacid = Data.DictTranslation.getAminoacid("".join(codon))
        return aminoacid

    def buildingResponse(self, Data, request):
        self.__building(Data, request)
        response = {
            "function": "replacement",
            "Exon" : self.StructExon,
            "Protein" : self.StructProtein,   
        }
        return response

replacement = Replacement()