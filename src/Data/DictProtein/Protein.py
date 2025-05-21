class Protein:
    def __init__(self, sequense: str):
        self.sequense = sequense
    def __getitem__(self, index):
        return self.sequense[index]
    def __repr__(self):
        return self.sequense