from WebPages.ResponseOutput.DeleteExonOutput import DeleteExonOutputDomain, DeleteExonOutputExon
from WebPages.ResponseOutput.DeleteNucOutput import DeleteNucOutputDomain, DeleteNucOutputExon
from WebPages.ResponseOutput.FindOutput import FindOutputDomain,FindOutputExon
from WebPages.ResponseOutput.InsertOutput import InsertOutputDomain, InsertOutputExon
from WebPages.ResponseOutput.ReplacementOutput import ReplacementOutputDomain, ReplacementOutputExon
from BusinessLogic.Settings.Settings import settings

class FabricResponse:
    Function = {
        settings.find : (FindOutputDomain, FindOutputExon),
        settings.insert : (InsertOutputDomain, InsertOutputExon),
        settings.replacement : (ReplacementOutputDomain, ReplacementOutputExon),
        settings.delete_nucleotide : (DeleteNucOutputDomain, DeleteNucOutputExon),
        settings.delete_exon : (DeleteExonOutputDomain, DeleteExonOutputExon),
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