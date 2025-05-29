class Connection:
    def __init__(self, sequense: str, indexSt: int, indexEnd: int):
        self.sequense = sequense
        self.indexSt = indexSt
        self.indexEnd = indexEnd
    def __repr__(self):
        return f"{self.sequense}, Connection, {self.indexSt}, {self.indexEnd}"
    def __eq__(self, other):
        return type(self).__name__ == type(other).__name__ and self.sequense == other.sequense and self.indexSt == other.indexSt and self.indexEnd == other.indexEnd