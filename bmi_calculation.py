import sys
from PyQt6.QtWidgets import QApplication, QWidget, QButtonGroup, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from bmi import bmi_calc
from weight_0to3 import under3_weight_calc
from height_0to3 import under3_height_calc


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle('Doctor Randa\'s App')
        # self.setWindowIcon(QIcon('temp.png'))

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_height)

    def get_height(self):
        try:
            height = float(self.heightInput.text())
            return height
        except ValueError:
            self.bmi.setText(
                'Please set Height correctly')
            self.child_health.setText("")
            self.healthy_range.setText("")

    def get_weight(self):
        try:
            weight = float(self.weightInput.text())
            return weight

        except ValueError:
            self.bmi.setText(
                'Please set Weight correctly')
            self.child_health.setText("")
            self.healthy_range.setText("")

    def get_age(self):
        try:
            age = float(self.ageInput.text())
            year = self.yearRadioButton.isChecked()
            under3 = True
            if year and age > 3:
                under3 = False
            elif not year and age > 36:
                under3 = False
            elif under3 and year:
                age *= 12

            return age, under3

        except ValueError:
            self.bmi.setText(
                'Please set Age correctly')
            self.child_health.setText("")
            self.healthy_range.setText("")
            return None, None

    def calculate_bmi(self):

        height = self.get_height()
        weight = self.get_weight()
        if height and weight:
            bmi, health, healthy_range = bmi_calc(height, weight)
            self.bmi.setText(bmi)
            self.child_health.setText(health)
            self.healthy_range.setText(healthy_range)

    def calculate_age_weight(self):
        age, under3 = self.get_age()
        weight = self.get_weight()

        if age:
            if under3:
                under3_weight_calc(age, weight)

    def calculate_age_height(self):
        age, under3 = self.get_age()
        height = self.get_height()

        if age:
            if under3:
                under3_height_calc(age, height)


app = QApplication(sys.argv)
# app.setStyleSheet('''
#     QWidget {
#         font-size: 25px;
#     }

#     QPushButton {
#         font-size: 20px;
#     }
# ''')

window = myApp()
window.show()

app.exec()
