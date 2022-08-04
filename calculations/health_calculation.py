import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import pandas as pd

from bmi_calculations import bmi_calc, under3_weight_calc, under3_height_calc, male_height_weight_calc, female_height_weight_calc

vaccine_list = [
    "Hepatite B", "Penta", "Tetra", "Prevnar 13", "Rota", "Meningo", "Priorix", "Varilix", "Hepatite A", "Typhim VI", "Papilloma virus", "Autres"
]


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("calculations/gui.ui", self)
        self.setWindowTitle("Doctor Randa\'s App")

        for i in vaccine_list:
            self.vaccineDropdown.addItem(i)

        self.dateInput.setDateTime(QtCore.QDateTime.currentDateTime())

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_height)
        self.addButton.clicked.connect(self.add_patient)
        self.deleteButton.clicked.connect(self.delete_from_database)
        self.vaccinationButton.clicked.connect(self.show_vaccination_table)
        self.addVaccineButton.clicked.connect(self.add_vaccine)

        self.vaccine_start_index = 4

        self.initialise_table()

    def initialise_table(self) -> None:
        self.model = QSqlTableModel(self)
        self.model.setTable("patients")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "First Name")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Last Name")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "DOB")
        for i in range(len(vaccine_list)):
            for j in range(5):
                self.model.setHeaderData(self.vaccine_start_index + i * 5 + j,
                                         Qt.Orientation.Horizontal, vaccine_list[i] + " " + str(j+1))

        self.model.select()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.hideColumn(0)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        self.view.setModel(filter_proxy_model)
        filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)
        search_field = self.searchInput
        search_field.textChanged.connect(
            filter_proxy_model.setFilterRegularExpression)

    def refresh_table(self, selectedRow: int) -> None:
        self.initialise_table()
        self.view.selectRow(selectedRow)

    def show_vaccination_table(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = self.model.data(index)
            query = QSqlQuery()
            query.prepare(
                """
                SELECT *
                FROM patients
                WHERE patients.id = ?
                """
            )

            query.addBindValue(id_index)
            query.exec()
            query.first()

            vaccine_data = []
            for i in range(len(vaccine_list)):
                specific_vaccine_data = []
                for j in range(5):
                    specific_vaccine_data.append(
                        query.value(self.vaccine_start_index + i * 5 + j))
                vaccine_data.append(specific_vaccine_data)

            data = pd.DataFrame(
                vaccine_data, columns=range(1, 6), index=vaccine_list)

            self.vaccine_model = TableModel(data)
            self.vaccinationView.setModel(self.vaccine_model)
            self.vaccine_model.setHeaderData(
                0, Qt.Orientation.Horizontal, "ID")

    def add_vaccine(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = self.model.data(index)
            row_index = index.row()
            retrieve_vaccine_query = QSqlQuery()
            retrieve_vaccine_query.prepare(
                """
                SELECT *
                FROM patients
                WHERE id = ?
                """
            )

            retrieve_vaccine_query.addBindValue(id_index)
            retrieve_vaccine_query.exec()
            retrieve_vaccine_query.first()

            vaccine = self.vaccineDropdown.currentText()
            if vaccine == 'Hepatite B' or vaccine == 'Hepatite A':
                vaccine = vaccine[:-2] + vaccine[-1]
            elif vaccine == 'Prevnar 13' or vaccine == 'Typhim VI':
                vaccine = vaccine[:-3] + vaccine[-2:]
            elif vaccine == 'Papilloma virus':
                vaccine = vaccine[:-6] + vaccine[-5].upper() + vaccine[-4:]

            vaccine = vaccine[0].lower() + vaccine[1:]
            for i in range(1, 6):
                if retrieve_vaccine_query.value(vaccine + '_' + str(i)) == "":
                    break

            vaccine += '_' + str(i)
            insert_vaccine_query = QSqlQuery()
            insert_vaccine_query.prepare(
                """
                UPDATE patients
                SET """ + vaccine + """ = ?
                WHERE id = ?
                """
            )

            date = self.dateInput.date()
            insert_vaccine_query.addBindValue(date)
            insert_vaccine_query.addBindValue(id_index)
            insert_vaccine_query.exec()

            self.show_vaccination_table()
            self.refresh_table(row_index)

    def add_patient(self) -> None:
        if self.firstNameInput.text() == '':
            if self.lastNameInput.text() == '':
                QMessageBox.warning(
                    None,
                    "",
                    "Please enter a first name and last name",
                )
            else:
                QMessageBox.warning(
                    None,
                    "",
                    "Please enter a first name",
                )
        elif self.lastNameInput.text() == '':
            QMessageBox.warning(
                None,
                "",
                "Please enter a last name",
            )

        else:
            row_count_query = QSqlQuery()
            row_count_query.exec("SELECT COUNT(*) FROM patients")
            row_count_query.first()
            row_index = row_count_query.value(0)

            insert_patient_query = QSqlQuery()
            insert_patient_query.prepare(
                """
                INSERT INTO patients(
                    firstName,
                    lastName,
                    DOB
                )
                VALUES (?, ?, ?)
                """
            )

            insert_patient_query.addBindValue(self.firstNameInput.text())
            insert_patient_query.addBindValue(self.lastNameInput.text())
            insert_patient_query.addBindValue(self.DOBInput.date())
            insert_patient_query.exec()

            self.refresh_table(row_index)
            self.show_vaccination_table()

    def delete_from_database(self) -> None:
        indices = self.view.selectionModel().selectedRows()
        if len(indices) == 0:
            QMessageBox.warning(
                None,
                "",
                "Please select a patient",
            )
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.setText(
                "Are you sure you would like to delete this patient?")
            msgBox.setStandardButtons(
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.StandardButton.Yes:
                for index in sorted(indices):
                    self.model.removeRow(index.row())

                self.initialise_table()

    def get_row_index(self) -> int:
        try:
            index = self.view.selectionModel().selectedRows()[0]
            return index

        except IndexError:
            QMessageBox.warning(
                None,
                "",
                "Please select a patient",
            )

    def get_height(self) -> float:
        try:
            height = float(self.heightInputBMI.text())
            return height
        except ValueError:
            self.bmi.setText(
                "Please set Height correctly")
            self.reset_labels(2)

    def get_weight(self) -> float:
        try:
            weight = float(self.weightInputBMI.text())
            return weight

        except ValueError:
            self.bmi.setText(
                "Please set Weight correctly")
            self.reset_labels(2)

    def get_age(self) -> float:
        try:
            age = float(self.ageInputBMI.text())
            year = self.yearRadioButtonBMI.isChecked()
            under3 = True
            if year and age > 3:
                under3 = False
            elif not year and age > 36:
                under3 = False
                age /= 12
            elif under3 and year:
                age *= 12

            return age, under3

        except ValueError:
            self.bmi.setText(
                "Please set Age correctly")
            self.reset_labels(2)
            return None, None

    def get_gender(self) -> bool:
        female = self.femaleRadioButtonBMI.isChecked()
        return female

    def reset_labels(self, num: int) -> None:
        if num > 1:
            self.child_health.setText("")
            self.healthy_range.setText("")
        if num > 2:
            self.bmi.setText("")

    def calculate_bmi(self) -> None:
        weight = self.get_weight()
        height = self.get_height()
        if height and weight:
            bmi, health, healthy_range = bmi_calc(height, weight)
            self.bmi.setText(bmi)
            self.child_health.setText(health)
            self.healthy_range.setText(healthy_range)

    def calculate_age_weight(self) -> None:
        age, under3 = self.get_age()
        weight = self.get_weight()

        if age:
            if under3 and weight:
                under3_weight_calc(age, weight)
                self.reset_labels(3)
                return

            height = self.get_height()
            if weight or height:
                female = self.get_gender()
                if female:
                    female_height_weight_calc(age, height, weight)
                    self.reset_labels(3)
                else:
                    male_height_weight_calc(age, height, weight)
                    self.reset_labels(3)

    def calculate_age_height(self) -> None:
        age, under3 = self.get_age()
        height = self.get_height()

        if age:
            if under3:
                if height:
                    under3_height_calc(age, height)
                    self.reset_labels(3)
                return

            weight = self.get_weight()
            if weight or height:
                female = self.get_gender()
                if female:
                    female_height_weight_calc(age, height, weight)
                    self.reset_labels(3)
                else:
                    male_height_weight_calc(age, height, weight)
                    self.reset_labels(3)


def createConnection() -> None:
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("calculations/patients.sqlite")

    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)

window = myApp()
window.show()

sys.exit(app.exec())
