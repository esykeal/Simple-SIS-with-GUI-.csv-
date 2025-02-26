import sys
import os
import config_file
import csv

from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt6 import QtWidgets
from AddDialog_folder.AddStudent_Dialog import Ui_AddStudent_Dialog
from AddDialog_folder.AddProgram_Dialog import Ui_AddProgram_Dialog
from AddDialog_folder.AddCollege_Dialog import Ui_AddCollege_Dialog
from final2 import Ui_MainWindow

#Function to create csv file
def create_csv_file(filename, fieldnames):
    if not os.path.isfile(filename):
        with open(filename, "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            print(f"✅ Created: {filename}")

#using function to create the csv files
create_csv_file(config_file.student_filename, config_file.student_fieldnames)
create_csv_file(config_file.program_filename, config_file.program_fieldnames)
create_csv_file(config_file.college_filename, config_file.college_fieldnames)

#Opens the Add Student Dialog when button is clicked
class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddStudent_Dialog()
        self.ui.setupUi(self)

        #When Save and Cancel button is clicked, call respective funtions
        self.ui.Save_button.clicked.connect(self.save_student)
        self.ui.Cancel_button.clicked.connect(self.cancel_action)

    #Funtion to cancel/close the dialog
    def cancel_action(self):
        print("Student Dialog Cancelled") #Optional
        self.reject()

    #Function to save student to csv
    def save_student(self):
        id_number = self.ui.ID_Number_input.text()
        first_name = self.ui.First_Name_input.text()
        last_name = self.ui.Last_Name_input.text()
        year_level = self.ui.Year_Level_comboBox.currentText()
        gender = self.ui.Gender_input.text()
        program_code = self.ui.Program_Code_input.text()

        csv_filename = config_file.student_filename 

        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, "a", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=config_file.student_fieldnames)

            if not file_exists:
                csv_writer.writeheader()

            csv_writer.writerow({
                "id_number": id_number,
                "first_name": first_name,
                "last_name": last_name,
                "year_level": year_level,
                "gender": gender,
                "program_code": program_code
            })

        print("Student Added")

        self.accept()
        
#Opens the Add Program Dialog when button is clicked
class AddProgramDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddProgram_Dialog()
        self.ui.setupUi(self)

        #When Save and Cancel button is clicked, call respective funtions
        self.ui.Save_button.clicked.connect(self.save_program)
        self.ui.Cancel_button.clicked.connect(self.cancel_action)

    #Funtion to cancel/close the dialog
    def cancel_action(self):
        print("Program Dialog Cancelled") #Optional
        self.reject()

    #Function to save program to csv
    def save_program(self):
        program_code = self.ui.ProgramCode_input.text()
        program_name = self.ui.ProgramName_input.text()
        college_code = self.ui.CollegeCode_input.text()

        csv_filename = config_file.program_filename

        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, "a", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=config_file.program_fieldnames)

            if not file_exists:
                csv_writer.writeheader()

            csv_writer.writerow({
                "program_code": program_code, 
                "program_name" : program_name, 
                "college_code" : college_code
                })

        print("Program Added")

        self.accept()

#Opens the Add College Dialog when button is clicked
class AddCollegeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AddCollege_Dialog()
        self.ui.setupUi(self)

        #When Save and Cancel button is clicked, call respective funtions
        self.ui.Save_button.clicked.connect(self.save_college)
        self.ui.Cancel_button.clicked.connect(self.cancel_action)

    #Funtion to cancel/close the dialog
    def cancel_action(self):
        print("College Dialog Cancelled") #Optional
        self.reject()

    #Function to save college to csv
    def save_college(self):
        college_code = self.ui.CollegeCode_input.text()
        college_name = self.ui.CollegeName_input.text()

        csv_filename = config_file.college_filename

        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, "a", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=config_file.college_fieldnames)

            if not file_exists:
                csv_writer.writeheader()

            csv_writer.writerow({
                "college_code" : college_code, 
                "college_name" : college_name
                })

        print("College Added")

        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        #nicknames for the tan;es
        self.student_table = self.ui.tableWidget
        self.program_table = self.ui.tableWidget_2
        self.college_table = self.ui.tableWidget_3

        #Set the table to stretch the columns per table
        self.student_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.program_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.college_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        #Lets you only see the sidebar with the icons only
        self.ui.sidebar_icon_with_description_widget.hide()

        #Add functionality to the exit buttons
        self.ui.exit_button.clicked.connect(QApplication.instance().quit)
        self.ui.exit_icon_only.clicked.connect(QApplication.instance().quit)

        #Add functionality to the sidebar buttons
        self.ui.students_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.programs_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.colleges_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.students_icon_only.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.programs_icon_only.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.college_icon_only.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        #When add [student, program, college] button is clicked, open the respective dialog
        self.ui.addstudent_button.clicked.connect(self.open_add_student_dialog)
        self.ui.addprogram_button.clicked.connect(self.open_add_program_dialog)
        self.ui.addcollege_button.clicked.connect(self.open_add_college_dialog)
        

    #Function to call [student, program, and college] dialog when the button is clicked
    def open_add_student_dialog(self):
        dialog = AddStudentDialog()
        dialog.exec()
    def open_add_program_dialog(self):
        dialog = AddProgramDialog()
        dialog.exec()
    def open_add_college_dialog(self):
        dialog = AddCollegeDialog()
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())