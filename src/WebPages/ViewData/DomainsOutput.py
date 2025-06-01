
class DomainsOutput:
    def __init__(self, DictProtein):
        self.listObject = DictProtein.listObject

    def __str__(self):
        html = list(map(str, self.listObject))
        return "<br>".join(html)