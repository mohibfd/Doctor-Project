import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
from calculations import bmi_calc, under3_weight_calc, under3_height_calc, male_height_weight_calc, female_height_weight_calc


class myApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("calculations/gui.ui", self)
        self.setWindowTitle("Doctor Randa\'s App")

        self.bmiButton.clicked.connect(self.calculate_bmi)
        self.weightAgeButton.clicked.connect(self.calculate_age_weight)
        self.heightAgeButton.clicked.connect(self.calculate_age_height)

    def get_height(self):
        try:
            height = float(self.heightInput.text())
            return height
        except ValueError:
            self.bmi.setText(
                "Please set Height correctly")
            self.reset_labels(2)

    def get_weight(self):
        try:
            weight = float(self.weightInput.text())
            return weight

        except ValueError:
            self.bmi.setText(
                "Please set Weight correctly")
            self.reset_labels(2)

    def get_age(self):
        try:
            age = float(self.ageInput.text())
            year = self.yearRadioButton.isChecked()
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
        female = self.femaleRadioButton.isChecked()
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
