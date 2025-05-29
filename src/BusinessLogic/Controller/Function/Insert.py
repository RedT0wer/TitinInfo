from BusinessLogic.Controller.Classes.StructExon import StructExon
from BusinessLogic.Controller.Classes.StructProtein import StructProtein

class Insert:
    def __init__(self):
        self.StructExon = None
        self.StructProtein = None

    def __parsingRequest(self, request):
        numNucleotide = int(request["st"]) - 1
        seqNewNucleotide = request["newSequense"]
        return (numNucleotide, seqNewNucleotide)

    def __building(self, Data, request):
        numNucleotide, seqNewNucleotide = self.__parsingRequest(request)
        structExon,structProtein = self.buildingStructs(Data, numNucleotide, seqNewNucleotide)
        self.StructExon = structExon
        self.StructProtein = structProtein

    def buildingStructs(self, Data, numNucleotide, seqNewNucleotide):
        ans = self.checkIntersectionDomain(Data, numNucleotide)
        arrayStructProtein = []
        for protein,indexObject in ans:
            indexExonSt = Data.getIndexExon(numNucleotide)
            exon = Data.getExon(indexExonSt)
            indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotide)

            sequense = self.constructSequence(exon, indexNucleotideInExon, seqNewNucleotide)
            startS, end = self.calculateStartEnd(Data, exon, protein, sequense)

            aminoacids, stopCodon = self.translateSequence(Data, sequense, startS, end)
            indexExonEnd, stopCodon, sequense, aminoacids = self.extendTranslation(Data, indexExonSt, sequense, aminoacids, stopCodon, end)

            structExon = StructExon(sequense,"",indexExonSt + 1,indexExonEnd,indexNucleotideInExon + 1,indexNucleotideInExon + len(seqNewNucleotide),stopCodon[0],stopCodon[1])

            nameObject = Data.DictProtein.getFullName(indexObject)
            general_sequense = self.findGeneralSequense(Data, exon, startS, protein)
            aminoacids = general_sequense + aminoacids
            indexDifference = self.calculIndexDifference(aminoacids, protein.sequense)

            arrayStructProtein.append(StructProtein(protein.sequense, aminoacids, nameObject, "", -1, indexDifference))

        return (structExon, arrayStructProtein)

    def buildingStructsOld(self, Data, numNucleotide, seqNewNucleotide):
        numAminoacid = numNucleotide // 3
        indexObject = Data.getIndexObject(numAminoacid)
        protein = Data.getObject(indexObject)

        indexExonSt = Data.getIndexExon(numNucleotide)
        exon = Data.getExon(indexExonSt)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotide)

        sequense = self.constructSequence(exon, indexNucleotideInExon, seqNewNucleotide)
        startS, end = self.calculateStartEnd(Data, exon, protein, sequense)

        aminoacids, stopCodon = self.translateSequence(Data, sequense, startS, end)
        indexExonEnd, stopCodon, sequense, aminoacids, stopCodon = self.extendTranslation(Data, indexExonSt, sequense, aminoacids, stopCodon, end)

        structExon = StructExon(sequense,"",indexExonSt + 1,indexExonEnd,indexNucleotideInExon + 1,indexNucleotideInExon + len(seqNewNucleotide),stopCodon[0],stopCodon[1])

        nameObject = Data.DictProtein.getFullName(indexObject)
        general_sequense = self.findGeneralSequense(Data, exon, startS)
        aminoacids = general_sequense + aminoacids
        indexDifference = self.calculIndexDifference(aminoacids, protein.sequense)

        arrayStructProtein = []
        arrayStructProtein.append(StructProtein(protein.sequense, aminoacids, nameObject, "", -1, indexDifference))

        return (structExon, arrayStructProtein)

    def checkIntersectionDomain(self, Data, numNucleotide):
        numAminoacid = numNucleotide // 3
        indexObject = Data.getIndexObject(numAminoacid)

        arrayStructProtein = []
        protein = Data.getObject(indexObject)
        # nameObject = Data.DictProtein.getFullName(indexObject)
        # indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
        arrayStructProtein.append((protein, indexObject))

        left_indexObject = indexObject
        while left_indexObject > 0:
            left_indexObject -= 1
            left = Data.getObject(indexObject - 1)
            if not left.indexSt <= numAminoacid <= left.indexEnd:
                break
            protein = left
            # nameObject = Data.DictProtein.getFullName(left_indexObject)
            # indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append((protein, left_indexObject))

        right_indexObject = indexObject
        while right_indexObject + 1 < len(Data.DictProtein.listObject):
            right_indexObject += 1
            right = Data.getObject(right_indexObject)
            if not right.indexSt <= numAminoacid <= right.indexEnd:
                break
            protein = right
            # nameObject = Data.DictProtein.getFullName(right_indexObject)
            # indexAminoacidInDomain = Data.indexAminoacidInDomain(protein, numAminoacid)
            arrayStructProtein.append((protein, right_indexObject))
        return arrayStructProtein

    def constructSequence(self, exon, indexNucleotideInExon, seqNewNucleotide):
        return exon.sequense[:indexNucleotideInExon + 1] + seqNewNucleotide + exon.sequense[indexNucleotideInExon + 1:]

    def calculateStartEnd(self, Data, exon, protein, sequense):
        startS = max(exon.indexSt + exon.startPhase, protein.indexSt * 3 + Data.DictExons.getUtr5()) - exon.indexSt
        end = len(sequense) - (len(sequense) - startS) % 3 - 3
        return startS, end

    def translateSequence(self, Data, sequense, start, end):
        return Data.DictTranslation.transaltionSequense(sequense, start, end)

    def extendTranslation(self, Data, indexExonSt, sequense, aminoacids, stopCodon, end):
        indexExonEnd = indexExonSt + 1
        while stopCodon == (-1, -1) and not Data.DictExons.isLastNumber(indexExonEnd):
            next_exon = Data.getExon(indexExonEnd)
            sequense += next_exon.sequense
            start = end + 3
            end = len(sequense) - (len(sequense) - start) % 3 - 3
            dop_aminoacids, stopCodon = self.translateSequence(Data, sequense, start, end)
            aminoacids += dop_aminoacids
            indexExonEnd += 1
        return indexExonEnd, stopCodon, sequense, aminoacids

    def findGeneralSequense(self, Data, exon, start, domain):
        numNucleotide = Data.DictExons.globalNucleotideFromExon(exon, start)
        numAminoacid = numNucleotide // 3
        start = 0
        end = numAminoacid - domain.indexSt
        return domain.sequense[start:end]

    def calculIndexDifference(self, aminoacids, origin):
        for num,tup in enumerate(zip(origin, aminoacids)):
            i,j = tup
            if i != j:
                return num
        return len(origin)

    def buildingResponse(self, Data, request):
        self.__building(Data, request)
        response = {
            "function": "insert",
            "Exon" : self.StructExon,
            "Protein" : self.StructProtein,
        }
        return response

insert = Insert()