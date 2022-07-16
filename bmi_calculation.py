import sys
from PyQt6.QtWidgets import QApplication, QWidget, QButtonGroup, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from bmi import bmi_calc
from weight_0to3 import baby_weight_calc


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle('Doctor Randa\'s App')
        # self.setWindowIcon(QIcon('temp.png'))

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_weight)

    def calculate_bmi(self):
        try:
            height = float(self.heightInput.text())
            weight = float(self.weightInput.text())
            bmi, health, healthy_range = bmi_calc(height, weight)
            self.bmi.setText(bmi)
            self.child_health.setText(health)
            self.healthy_range.setText(healthy_range)
        except ValueError:
            self.bmi.setText(
                'Please enter both height and weight as numbers')
            self.child_health.setText("")
            self.healthy_range.setText("")

    def calculate_age_weight(self):
        try:
            age = float(self.ageInput.text())
            year = float(self.yearRadioButton.isChecked())
            baby = True
            if year and age > 3:
                baby = False
            elif not year and age > 36:
                baby = False
            elif baby and year:
                age *= 12

            weight = float(self.weightInput.text())

            if baby:
                baby_weight_calc(age, weight)
        except ValueError:
            self.bmi.setText(
                'Please enter age as a number')
            self.child_health.setText("")
            self.healthy_range.setText("")


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
