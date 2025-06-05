
class ExonsOutput:
    def __init__(self, DictExons):
        self.sequense = DictExons.SequenseN
        self.exons = DictExons.exons
        self.utr5 = DictExons.getUtr5()
        self.utr3 = DictExons.getUtr3()
        self._lastNumber = DictExons._lastNumber
        self._firstNumber = DictExons._firstNumber

    def __str__(self):
        html = [f"<span>Exon {i + 1} {self.exons[i].sequense}</span>" for i in range(len(self.exons))]
        if not self._firstNumber is None:
            for i in range(self._firstNumber):
                html[i] = f"<span style='color: red;'>Exon {i + 1} {self.exons[i].sequense}</span>"

            i = self._firstNumber
            index = self.utr5 - self.exons[i].indexSt
            html[i] = f"<span style='color: red;'>Exon {i + 1} {self.exons[i].sequense[:index]}</span>" + \
                  f"<span style='color: black;'>{self.exons[i].sequense[index:]}</span>"

        return "<br>".join(html)