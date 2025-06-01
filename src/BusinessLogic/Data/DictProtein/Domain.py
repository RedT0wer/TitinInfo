class Domain:
    def __init__(self, sequense: str, name: str, indexSt: int, indexEnd: int):
        self.sequense = sequense
        self.name = name
        self.indexSt = indexSt
        self.indexEnd = indexEnd
    def __repr__(self):
        return f"{self.sequense}, Name={self.name}, St={self.indexSt}, End={self.indexEnd}"
    def __eq__(self, other):
        return type(self).__name__ == type(other).__name__ and self.sequense == other.sequense and self.name == other.name and self.indexSt == other.indexSt and self.indexEnd == other.indexEnd