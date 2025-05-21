class StructExon:
    def __init__(self, sequense: str, nucleotide: str, startExon: int, endExon: int, indexStart: int, indexEnd: int, stStopCodon: int, endStopCodon: int):
        self.sequense = sequense
        self.nucleotide = nucleotide
        self.numberExon = (startExon, endExon)
        self.indexNucleotide = (indexStart, indexEnd)
        self.stopCodon = (stStopCodon, endStopCodon)

    def __repr__(self):
        return f"({self.sequense}, {self.nucleotide}, {self.numberExon}, {self.indexNucleotide}, {self.stopCodon})"