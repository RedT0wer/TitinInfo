class DeleteNucOutputDomain:
    def __init__(self, StructProtein):
        self.name = StructProtein.nameObject
        self.origin = StructProtein.origin
        self.isoform = StructProtein.isoform
        self.index = StructProtein.indexDifference
    def __str__(self):
        return f"<span>{self.name}</span>" + \
        "<br>" +\
        f"<span style='color: black;'>{self.origin[:self.index]}</span>" +\
        f"<span style='color: red;'>{self.origin[self.index:]}</span>" +\
        "<br>" + \
        f"<span style='color: black;'>{self.isoform[:self.index]}</span>" + \
        f"<span style='color: blue;'>{self.isoform[self.index:]}</span>"
    def __add__(self, other):
        return str(self) + other
    def __radd__(self, other):
        return other + str(self)

class DeleteNucOutputExon:
    def __init__(self, StructExon):
        self.st = StructExon.numberExon[0]
        self.end = StructExon.numberExon[1]
        self.sequense = StructExon.sequense
        self.stopCodon = StructExon.stopCodon
        self.index = StructExon.indexNucleotide
    def __str__(self):
        return f"<span>Начали с Экзона {self.st}</span>" +\
        "<br>" + \
        f"<span>Закончили в Экзоне {self.end}</span>" + \
        "<br>" + \
        f"<span style='color: black;'>{self.sequense[:self.index[0]]}</span>" +\
        f"<span style='color: red;'>{self.sequense[self.index[0]]}</span>" +\
        f"<span style='color: black;'>{self.sequense[self.index[1] + 1:self.stopCodon[0]]}</span>" +\
        f"<span style='color: orange;'>{self.sequense[self.stopCodon[0]:self.stopCodon[1] + 1]}</span>" +\
        f"<span style='color: black;'>{self.sequense[self.stopCodon[1] + 1:]}</span>"
    def __add__(self, other):
        return str(self) + other
    def __radd__(self, other):
        return other + str(self)