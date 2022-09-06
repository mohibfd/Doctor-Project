import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QDate
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt6.QtCore import QModelIndex
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from bmi_calculations import bmi_calc, under3_weight_calc, under3_height_calc, male_height_weight_calc, female_height_weight_calc

vaccine_list = [
    "Hepatite B", "Penta", "Tetra", "Prevnar 13", "Rota", "Meningo", "Priorix", "Varilix", "Hepatite A", "Typhim VI", "Papilloma virus", "Autres"
]

examination_list = [
    "examinationID", "date", "age", "height", "weight", "headCircumference", "bloodPressure", "allergy", "history", "physicalExam", "diagnostic", "treatment", "laboratory", "radiology"
]

visual_examination_list = [
    "ID", "Date", "Age", "Height", "Weight", "H C", "B P", "Allergy", "History", "Physical Exam", "Diagnostic", "Treatment", "Laboratory", "Radiology"
]


def get_vaccine(vaccine) -> str:
    if vaccine == 'Hepatite B' or vaccine == 'Hepatite A':
        vaccine = vaccine[:-2] + vaccine[-1]
    elif vaccine == 'Prevnar 13' or vaccine == 'Typhim VI':
        vaccine = vaccine[:-3] + vaccine[-2:]
    elif vaccine == 'Papilloma virus':
        vaccine = 'papiloma' + vaccine[-5].upper() + vaccine[-4:]
    vaccine = vaccine[0].lower() + vaccine[1:]
    return vaccine + '_'


class PandasModel(QAbstractTableModel):
    def __init__(self, data, id):
        super().__init__()
        self._data = data
        self.id = id

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable


class VaccineModel(PandasModel):
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value

            index_num = index.column() + 1
            vaccine = get_vaccine(vaccine_list[index.row()])
            vaccine += str(index_num)

            insert_vaccine_query = QSqlQuery()
            insert_vaccine_query.prepare(
                """
                UPDATE vaccines
                SET """ + vaccine + """ = ?
                WHERE patientID = ?
                """
            )

            insert_vaccine_query.addBindValue(value)
            insert_vaccine_query.addBindValue(self.id)
            insert_vaccine_query.exec()

            return True
        return False


class ExaminationModel(PandasModel):
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            index_row = index.row()
            index_column = index.column()
            self._data.iloc[index_row, index_column] = value

            data = examination_list[index_column]

            get_examinations_query = QSqlQuery()
            get_examinations_query.prepare(
                """
                SELECT examinationID
                FROM examinations
                WHERE patientID = ?
                """
            )
            get_examinations_query.addBindValue(self.id)
            get_examinations_query.exec()
            count = 0
            examination_id = 0
            while get_examinations_query.next():
                if count == index_row:
                    examination_id = get_examinations_query.value(0)
                    break
                count += 1

            insert_examinations_query = QSqlQuery()
            insert_examinations_query.prepare(
                """
                UPDATE examinations
                SET """ + data + """ = ?
                WHERE examinationID = ?
                """
            )

            insert_examinations_query.addBindValue(value)
            insert_examinations_query.addBindValue(examination_id)
            insert_examinations_query.exec()

            return True
        return False


