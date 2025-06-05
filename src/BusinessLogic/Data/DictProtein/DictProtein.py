from bisect import bisect_left
from BusinessLogic.Data.DictProtein.Protein import Protein
from BusinessLogic.Data.DictProtein.Domain import Domain
from BusinessLogic.Data.DictProtein.Connection import Connection

class DictProtein:
    def __init__(self, stream1, stream2):
        self.protein = ""
        self.listObject = []
        self.createProtein(stream1)
        self.createListObject(stream2)

    def createProtein(self, stream1):
        self.protein = Protein(stream1)

    def createListObjectOld(self, stream2):
        for st,end,name in stream2:
            if self.listObject == [] and st != 0:
                conn = Connection(self.protein[0:st], 0, st - 1)
                self.listObject.append(conn)
            elif self.listObject[-1].indexEnd + 1 < st:
                prev = self.listObject[-1]
                conn = Connection(self.protein[prev.indexEnd + 1:st], prev.indexEnd + 1, st - 1)
                self.listObject.append(conn)
            dom = Domain(self.protein[st:end + 1], name, st, end)
            self.listObject.append(dom)

    def createListObject(self, stream2):
        for st,end,name in stream2:
            dom = Domain(self.protein[st:end + 1], name, st, end)
            self.listObject.append(dom)

    def buildingListObject(self):
        arr = []
        for domain in self.listObject:
            name, seq = domain.name, domain.sequense
            index = self.protein.sequense.find(seq)
            if index == -1:
                continue
            else:
                if arr == [] and index != 0:
                    conn = Connection(self.protein[0:index], 0, index - 1)
                    arr.append(conn)
                elif arr and arr[-1].indexEnd + 1 < index:
                    prev = arr[-1]
                    conn = Connection(self.protein[prev.indexEnd + 1:index], prev.indexEnd + 1, index - 1)
                    arr.append(conn)
                dom = Domain(domain.sequense, domain.name, index, len(domain.sequense) + index - 1)
            arr.append(dom)

        last, mx = arr[-1], len(self.protein.sequense) - 1
        if last.indexEnd != mx:
            conn = Connection(self.protein[last.indexEnd + 1:mx + 1], last.indexEnd + 1, mx)
            arr.append(conn)

        self.listObject = arr

    def buildingProtein(self, DictExons, DictTranslation):
        sequense = DictExons.SequenseN.sequense
        start, end = 0, len(sequense) - 1
        self.protein = Protein(DictTranslation.transaltionSequense(sequense, start, end)[0])

    def indexAminoacidInDomain(self, domain, numAminoacid):
        return numAminoacid - domain.indexSt

    def getIndexObject(self, numAminoacid: int) -> int:
        array = []
        for obj in self.listObject:
            array.append(obj.indexEnd)
        return bisect_left(array, numAminoacid)

    def getFullName(self, indexObject):
        protein = self.getObject(indexObject)
        if hasattr(protein, 'name'):
            return protein.name
        else:
            name = []
            if indexObject != 0: name.append(self.getObject(indexObject - 1).name)
            name.append("Connection")
            if indexObject != len(self.listObject) - 1: name.append(self.getObject(indexObject + 1).name)
            return " -> ".join(name).strip()

    def getObject(self, indexObject: int):
        return self.listObject[indexObject]