import sys
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QRadioButton, QWidget
from BusinessLogic.Application import Application
from FabricResponse import FabricResponse
from BusinessLogic.Settings.Settings import settings
from WebPages.ViewData.DomainsOutput import DomainsOutput
from WebPages.ViewData.ExonsOutput import ExonsOutput


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.app = Application()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.ui.view_domains.clicked.connect(self.f1)
        self.ui.view_exons.clicked.connect(self.f2)
        self.ui.pull_request.clicked.connect(self.PullRequest)
        self.ui.find.clicked.connect(self.choiseFunction)
        self.ui.replacement.clicked.connect(self.choiseFunction)
        self.ui.insert.clicked.connect(self.choiseFunction)
        self.ui.delete_nucleotide.clicked.connect(self.choiseFunction)
        self.ui.delete_exon.clicked.connect(self.choiseFunction)

    def f1(self):
        html = DomainsOutput(self.app.Data.DictProtein)
        self.app_finished(str(html), False)

    def f2(self):
        html = ExonsOutput(self.app.Data.DictExons)
        self.app_finished(str(html), False)

    def f3(self, response):
        html = FabricResponse.getResponse(response)
        self.app_finished(html, False)

    def PullRequest(self):
        request = self.getRequest()
        self.app.finished.connect(self.f3)
        self.app.start_request(request)

    def app_finished(self, html, status):
        self.ui.response_browser.setHtml(html)
        self.ui.checkException.setChecked(status)

    def getRequest(self):
        button = self.getActiveButton()
        function = button.objectName()
        if function == settings.find:
            return self.buildingRequestFind()
        elif function == settings.insert:
            return self.buildingRequestInsert()
        elif function == settings.replacement:
            return self.buildingRequestReplacement()
        elif function == settings.delete_nucleotide:
            return self.buildingRequestDeleteNucleotide()
        elif function == settings.delete_exon:
            return self.buildingRequestDeleteExon()

    def buildingRequestFind(self):
        request = {}
        request["function"] = settings.find
        request["origin"] = self.ui.origin.text()
        request["isoform"] = self.ui.isoform.text()
        request["number"] = self.ui.find_number.toPlainText()
        return request

    def buildingRequestInsert(self):
        request = {}
        request["function"] = settings.insert
        request["origin"] = self.ui.origin.text()
        request["isoform"] = self.ui.isoform.text()
        request["st"] = self.ui.insert_st.toPlainText()
        request["end"] = self.ui.insert_end.toPlainText()
        request["newSequense"] = self.ui.insert_nucleotide.toPlainText()
        return request

    def buildingRequestReplacement(self):
        request = {}
        request["function"] = settings.replacement
        request["origin"] = self.ui.origin.text()
        request["isoform"] = self.ui.isoform.text()
        request["number"] = self.ui.replacement_number.toPlainText()
        request["nucleotide"] = self.ui.replacement_nucleotide.toPlainText()
        return request

    def buildingRequestDeleteNucleotide(self):
        request = {}
        request["function"] = settings.delete_nucleotide
        request["origin"] = self.ui.origin.text()
        request["isoform"] = self.ui.isoform.text()
        request["st"] = self.ui.delete_nucleotide_st.toPlainText()
        request["end"] = self.ui.delete_nucleotide_end.toPlainText()
        return request

    def buildingRequestDeleteExon(self):
        request = {}
        request["function"] = settings.delete_exon
        request["origin"] = self.ui.origin.text()
        request["isoform"] = self.ui.isoform.text()
        request["number"] = self.ui.delete_exon_number.toPlainText()
        return request

    def choiseFunction(self):
        button = self.getActiveButton()
        self.setEnabledFalseParams()
        self.setEnabledTrueToFunction(button)

    def setEnabledFalseParams(self):
        for element in self.ui.params_request.findChildren(QWidget):
            if element.inherits("QLabel") or element.inherits("QTextEdit"):
                element.setEnabled(False)

    def setEnabledTrueToFunction(self, button):
        for element in self.ui.params_request.findChildren(QWidget):
            if (element.inherits("QLabel") or element.inherits("QTextEdit")) and button.objectName() in element.objectName():
                element.setEnabled(True)

    def getActiveButton(self):
        for button in self.ui.choise_function.findChildren(QRadioButton):
            if button.isChecked():
                return button


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    application.exec()