class EmptyModel(PandasModel):
    def headerData(self, section, orientation, role):
        return


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("calculations/gui.ui", self)
        self.setWindowTitle("Doctor Randa\'s App")

        for i in vaccine_list:
            self.vaccineDropdown.addItem(i)

        self.vaccineDateInput.setDate(QDate.currentDate())
        self.examinationDateInput.setDate(QDate.currentDate())

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_height)
        self.addButton.clicked.connect(self.add_patient)
        self.deletePatientButton.clicked.connect(self.delete_patient)
        self.deleteExaminationButton.clicked.connect(self.delete_examination)
        self.vaccinationButton.clicked.connect(self.show_vaccination_table)
        self.addVaccineButton.clicked.connect(self.add_vaccine)
        self.examinationButton.clicked.connect(self.show_examination_table)
        self.addExaminationButton.clicked.connect(self.add_examination)

        self.vaccine_start_index = 1

        self.initialise_table()
        self.viewingExaminations = False

    def initialise_table(self) -> None:
        self.model = QSqlTableModel(self)
        self.model.setTable("patients")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "First Name")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Last Name")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "DOB")

        self.model.select()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.hideColumn(0)
        self.view.setColumnWidth(1, 110)
        self.view.setColumnWidth(2, 110)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        self.view.setModel(filter_proxy_model)
        filter_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)
        search_field = self.searchInput
        search_field.textChanged.connect(
            filter_proxy_model.setFilterRegularExpression)

    def refresh_table(self, selectedRow: QModelIndex) -> None:
        self.initialise_table()
        self.view.selectRow(selectedRow)

    def show_vaccination_table(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = index.data()
            query = QSqlQuery()
            query.prepare(
                """
                SELECT *
                FROM vaccines
                WHERE patientID = ?
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

            self.vaccine_model = VaccineModel(data, id_index)
            self.vaccinationView.setModel(self.vaccine_model)
            self.vaccine_model.setHeaderData(
                0, Qt.Orientation.Horizontal, "ID")

            self.vaccinationView.showColumn(0)
            self.vaccinationView.verticalHeader().setDefaultSectionSize(30)
            self.vaccinationView.horizontalHeader().setDefaultSectionSize(130)

            self.viewingExaminations = False

    def add_vaccine(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = index.data()
            retrieve_vaccine_query = QSqlQuery()
            retrieve_vaccine_query.prepare(
                """
                SELECT *
                FROM vaccines
                WHERE patientID = ?
                """
            )

            retrieve_vaccine_query.addBindValue(id_index)
            retrieve_vaccine_query.exec()
            retrieve_vaccine_query.first()

            vaccine = get_vaccine(self.vaccineDropdown.currentText())
            for i in range(1, 6):
                if retrieve_vaccine_query.value(vaccine + str(i)) == "":
                    break

            vaccine += str(i)
            insert_vaccine_query = QSqlQuery()
            insert_vaccine_query.prepare(
                """
                UPDATE vaccines
                SET """ + vaccine + """ = ?
                WHERE patientID = ?
                """
            )

            date = self.vaccineDateInput.date()
            insert_vaccine_query.addBindValue(date)
            insert_vaccine_query.addBindValue(id_index)
            insert_vaccine_query.exec()

            self.show_vaccination_table()

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
            return

        elif self.lastNameInput.text() == '':
            QMessageBox.warning(
                None,
                "",
                "Please enter a last name",
            )
            return

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

        select_id_query = QSqlQuery()
        select_id_query.exec("SELECT last_insert_rowid()")
        select_id_query.first()
        foreign_id = select_id_query.value(0)

        insert_vaccines_query = QSqlQuery()
        insert_vaccines_query.prepare(
            """
            INSERT INTO vaccines(patientID)
            VALUES (?)
            """
        )
        insert_vaccines_query.addBindValue(foreign_id)
        insert_vaccines_query.exec()

        self.refresh_table(row_index)
        self.show_vaccination_table()

    def show_examination_table(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = index.data()
            query = QSqlQuery()
            query.prepare(
                """
                SELECT *
                FROM examinations
                WHERE patientID = ?
                """
            )
            query.addBindValue(id_index)
            query.exec()
            rows_count = 1
            data = []
            while query.next():
                row_data = []
                for i in examination_list:
                    row_data.append(query.value(i))

                data.append(row_data)
                rows_count += 1

            data = pd.DataFrame(
                data, columns=visual_examination_list, index=range(1, rows_count))

            self.examination_model = ExaminationModel(data, id_index)
            self.vaccinationView.setModel(self.examination_model)
            self.vaccinationView.resizeColumnsToContents()
            self.vaccinationView.verticalHeader().setDefaultSectionSize(50)

            column_width = 200
            self.vaccinationView.setColumnWidth(7, 100)
            for i in range(8, 14):
                if i == 10 or i == 13:
                    self.vaccinationView.setColumnWidth(i, 130)
                else:
                    self.vaccinationView.setColumnWidth(i, column_width)

            self.vaccinationView.hideColumn(0)
            self.viewingExaminations = True

    def add_examination(self) -> None:
        index = self.get_row_index()
        if index:
            id_index = index.data()

            age_query = QSqlQuery()
            age_query.prepare(
                """
                SELECT DOB
                FROM patients
                WHERE id = ?
                """
            )
            age_query.addBindValue(id_index)
            age_query.exec()

            age_query.first()
            age_query = age_query.value(0)

            insert_examination_query = QSqlQuery()
            insert_examination_query.prepare(
                """
                INSERT INTO examinations(
                date, age, height, weight, headCircumference, bloodPressure, allergy, history, physicalExam,
                diagnostic, treatment, laboratory, radiology, patientID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            )

            year = int(age_query[:4])
            month = int(age_query[5:7])
            day = int(age_query[8:10])
            dob = datetime.datetime(year, month, day)
            date = self.examinationDateInput.date().toPyDate()
            age_years = relativedelta(date, dob).years
            age_months = relativedelta(date, dob).months
            age = ""
            if age_years >= 1:
                age = "{}Y {}M".format(str(age_years), str(age_months))
            else:
                age = "{}M".format(str(age_months))

            insert_examination_query.addBindValue(
                self.examinationDateInput.date())
            insert_examination_query.addBindValue(age)
            insert_examination_query.addBindValue(self.heightInput.text())
            insert_examination_query.addBindValue(self.weightInput.text())
            insert_examination_query.addBindValue(
                self.headCircumferenceInput.text())
            insert_examination_query.addBindValue(
                self.bloodPressureInput.text())
            insert_examination_query.addBindValue(
                self.allergyInput.toPlainText())
            insert_examination_query.addBindValue(
                self.historyInput.toPlainText())
            insert_examination_query.addBindValue(
                self.physicalExamInput.toPlainText())
            insert_examination_query.addBindValue(
                self.diagnosticInput.toPlainText())
            insert_examination_query.addBindValue(
                self.treatmentInput.toPlainText())
            insert_examination_query.addBindValue(
                self.laboratoryInput.toPlainText())
            insert_examination_query.addBindValue(
                self.radiologyInput.toPlainText())
            insert_examination_query.addBindValue(id_index)
            insert_examination_query.exec()

            self.heightInput.setText("")
            self.weightInput.setText("")
            self.headCircumferenceInput.setText("")
            self.bloodPressureInput.setText("")
            self.allergyInput.setPlainText("")
            self.historyInput.setPlainText("")
            self.physicalExamInput.setPlainText("")
            self.diagnosticInput.setPlainText("")
            self.treatmentInput.setPlainText("")
            self.laboratoryInput.setPlainText("")
            self.radiologyInput.setPlainText("")

            self.show_examination_table()

    def delete_patient(self) -> None:
        indices = self.view.selectionModel().selectedRows()
        if len(indices) == 0:
            QMessageBox.warning(
                None,
                "",
                "Please select a patient",
            )
        else:
            response = self.deletion_warning('patient', len(indices))
            if response == QMessageBox.StandardButton.Yes:
                for index in sorted(indices):
                    id_index = index.data()
                    vaccine_deletion_query = QSqlQuery()
                    vaccine_deletion_query.prepare(
                        """
                        DELETE
                        FROM vaccines
                        WHERE patientID = ?
                        """
                    )
                    vaccine_deletion_query.addBindValue(id_index)
                    vaccine_deletion_query.exec()

                    exmination_deletion_query = QSqlQuery()
                    exmination_deletion_query.prepare(
                        """
                        DELETE
                        FROM examinations
                        WHERE patientID = ?
                        """
                    )
                    exmination_deletion_query.addBindValue(id_index)
                    exmination_deletion_query.exec()

                    patient_deletion_query = QSqlQuery()
                    patient_deletion_query.prepare(
                        """
                        DELETE
                        FROM patients
                        WHERE id = ?
                        """
                    )
                    patient_deletion_query.addBindValue(id_index)
                    patient_deletion_query.exec()

                self.initialise_table()
                self.searchInput.setText("")
                empty_data = pd.DataFrame()
                empty_table = EmptyModel(empty_data, None)
                self.vaccinationView.setModel(empty_table)

    def delete_examination(self) -> None:
        if self.viewingExaminations == False:
            QMessageBox.warning(
                None,
                "",
                "Please open a patient\'s examination",
            )
            return

        indices = self.vaccinationView.selectionModel().selectedRows()
        if len(indices) == 0:
            QMessageBox.warning(
                None,
                "",
                "Please select an examination",
            )
            return

        response = self.deletion_warning('examination', len(indices))
        if response == QMessageBox.StandardButton.Yes:
            for i in indices:
                id_index = i.data()

                deletion_query = QSqlQuery()
                deletion_query.prepare(
                    """
                    DELETE
                    FROM examinations
                    WHERE examinationID = ?
                    """
                )
                deletion_query.addBindValue(id_index)
                deletion_query.exec()

            self.show_examination_table()

    def deletion_warning(self, message, message_count) -> QMessageBox.StandardButton:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        if message_count == 1:
            msgBox.setText(
                "Are you sure you would like to delete this {}?".format(message))
        else:
            msgBox.setText(
                "Are you sure you would like to delete these {} {}s?".format(message_count, message))
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)

        returnValue = msgBox.exec()
        return returnValue

    def get_row_index(self) -> QModelIndex:
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
