import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from calculations import bmi_calc, under3_weight_calc, under3_height_calc, male_height_weight_calc, female_height_weight_calc


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("calculations/gui.ui", self)
        self.setWindowTitle("Doctor Randa\'s App")

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_height)
        self.addButton.clicked.connect(self.add_to_database)
        self.deleteButton.clicked.connect(self.delete_from_database)

        self.initialise_table()

    def initialise_table(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("patients")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        # self.model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
        # self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Name")
        # self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Job")
        # self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Email")
        self.model.select()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

    def add_to_database(self):

        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """
            INSERT INTO patients(
                firstName,
                lastName,
                DOB
            )
            VALUES (?, ?, ?)
            """
        )

        insertDataQuery.addBindValue(self.firstNameInput.text())
        insertDataQuery.addBindValue(self.lastNameInput.text())
        insertDataQuery.addBindValue(self.DOBInput.date())
        insertDataQuery.exec()

        self.initialise_table()

    def delete_from_database(self):
        indices = self.view.selectionModel().selectedRows()
        for index in sorted(indices):
            self.model.removeRow(index.row())

        self.initialise_table()

    def get_height(self):
        try:
            height = float(self.heightInputBMI.text())
            return height
        except ValueError:
            self.bmi.setText(
                "Please set Height correctly")
            self.reset_labels(2)

    def get_weight(self):
        try:
            weight = float(self.weightInputBMI.text())
            return weight

        except ValueError:
            self.bmi.setText(
                "Please set Weight correctly")
            self.reset_labels(2)

    def get_age(self):
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

    def get_gender(self):
        female = self.femaleRadioButtonBMI.isChecked()
        return female

    def reset_labels(self, num):
        if num > 1:
            self.child_health.setText("")
            self.healthy_range.setText("")
        if num > 2:
            self.bmi.setText("")

    def calculate_bmi(self):
        weight = self.get_weight()
        height = self.get_height()
        if height and weight:
            bmi, health, healthy_range = bmi_calc(height, weight)
            self.bmi.setText(bmi)
            self.child_health.setText(health)
            self.healthy_range.setText(healthy_range)

    def calculate_age_weight(self):
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

    def calculate_age_height(self):
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


def createConnection():
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


def create_new_table():
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            firstName VARCHAR(30) NOT NULL,
            lastName VARCHAR(30) NOT NULL,
            DOB DATE,
            hepatiteB_1 DATE,
            hepatiteB_2 DATE,
            hepatiteB_3 DATE,
            hepatiteB_4 DATE,
            hepatiteB_5 DATE,
            penta_1 DATE,
            penta_2 DATE,
            penta_3 DATE,
            penta_4 DATE,
            penta_5 DATE,
            tetra_1 DATE,
            tetra_2 DATE,
            tetra_3 DATE,
            tetra_4 DATE,
            tetra_5 DATE,
            prevnar13_1 DATE,
            prevnar13_2 DATE,
            prevnar13_3 DATE,
            prevnar13_4 DATE,
            prevnar13_5 DATE,
            rota_1 DATE,
            rota_2 DATE,
            rota_3 DATE,
            rota_4 DATE,
            rota_5 DATE,
            meningo_1 DATE,
            meningo_2 DATE,
            meningo_3 DATE,
            meningo_4 DATE,
            meningo_5 DATE,
            priorix_1 DATE,
            priorix_2 DATE,
            priorix_3 DATE,
            priorix_4 DATE,
            priorix_5 DATE,
            varilix_1 DATE,
            varilix_2 DATE,
            varilix_3 DATE,
            varilix_4 DATE,
            varilix_5 DATE,
            hepatiteA_1 DATE,
            hepatiteA_2 DATE,
            hepatiteA_3 DATE,
            hepatiteA_4 DATE,
            hepatiteA_5 DATE,
            typhimVI_1 DATE,
            typhimVI_2 DATE,
            typhimVI_3 DATE,
            typhimVI_4 DATE,
            typhimVI_5 DATE,
            papilomaVirus_1 DATE,
            papilomaVirus_2 DATE,
            papilomaVirus_3 DATE,
            papilomaVirus_4 DATE,
            papilomaVirus_5 DATE
        )
        """
    )


def drop_table():
    dropTableQuery = QSqlQuery()
    dropTableQuery.exec(
        """
    DROP TABLE patients
    """
    )


# create_new_table()
# drop_table()

window = myApp()
window.show()

sys.exit(app.exec())
