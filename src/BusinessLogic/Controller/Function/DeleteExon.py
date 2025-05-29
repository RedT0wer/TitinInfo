from BusinessLogic.Controller.Classes.StructExon import StructExon
from BusinessLogic.Controller.Classes.StructProtein import StructProtein


class DeleteExon():
    def __init__(self):
        self.StructExon = None
        self.StructProtein = None

    def __parsingRequest(self, request):
        numNucleotide = int(request["number"]) - 1
        return numNucleotide

    def __building(self, Data, request):
        numNucleotide = self.__parsingRequest(request)
        structExon, structProtein = self.buildingStructExon(Data, numNucleotide)
        self.StructExon = structExon
        self.StructProtein = structProtein

    def buildingStructExon(self, Data, numNucleotide):
        exon_changed, numChanged, exon_for_seq = self.checkingStartExon(Data, numNucleotide) #номер в индексах как входной
        indexExonSt = Data.getIndexExon(numNucleotide)
        ans = self.checkIntersectionDomain(Data, numChanged)
        arrayStructProtein = []

        for protein, indexObject in ans:
            startS = self.calculateStart(exon_for_seq, protein, Data)
            sequense = self.constructSequense(exon_for_seq)
            end = self.calculateEnd(sequense, startS)

            aminoacids, stopCodon = self.translateSequence(Data, sequense, startS, end)
            indexExonEnd, stopCodon, sequense, aminoacids = self.extendTranslation(Data, indexExonSt, sequense, aminoacids, stopCodon, end)
            structExon = StructExon(sequense, "", indexExonSt + 1, indexExonEnd,
                                    -1, -1, stopCodon[0],
                                    stopCodon[1])

            nameObject = Data.DictProtein.getFullName(indexObject)
            general_sequense = self.findGeneralSequense(Data, protein, exon_changed, startS)
            aminoacids = general_sequense + aminoacids
            indexDifference = self.calculIndexDifference(aminoacids, protein.sequense)
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

    def checkingStartExon(self, Data, numNucleotide):
        indexExon = Data.getIndexExon(numNucleotide)
        if Data.DictExons.isFirstNumber(indexExon):
            exon_changed = Data.getExon(indexExon)
            numChanged = exon_changed.startPhase
            exon_for_seq = None
        else:
            exon = Data.getExon(indexExon - 1)
            if exon.endPhase == 0:
                exon_changed = Data.getExon(indexExon)
                numChanged = exon_changed.startPhase
                exon_for_seq = None
            else:
                exon_changed = exon
                numChanged = len(exon.sequense) - exon.endPhase
                exon_for_seq = exon
        return (exon_changed, numChanged + exon_changed.indexSt - Data.DictExons.getUtr5(), exon_for_seq)

    def calculateStart(self, exon, protein, Data):
        if exon is None:
            return 0
        else:
            return max(exon.indexSt + exon.startPhase, protein.indexSt * 3 + Data.DictExons.getUtr5()) - exon.indexSt

    def constructSequense(self, exon):
        sequense = ""
        if exon:
            sequense += exon.sequense
        return sequense

    def calculateEnd(self, sequense, start):
        return len(sequense) - (len(sequense) - start) % 3 - 3

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
        if Data.DictExons.isLastNumber(indexExonEnd) and stopCodon == (-1, -1):
            next_exon = Data.getExon(indexExonEnd)
            sequense += next_exon.sequense[:len(next_exon.sequense) - next_exon.endPhase]
            start = end + 3
            end = len(sequense) - (len(sequense) - start) % 3 - 3
            dop_aminoacids, stopCodon = self.translateSequence(Data, sequense, start, end)
            aminoacids += dop_aminoacids
            indexExonEnd += 1
        return indexExonEnd, stopCodon, sequense, aminoacids

    def findGeneralSequense(self, Data, domain, exon, start):
        numNucleotide = Data.DictExons.globalNucleotideFromExon(exon, start)
        numAminoacid = numNucleotide // 3
        start = 0
        end = numAminoacid - domain.indexSt
        return domain.sequense[start:end]

    def calculIndexDifference(self, aminoacids, origin):
        for num, tup in enumerate(zip(origin, aminoacids)):
            i, j = tup
            if i != j:
                return num
        return len(origin)

    def buildingResponse(self, Data, request):
        self.__building(Data, request)
        response = {
            "function": "delete_exon",
            "Exon": self.StructExon,
            "Protein": self.StructProtein,
        }
        return response


deleteExon = DeleteExon()