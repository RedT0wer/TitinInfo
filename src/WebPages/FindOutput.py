from Controller.Classes.StructProtein import StructProtein
from Controller.Classes.StructExon import StructExon

class FindOutputDomain:
    def __init__(self, StructProtein):
        self.name = StructProtein.nameObject
        self.sequense = StructProtein.origin
        self.index = StructProtein.indexAminoacid
    def __str__(self):
        return f"<span>{self.name}</span>" + \
        "<br>" +\
        f"<span style='color: black;'>{self.sequense[:self.index]}</span>" +\
        f"<span style='color: red;'>{self.sequense[self.index]}</span>" +\
        f"<span style='color: black;'>{self.sequense[self.index + 1:]}</span>"
    def __add__(self, other):
        return str(self) + other
    def __radd__(self, other):
        return other + str(self)

class FindOutputExon:
    def __init__(self, StructExon):
        self.number = StructExon.numberExon[0]
        self.sequense = StructExon.sequense
        self.index = StructExon.indexNucleotide
    def __str__(self):
        return f"<span>Экзон {self.number}</span>" + \
        "<br>" +\
        f"<span style='color: black;'>{self.sequense[:self.index[0]]}</span>" +\
        f"<span style='color: red;'>{self.sequense[self.index[0]]}</span>" +\
        f"<span style='color: black;'>{self.sequense[self.index[1] + 1:]}</span>"
    def __add__(self, other):
        return str(self) + other
    def __radd__(self, other):
        return other + str(self)