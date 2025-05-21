class StructProtein:
    def __init__(self, origin: str, isoform: str, nameObject: str, aminoacid: str, indexAminoacid: int, indexDifference: int):
        self.origin = origin
        self.isoform = isoform
        self.nameObject = nameObject
        self.aminoacid = aminoacid
        self.indexAminoacid = indexAminoacid
        self.indexDifference = indexDifference

    def __repr__(self):
        return f"({self.origin}, {self.isoform}, {self.nameObject}, {self.aminoacid}, {self.indexAminoacid}, {self.indexDifference})"