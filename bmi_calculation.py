import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from bmi import bmi_calc
from weight_0to3 import baby_weight_calc


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle('Randa\'s App')
        # self.setWindowIcon(QIcon('temp.png'))

        self.bmiButton.clicked.connect(self.calculate_bmi)

        self.ageButton.clicked.connect(self.calculate_baby_weight)

    def calculate_bmi(self):
        try:
            height = int(self.heightInput.text())
            weight = int(self.weightInput.text())
            bmi, health, healthy_range = bmi_calc(height, weight)
            self.bmi.setText(bmi)
            self.child_health.setText(health)
            self.healthy_range.setText(healthy_range)
        except ValueError:
            self.bmi.setText(
                'Please enter both height and weight as numbers')
            self.child_health.setText("")
            self.healthy_range.setText("")

    def calculate_baby_weight(self):
        try:
            age = int(self.ageInput.text())
            weight = int(self.weightInput.text())
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
