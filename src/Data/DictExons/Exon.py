class Exon:
    def __init__(self, indexSt: int, indexEnd: int, startPhase: int, endPhase: int, sequense):
        self.indexSt = indexSt
        self.indexEnd = indexEnd
        self.startPhase = startPhase
        self.endPhase = endPhase
        self.sequense = sequense

    def __repr__(self):
        return f"({self.indexSt}, {self.indexEnd}, {self.startPhase}, {self.endPhase},{self.sequense})"