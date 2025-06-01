from bisect import bisect_left
from typing import List
from BusinessLogic.Data.DictExons.Exon import Exon
from BusinessLogic.Data.DictExons.SequenseN import SequenseN

class DictExons:
    def __init__(self, stream1, stream2):
        self.SequenseN = ""
        self.exons = []
        self._lastNumber = None
        self._firstNumber = None
        self.createSequense(stream1)
        self.createExons(stream2)

    def createSequense(self, stream1) -> SequenseN:
        self.SequenseN = SequenseN(*stream1)

    def createExons(self, stream2) -> List[Exon]:
        seq = self.SequenseN.getFullSequense()
        utr5 = self.getUtr5()
        utr3 = len(seq) - self.getUtr3()
        index = -1
        for st,end in stream2:
            index += 1
            if st + 1 <= utr5 <= end:
                if self._firstNumber is None: self._firstNumber = index
                exon = Exon(st, end, utr5 - st, (end - utr5 + 1) % 3, seq[st:end + 1])                   
            elif end < utr5:
                exon = Exon(st, end, 0, 0, seq[st:end + 1])
            elif st + 1 <= utr3 <= end:
                if self._lastNumber is None: self._lastNumber = index
                prev = self.exons[-1].endPhase
                exon = Exon(st, utr3 - 1, (3 - prev)%3, 0, seq[st:utr3])
            elif st > utr3:
                exon = Exon(st, end, 0, 0, seq[st:end + 1])
            else:
                prev = self.exons[-1].endPhase if self.exons else 0
                exon = Exon(st, end, (3 - prev)%3, ((end - st + 1) - (3 - prev)%3) % 3, seq[st:end + 1])
            
            self.exons.append(exon)

    def isLastNumber(self, index):
        return index >= self._lastNumber

    def isFirstNumber(self, index):
        return index <= self._firstNumber

    def indexNucleotideInExon(self, numNucleotide):
        indexExon = self.getIndexExon(numNucleotide)
        exon = self.getExon(indexExon)
        return numNucleotide + self.getUtr5() - exon.indexSt

    def globalNucleotideFromExon(self, exon, indexNucleotide):
        return indexNucleotide - self.getUtr5() + exon.indexSt

    def getCodon(self, numNucleotide: int):
        numNucleotide = (numNucleotide // 3) * 3
        return [self.SequenseN[numNucleotide], self.SequenseN[numNucleotide + 1], self.SequenseN[numNucleotide + 2]]

    def getIndexExon(self, numNucleotide: int) -> int:
        array = []
        for exon in self.exons:
            array.append(exon.indexEnd)
        return bisect_left(array, numNucleotide + self.getUtr5())

    def getExon(self, indexExon: int) -> Exon:
        return self.exons[indexExon]

    def getUtr3(self) -> int:
        return len(self.SequenseN.utr3)

    def getUtr5(self) -> int:
        return len(self.SequenseN.utr5)