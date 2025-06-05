import sys
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QRadioButton, QWidget, QTableWidgetItem, QMessageBox
from BusinessLogic.Application import Application
from BusinessLogic.Settings.UrlsEnv import UrlsEnv
from FabricResponse import FabricResponse
from BusinessLogic.Settings.Settings import settings
from WebPages.ViewData.DomainsOutput import DomainsOutput
from WebPages.ViewData.ExonsOutput import ExonsOutput


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.app = Application()
        self.ui = uic.loadUi("mainwindow.ui", self)
        self.__initializationSettings()

        self.ui.table_urls.cellChanged.connect(self.handleCellChanged)

        self.ui.view_domains.clicked.connect(self.viewAllDomains)
        self.ui.view_exons.clicked.connect(self.viewAllExons)

        self.ui.pull_request.clicked.connect(self.PullRequest)

        self.ui.find.clicked.connect(self.choiseFunction)
        self.ui.replacement.clicked.connect(self.choiseFunction)
        self.ui.insert.clicked.connect(self.choiseFunction)
        self.ui.delete_nucleotide.clicked.connect(self.choiseFunction)
        self.ui.delete_exon.clicked.connect(self.choiseFunction)

        self.ui.insert_st.textChanged.connect(self.dinamicChangeNumber)
        
        self.ui.add_url.clicked.connect(self.addRowToTable)
        self.ui.remove_url.clicked.connect(self.removeSelectedRows)

    def handleCellChanged(self, row, column):
        table_widget = self.ui.table_urls
        item = table_widget.item(row, column)
        if table_widget.rowCount() != row + 1:
            if column == 1:
                id = table_widget.item(row, 0).text()
                url = item.text()
            else:
                id = item.text()
                url = table_widget.item(row, 1).text()
            UrlsEnv.add_variable_to_env_file(id, url)

    def __initializationSettings(self):
        urlsEnv = UrlsEnv()
        dictionary = urlsEnv.model_dump()
        rows_data = [(key, dictionary[key]) for key in dictionary]

        row_position = -1
        table_widget = self.ui.table_urls
        table_widget.insertRow(row_position)
        for key,value in rows_data:
            row_position += 1
            table_widget.insertRow(row_position)
            table_widget.setItem(row_position, 0, QTableWidgetItem(key))
            table_widget.setItem(row_position, 1, QTableWidgetItem(value))

    def addRowToTable(self):
        table_widget = self.ui.table_urls
        index = table_widget.rowCount() + 1
        row_data = [f'id{index}', f'url{index}']

        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)

        UrlsEnv.add_variable_to_env_file(*row_data)

        for column, data in enumerate(row_data):
            table_widget.setItem(row_position, column, QTableWidgetItem(data))

    def removeSelectedRows(self):
        table_widget = self.ui.table_urls

        selected_rows = table_widget.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(table_widget, "Предупреждение", "Нет выделенных строк для удаления.")
            return

        selected_values = self.value_selected_rows(table_widget, selected_rows)
        for column, data in selected_values:
            UrlsEnv.remove_variable_from_env_file(column)

        for row in sorted(selected_rows, reverse=True):
            table_widget.removeRow(row.row())

    def value_selected_rows(self, table_widget, selected_rows):
        selected_values = []

        for row in selected_rows:
            row_values = []
            row_index = row.row()
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row_index, column)
                if item is not None:
                    row_values.append(item.text())
                else:
                    row_values.append(None)
            selected_values.append(row_values)

        return selected_values

    def dinamicChangeNumber(self):
        integer = self.ui.insert_st.toPlainText()
        if integer.isdigit():
            self.ui.insert_end.setPlainText(str(int(integer) + 1))
        else:
            self.ui.insert_end.setPlainText('-')

    def viewAllDomains(self):
        html = DomainsOutput(self.app.Data.DictProtein)
        self.app_finished(str(html), False)

    def viewAllExons(self):
        html = ExonsOutput(self.app.Data.DictExons)
        self.app_finished(str(html), False)

    def f3(self, response):
        html = FabricResponse.getResponse(response)
        self.app_finished(html, False)

    def PullRequest(self):
        request = self.getRequest()
        self.app.finished.connect(self.f3)
        self.app.start_request(request)
        self.block_button()

    def block_button(self):
        self.ui.pull_request.setEnabled(False)
        self.ui.response_browser.setHtml("Идет чтение данных...")

    def app_finished(self, html, status):
        self.ui.response_browser.setHtml(html)
        self.ui.checkException.setChecked(status)
        self.ui.pull_request.setEnabled(True)

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
            if element.objectName() == 'insert_end':
                element.setEnabled(False)

    def getActiveButton(self):
        for button in self.ui.choise_function.findChildren(QRadioButton):
            if button.isChecked():
                return button


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    application.exec()