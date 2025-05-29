from BusinessLogic.Controller.Classes.StructExon import StructExon
from BusinessLogic.Controller.Classes.StructProtein import StructProtein


class DeleteNucleotide():
    def __init__(self):
        self.StructExon = None
        self.StructProtein = None

    def __parsingRequest(self, request):
        numNucleotideSt = int(request["st"]) - 1
        numNucleotideEnd = int(request["end"]) - 1
        return (numNucleotideSt, numNucleotideEnd)

    def __building(self, Data, request):
        numNucleotideSt, numNucleotideEnd = self.__parsingRequest(request)
        structExon,structProtein = self.buildingStructExon(Data, numNucleotideSt, numNucleotideEnd)
        self.StructExon = structExon
        self.StructProtein = structProtein

    def buildingStructExon(self, Data, numNucleotideSt, numNucleotideEnd):
        ans = self.checkIntersectionDomain(Data, numNucleotideSt)
        arrayStructProtein = []
        for protein,indexObject in ans:
            indexExonSt = Data.getIndexExon(numNucleotideSt)
            exon = Data.getExon(indexExonSt)
            indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotideSt)

            startS = self.calculateStart(indexNucleotideInExon, exon, protein, Data)
            sequense, prev = self.checkingStartPhase(Data, numNucleotideSt)

            indexNucleotideInExon2, oldAminoaicd, sequense = self.checkingConnectionDomain(Data, numNucleotideSt,
                                                                                           numNucleotideEnd, sequense)

            end = self.calculateEnd(sequense, startS)
            aminoacids, stopCodon = Data.DictTranslation.transaltionSequense(sequense, startS, end)
            indexExonEnd, stopCodon = self.extendTranslation(Data, indexExonSt, sequense, aminoacids, stopCodon, end)
            structExon = StructExon(sequense[len(prev):], oldAminoaicd, indexExonSt + 1, indexExonEnd,
                                    indexNucleotideInExon, indexNucleotideInExon2, stopCodon[0] - len(prev),
                                    stopCodon[1] - len(prev))

            nameObject = Data.DictProtein.getFullName(indexObject)
            general_sequense = self.findGeneralSequense(Data, exon, startS, protein)
            aminoacids = general_sequense + aminoacids
            indexDifference = self.calculIndexDifference(aminoacids, protein.sequense)
            arrayStructProtein.append(StructProtein(protein.sequense, aminoacids, nameObject, "", -1, indexDifference))

        return (structExon, arrayStructProtein)

    def buildingStructExonOld(self, Data, numNucleotideSt, numNucleotideEnd):
        numAminoacid = numNucleotideSt // 3
        indexObject = Data.getIndexObject(numAminoacid)
        protein = Data.getObject(indexObject)

        indexExonSt = Data.getIndexExon(numNucleotideSt)
        exon = Data.getExon(indexExonSt)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotideSt)

        startS = self.calculateStart(indexNucleotideInExon, exon, protein, Data)
        sequense, prev = self.checkingStartPhase(Data, numNucleotideSt)

        indexNucleotideInExon2, oldAminoaicd, sequense = self.checkingConnectionDomain(Data, numNucleotideSt, numNucleotideEnd, sequense)

        end = self.calculateEnd(sequense, startS)
        aminoacids, stopCodon = Data.DictTranslation.transaltionSequense(sequense, startS, end)
        indexExonEnd, stopCodon = self.extendTranslation(Data, indexExonSt, sequense, aminoacids, stopCodon, end)
        structExon = StructExon(sequense[len(prev):], oldAminoaicd, indexExonSt + 1, indexExonEnd, indexNucleotideInExon, indexNucleotideInExon2, stopCodon[0] - len(prev), stopCodon[1] - len(prev))

        nameObject = Data.DictProtein.getFullName(indexObject)
        general_sequense = self.findGeneralSequense(Data, exon, startS, protein)
        aminoacids  = general_sequense + aminoacids
        indexDifference = self.calculIndexDifference(aminoacids, protein.sequense)
        arrayStructProtein = self.checkIntersectionDomain(Data, numNucleotideSt)
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

    def checkingStartPhase(self, Data, numNucleotideSt):
        indexExonSt = Data.getIndexExon(numNucleotideSt)
        exon = Data.getExon(indexExonSt)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotideSt)
        if indexNucleotideInExon < exon.startPhase:
            prev_exon = Data.getExon(indexExonSt - 1)
            prev = prev_exon.sequense[len(prev_exon.sequense) - prev_exon.endPhase:]
            return (prev, prev)
        else:
            return ("", "")

    def checkingConnectionDomain(self, Data, numNucleotideSt, numNucleotideEnd, sequense):
        indexExonSt = Data.getIndexExon(numNucleotideSt)
        exon = Data.getExon(indexExonSt)
        indexNucleotideInExon = Data.indexNucleotideInExon(numNucleotideSt)
        indexExonSt2 = Data.getIndexExon(numNucleotideEnd)
        indexNucleotideInExon2 = Data.indexNucleotideInExon(numNucleotideEnd)
        if indexExonSt == indexExonSt2:
            oldAminoaicd = exon.sequense[indexNucleotideInExon:indexNucleotideInExon2 + 1]
            sequense += exon.sequense[:indexNucleotideInExon] + exon.sequense[indexNucleotideInExon2 + 1:]
        else:
            sequense = exon.sequense[:indexNucleotideInExon]
            oldAminoaicd = exon.sequense[indexNucleotideInExon:]
            exon2 = Data.getExon(indexExonSt2)
            sequense += exon2.sequense[indexNucleotideInExon2 + 1:]
            oldAminoaicd += exon2.sequense[:indexNucleotideInExon2]
        return indexNucleotideInExon2, oldAminoaicd, sequense

    def calculateStart(self, indexNucleotideInExon, exon, protein, Data):
        if indexNucleotideInExon < exon.startPhase:
            return 0
        else:
            return max(exon.indexSt + exon.startPhase, protein.indexSt * 3 + Data.DictExons.getUtr5()) - exon.indexSt

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
        return indexExonEnd, stopCodon

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
            "function": "delete_nucleotide",
            "Exon" : self.StructExon,
            "Protein" : self.StructProtein,
        }
        return response

deleteNucleotide = DeleteNucleotide()