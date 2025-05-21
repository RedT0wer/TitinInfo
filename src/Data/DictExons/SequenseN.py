class SequenseN:
    def __init__(self, sequense: str):
        index_utr5 = self.createUtr5(sequense)
        index_utr3 = self.createUtr3(sequense)
        self.utr5 = sequense[:index_utr5]
        self.utr3 = sequense[index_utr3:]
        self.sequense = sequense[index_utr5:index_utr3]

    def __getitem__(self, index):
        return self.sequense[index]

    def createUtr5(self, sequense: str) -> str:
        utr5 = 0
        for i in range(len(sequense)):
            if sequense[i].islower():
                utr5 = i
            else:
                break
        return utr5 + 1

    def createUtr3(self, sequense: str) -> str:
        utr3 = 0
        for i in range(len(sequense) - 1, -1, -1):
            if sequense[i].islower():
                utr3 = i
            else:
                break
        return utr3

    def getFullSequense(self) -> str:
        return self.utr5.upper() + self.sequense + self.utr3.upper()