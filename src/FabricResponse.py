from WebPages.DeleteExonOutput import DeleteExonOutputDomain, DeleteExonOutputExon
from WebPages.DeleteNucOutput import DeleteNucOutputDomain, DeleteNucOutputExon
from WebPages.FindOutput import FindOutputDomain,FindOutputExon
from WebPages.InsertOutput import InsertOutputDomain, InsertOutputExon
from WebPages.ReplacementOutput import ReplacementOutputDomain, ReplacementOutputExon


class FabricResponse:
    Function = {
        "find" : (FindOutputDomain, FindOutputExon),
        "insert" : (InsertOutputDomain, InsertOutputExon),
        "replacement" : (ReplacementOutputDomain, ReplacementOutputExon),
        "delete_nucleotide" : (DeleteNucOutputDomain, DeleteNucOutputExon),
        "delete_exon" : (DeleteExonOutputDomain, DeleteExonOutputExon),
    }
    @classmethod
    def getResponse(cls, response):
        function = response["function"]
        StructExon = response["Exon"]
        arrayStructProtein = response["Protein"]
        outputDomain, outputExon = cls.Function[function]
        html = []
        for StructProtein in arrayStructProtein:
            html += [outputDomain(StructProtein)]
        html += [outputExon(StructExon)]
        return "<br>".join(list(map(str, html)))