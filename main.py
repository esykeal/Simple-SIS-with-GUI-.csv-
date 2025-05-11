import sys
import os
import config_file
import csv

from existence_checker import programName_existence, programCode_existence, collegeCode_existence, collegeName_existence, idNumber_existence

from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from PyQt6 import QtWidgets, QtCore

from rev_AddDialog_folder.rev_AddCollegeDialog_ui import Ui_Add_College_Dialog
from rev_AddDialog_folder.rev_AddProgramDialog_ui import Ui_Add_Program_Dialog
from rev_AddDialog_folder.rev_AddStudentDialog_ui import Ui_Add_Student_Dialog

from rev_EditDialog_folder.rev_EditCollegeDialog_ui import Ui_Edit_College_Dialog
from rev_EditDialog_folder.rev_EditProgramDialog_ui import Ui_Edit_Program_Dialog
from rev_EditDialog_folder.rev_EditStudentDialog_ui import Ui_Edit_Student_Dialog

from deleteItemConfirmation import Ui_DeleteConfirmation

from final2 import Ui_MainWindow

#Function to create csv file
def create_csv_file(filename, fieldnames):
    if not os.path.isfile(filename):
        with open(filename, "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            print(f" Created: {filename}")

#using function to create the csv files
create_csv_file(config_file.student_filename, config_file.student_fieldnames)
create_csv_file(config_file.program_filename, config_file.program_fieldnames)
create_csv_file(config_file.college_filename, config_file.college_fieldnames)


class Add_College_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Add_College_Dialog()
        self.ui.setupUi(self)

        self.ui.Save_button.clicked.connect(self.save_college)
        self.ui.Cancel_button.clicked.connect(self.cancel)

    def cancel(self):
        self.reject()

    def save_college(self):
        college_code = self.ui.CollegeCode_input.text()
        college_name = self.ui.CollegeName_input.text()

        if collegeCode_existence(config_file.college_filename, college_code):
            QMessageBox.warning(self, "Error", "College code already exists, please change it")
            return
        if collegeName_existence(config_file.college_filename, college_name):
            QMessageBox.warning(self, "Error", "College name already exists, please change it")
            return
        if not college_code and not college_name:
            QMessageBox.warning(self, "Error", "All field must be filled out")
            return

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
            
        self.parent().load_csv_to_table(self.parent().college_table, csv_filename, "COLLEGES")
        self.parent().sort_table()
        self.accept()


class Add_Program_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Add_Program_Dialog()
        self.ui.setupUi(self)

        self.load_college_codes()

        self.ui.Save_button.clicked.connect(self.save_program)
        self.ui.Cancel_button.clicked.connect(self.cancel)


    def load_college_codes(self):
        csv_file = config_file.college_filename
        if not os.path.isfile(csv_file):
            QMessageBox.warning(self, "Error", f"{csv_file} not found!")
            return
        
        with open(csv_file, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                college_code = row.get("college_code")
                if college_code:
                    self.ui.college_code_input_comboBox.addItem(college_code)

    def cancel(self):
        self.reject()

    def save_program(self):
        program_code = self.ui.ProgramCode_input.text()
        program_name = self.ui.ProgramName_input.text()
        college_code = self.ui.college_code_input_comboBox.currentText()

        if not program_code or not program_name or not college_code:
            QMessageBox.warning(self, "Error", "All fields must be filled")
            return
        
        if programName_existence(config_file.program_filename, program_name):
            QMessageBox.warning(self, "Error", "Program Name already exists!")
            return
        
        if programCode_existence(config_file.program_filename, program_code):
            QMessageBox.warning(self, "Error", "Program Code already exists!")
            return 
        
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

        #Reloads the table to show the added program
        self.parent().load_csv_to_table(self.parent().program_table, csv_filename, "PROGRAMS")
        self.parent().sort_table()
        self.accept()


class Add_Student_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Add_Student_Dialog()
        self.ui.setupUi(self)

        self.load_program_codes()

        self.ui.Save_button.clicked.connect(self.save_student)
        self.ui.Cancel_button.clicked.connect(self.cancel)

    def load_program_codes(self):
        csv_file = config_file.program_filename
        if not os.path.isfile(csv_file):
            QMessageBox.warning(self, "Error", f"{csv_file} not found!")
            return
        
        with open(csv_file, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                program_code = row.get("program_code")
                if program_code:
                    self.ui.program_code_input_comboBox.addItem(program_code)

    def cancel(self):
        self.reject()

    def save_student(self):
        id_number = self.ui.id_number_input.text()
        first_name = self.ui.first_name_input.text()
        last_name = self.ui.last_name_input.text()
        gender = self.ui.gender_comboBox.currentText()
        year_level = self.ui.year_level_comboBox.currentText()
        program_code = self.ui.program_code_input_comboBox.currentText()

        if not all([id_number, first_name, last_name, year_level, gender, program_code]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return
        
        if idNumber_existence(config_file.student_filename, id_number):
            QMessageBox.warning(self, "Error", "ID Number already exists")
            return
        
        if not programCode_existence(config_file.program_filename, program_code):
            QMessageBox.warning(self, "Error", "Program Code doesn't exists! Enter a valid program code")
            return

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
                "gender": gender,
                "year_level": year_level,
                "program_code": program_code
            })

        #Reloads the table to show the added student
        self.parent().load_csv_to_table(self.parent().student_table, csv_filename, "STUDENTS")
        self.parent().sort_table()
        self.accept()


class Edit_College_Dialog(QDialog):
    def __init__(self, parent, row_data, row_index):
        super().__init__(parent)
        self.ui = Ui_Edit_College_Dialog()
        self.ui.setupUi(self)
        self.row_index = row_index
        self.parent = parent
        self.old_college_code = row_data[0]
        self.old_college_name = row_data[1]

        self.ui.college_code_input.setText(row_data[0])
        self.ui.college_name_input.setText(row_data[1])

        self.ui.Save_button.clicked.connect(self.save_changes)
        self.ui.Cancel_button.clicked.connect(self.reject)

    def save_changes(self):
        new_college_code = self.ui.college_code_input.text().strip()
        new_college_name = self.ui.college_name_input.text().strip()

        if not new_college_code or not new_college_name:
            QMessageBox.warning(self, "Error", "Fields cannot be empty!")
            return

        if new_college_code == self.old_college_code:
            pass
        else:
            if collegeCode_existence(config_file.college_filename, new_college_code):
                QMessageBox.warning(self, "Error", "College code already exists!")
                return
            
        if new_college_name == self.old_college_name:
            pass
        else:
            if collegeName_existence(config_file.college_filename, new_college_name):
                QMessageBox.warning(self, "Error", "College already exists!")
                return
            
        filename = config_file.college_filename

        with open(filename, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        if 1 <= self.row_index < len(data):
            data[self.row_index] = [new_college_code, new_college_name]

        with open(filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(data)

        if new_college_code != self.old_college_code:
            self.update_program_college_codes(self.old_college_code, new_college_code)
            self.parent.load_csv_to_table(self.parent.program_table, config_file.program_filename, "PROGRAMS")

        self.parent.load_csv_to_table(self.parent.program_table, config_file.program_filename, "PROGRAMS")
        self.parent.load_csv_to_table(self.parent.college_table, config_file.college_filename, "COLLEGES")
        
        self.accept()

    def update_program_college_codes(self, old_code, new_code):
        """Update the college code in program.csv when a college code is changed."""
        program_filename = config_file.program_filename
        updated_data = []

        with open(program_filename, "r", newline="") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        # Ensure data is not empty
        if not data:
            print("Warning: program.csv is empty or missing headers.")
            return

        # Check if the file has a header
        header = data[0] if len(data) > 0 else None
        rows = data[1:]  if len(data) > 1 else []

        print(f"📄 Loaded {len(rows)} rows from program.csv")

        for row in rows:
            if len(row) < 3:  # Ensure the row has at least 3 columns
                print(f"Skipping invalid row: {row}")
                continue  # Skip this row to prevent IndexError

            original_code = row[2].strip()
            print(f"Checking row: {row}")

            if original_code == old_code:  # Check the correct column
                print(f"Updating: {original_code} → {new_code}")
                row[2] = new_code
                
            updated_data.append(row)

        if not updated_data:
            print("No updates made to program.csv")
            return
        
        # Write back to program.csv
        with open(program_filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            if header:
                csv_writer.writerow(header)  # Keep the header row

            csv_writer.writerows(updated_data)

        print(f"✅ Successfully updated {old_code} → {new_code} in program.csv")


class Edit_Program_Dialog(QDialog):
    def __init__(self, parent, row_data, row_index):
        super().__init__(parent)
        self.ui = Ui_Edit_Program_Dialog()
        self.ui.setupUi(self)
        self.row_index = row_index
        self.parent = parent
        self.old_program_code = row_data[0]
        self.old_program_name = row_data[1]
        self.old_college_code = row_data[2]

        self.load_college_code()

        self.ui.program_code_input.setText(row_data[0])
        self.ui.program_name_input.setText(row_data[1])
        self.ui.college_code_input_comboBox.setCurrentText(row_data[2])

        self.ui.Save_button.clicked.connect(self.save_changes)
        self.ui.Cancel_button.clicked.connect(self.cancel)

    def load_college_code(self):
        csv_file_path = config_file.college_filename
        if not os.path.isfile(csv_file_path):
            QMessageBox.warning(self, "Error", f"{csv_file_path} not found!")
            return
        
        with open(csv_file_path, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                college_code = row.get("college_code")
                if college_code:
                    self.ui.college_code_input_comboBox.addItem(college_code)

    def cancel(self):
        self.reject()

    def save_changes(self):
        new_program_code = self.ui.program_code_input.text().strip()
        new_program_name = self.ui.program_name_input.text().strip()
        new_college_code = self.ui.college_code_input_comboBox.currentText()

        if not new_program_code or not new_program_name or not new_college_code:
            QMessageBox.warning(self, "Error", "All fields must not be empty!")
            return        

        if new_program_code == self.old_program_code:
            pass
        else:
            if programCode_existence(config_file.program_filename, new_program_code):
                QMessageBox.warning(self, "Error", "Program code already exists")
                return
            
        if new_program_name == self.old_program_name:
            pass
        else:
            if programName_existence(config_file.program_filename, new_program_name):
                QMessageBox.warning(self, "Error", "Program name already exists!")
                return
            
        if new_college_code == self.old_college_code:
            pass

        filename = config_file.program_filename

        with open(filename, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        if 1 <= self.row_index < len(data):
            data[self.row_index] = [new_program_code, new_program_name, new_college_code]

        with open(filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(data)

        if new_program_code != self.old_program_code:
            self.update_student_program_codes(self.old_program_code, new_program_code)
            self.parent.load_csv_to_table(self.parent.student_table, config_file.student_filename, "STUDENTS")

        self.parent.load_csv_to_table(self.parent.student_table, config_file.student_filename, "STUDENTS")
        self.parent.load_csv_to_table(self.parent.program_table, config_file.program_filename, "PROGRAMS")

        self.accept()

    def update_student_program_codes(self, old_code, new_code):
        student_filename = config_file.student_filename
        updated_data = []

        with open(student_filename, "r", newline="") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        if not data:
            print("Warning: student.csv is empty or missing headers")
            return
        
        header = data[0] if len(data) > 0 else None
        rows = data[1:]  if len(data) > 1 else []

        for row in rows:
            if len(row) < 6:
                print(f"Skipping invalid row: {row}")
                continue

            original_code = row[5].strip()
            print(f"Checking row: {row}")

            if original_code == old_code:  # Check the correct column
                print(f"📝 Updating: {original_code} → {new_code}")
                row[5] = new_code

            updated_data.append(row)

        if not updated_data:
            print("No updated made to studentInfo.csv")
            return
        
        with open(student_filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            if header:
                csv_writer.writerow(header)

            csv_writer.writerows(updated_data)

        print(f"✅ Successfully updated {old_code} → {new_code} in studentInfo.csv")


class Edit_Student_Dialog(QDialog):
    def __init__(self, parent, row_data, row_index):
        super().__init__(parent)
        self.ui = Ui_Edit_Student_Dialog()
        self.ui.setupUi(self)
        self.row_index = row_index
        self.parent = parent

        self.old_id_number = row_data[0]
        self.old_first_name = row_data[1]
        self.old_last_name = row_data[2]
        self.old_gender = row_data[3]
        self.old_year_level = row_data[4]
        self.old_program_code = row_data[5]

        self.load_program_codes()

        self.ui.id_number_input.setText(row_data[0])
        self.ui.first_name_input.setText(row_data[1])
        self.ui.last_name_input.setText(row_data[2])
        self.ui.gender_comboBox.setCurrentText(row_data[3])
        self.ui.year_level_comboBox.setCurrentText(row_data[4])
        self.ui.program_code_input_comboBox.setCurrentText(row_data[5])

        self.ui.Save_button.clicked.connect(self.save_changes)
        self.ui.Cancel_button.clicked.connect(self.cancel)

    def load_program_codes(self):
        csv_file = config_file.program_filename
        if not os.path.isfile(csv_file):
            QMessageBox.warning(self, "Error", f"{csv_file} not found!")
            return
        
        with open(csv_file, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                program_code = row.get("program_code")
                if program_code:
                    self.ui.program_code_input_comboBox.addItem(program_code)

    def cancel(self):
        self.reject()

    def save_changes(self):
        new_id_number = self.ui.id_number_input.text().strip()
        new_first_name = self.ui.first_name_input.text().strip()
        new_last_name = self.ui.last_name_input.text().strip()
        new_gender = self.ui.gender_comboBox.currentText()
        new_year_level = self.ui.year_level_comboBox.currentText()
        new_program_code = self.ui.program_code_input_comboBox.currentText()

        if not new_id_number or not new_first_name or not new_last_name or not new_gender or not new_year_level or not new_program_code:
            QMessageBox.warning(self, "Error", "All fields must not be empty!")
            return

        if new_id_number == self.old_id_number:
            pass
        else:
            if idNumber_existence(config_file.student_filename, new_id_number):
                QMessageBox.warning(self, "Error", "ID Number already exists!")
                return
            
        filename = config_file.student_filename

        with open(filename, "r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                data = list(csv_reader)

        if 1 <= self.row_index < len(data):
            data[self.row_index] = [new_id_number, new_first_name, new_last_name, new_gender, new_year_level, new_program_code]

        with open(filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(data)

        self.parent.load_csv_to_table(self.parent.student_table, filename, "STUDENTS")

        self.accept()
        

class DeleteItemConfirmation(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DeleteConfirmation()
        self.ui.setupUi(self)

        self.ui.Confirm.clicked.connect(self.accept)
        self.ui.Cancel.clicked.connect(self.reject)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Aron dli ma click
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        #self.ui.tableWidget.setEnabled(False)

        #Function call for using search function
        self.ui.search_text.textChanged.connect(self.search_table)

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

        self.ui.stackedWidget.currentChanged.connect(self.on_page_changed)

        #When add [student, program, college] button is clicked, open the respective dialog
        self.ui.addstudent_button.clicked.connect(self.open_add_student_dialog)
        self.ui.addprogram_button.clicked.connect(self.open_add_program_dialog)
        self.ui.addcollege_button.clicked.connect(self.open_add_college_dialog)

        #MAYBE USEFUL FOR UPDATING
        #Load the CSV files to the table
        self.load_csv_to_table(self.student_table, config_file.student_filename, "STUDENTS")
        self.load_csv_to_table(self.program_table, config_file.program_filename, "PROGRAMS")
        self.load_csv_to_table(self.college_table, config_file.college_filename, "COLLEGES")

        #SORTING
        self.ui.comboBox.currentIndexChanged.connect(self.sort_table)
        self.ui.comboBox_2.currentIndexChanged.connect(self.sort_table)
        self.ui.comboBox_3.currentIndexChanged.connect(self.sort_table)
        
    #Function to call [student, program, and college] dialog when the button is clicked
    def open_add_student_dialog(self):
        dialog = Add_Student_Dialog(self)
        dialog.exec()

    def open_add_program_dialog(self):
        dialog = Add_Program_Dialog(self)
        dialog.exec()

    def open_add_college_dialog(self):
        dialog = Add_College_Dialog(self)
        dialog.exec()

    #Function to load the csv files to the tables
    def load_csv_to_table(self, table_widget, filename, table_type):
        if not os.path.isfile(filename):
            print(f" File {filename} does not exist yet.")
            return

        with open(filename, "r", newline="") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

            if not data:
                print(f" {filename} is empty.")
                return
            
            #Get headers from config_file.py
            headers = config_file.header_names.get(table_type, [])
            fieldnames = [h[0] for h in headers] #Unused yet
            readable_headers = [h[1] for h in headers]

            #Sets the table headers and adds one for the Actions
            table_widget.setHorizontalHeaderLabels(readable_headers + ["Actions"])

            #Adds data to the table
            rows = data[1:]
            table_widget.setRowCount(len(rows))
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    if col_index < table_widget.columnCount() - 1: # Ignore last column for buttons
                        table_widget.setItem(row_index, col_index, QTableWidgetItem(value))

                #Adds buttons to the last column
                action_widget = QWidget()
                layout = QHBoxLayout(action_widget)
                layout.setContentsMargins(0, 0, 0, 0)

                #Edit button stylesheet
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda _, ri=row_index: self.edit_row(table_widget, filename, ri))
                layout.addWidget(edit_button)

                #Delete button stylesheet
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, ri=row_index: self.confirm_delete_Row(table_widget, filename, ri))
                layout.addWidget(delete_button)
                
                #Puts the button to the column
                table_widget.setCellWidget(row_index, len(readable_headers), action_widget)

            print(f" Loaded {filename} into {table_type} table with custom headers.")
    
    #Function to edit the row
    def edit_row(self, table_widget, filename, row_index):
        print(f"Editing row {row_index} in {filename}")
        
        with open(filename, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list (csv_reader)


        row_index = row_index + 1

        if row_index < 1 or row_index >= len(data):
            print("Invalid row index. Skipping edit.")
            return

        row_data = data[row_index]

        if filename == config_file.student_filename:
            dialog = Edit_Student_Dialog(self, row_data, row_index)
            table_type = "STUDENTS"
        elif filename == config_file.program_filename:
            dialog = Edit_Program_Dialog(self, row_data, row_index)
            table_type = "PROGRAMS"
        elif filename == config_file.college_filename:
            dialog = Edit_College_Dialog(self, row_data, row_index)
            table_type = "COLLEGES"
        else:
            print("⚠️ Unknown CSV file. Skipping edit.")
            return
        
        if dialog.exec():  # User clicked Save
            self.load_csv_to_table(table_widget, filename, table_type)

    #Function to delete the row
    def delete_row(self, table_widget, filename, row_index):
        print(f"Deleting row {row_index} from {filename}")

        with open(filename, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        #weirdly ako index ga start sa [1] and not [0], therefore permi ga bug kay akong [1] is my header
        row_index = row_index + 1

        if row_index < 1 or row_index >=len(data):
            print("Invalid row index. Skipping deletion.")
            return

        deleted_row = data[row_index]
        del data[row_index]

        with open(filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(data)

        table_widget.removeRow(row_index)

        print("Row deleted successfully and CSV updated.")

        if filename == config_file.college_filename:
            #TODO:
            deleted_college_code = deleted_row[0]  # Get deleted college_code
            self.update_programs_after_college_delete(deleted_college_code)

        if filename == config_file.program_filename:
            deleted_program_code = deleted_row[0]
            self.update_students_after_program_delete(deleted_program_code)

        if filename == config_file.student_filename:
            table_type = "STUDENTS"
        elif filename == config_file.program_filename:
            table_type = "PROGRAMS"
        elif filename == config_file.college_filename:
            table_type = "COLLEGES"
        else:
            print("⚠️ Unknown CSV file. Skipping refresh.")
            return  

        self.load_csv_to_table(table_widget, filename, table_type)

    def confirm_delete_Row(self,table_widget, filename, row_index):
        dialog = DeleteItemConfirmation()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.delete_row(table_widget, filename, row_index)
        else:
            print("Cancelled")

    def on_page_changed(self, index):
    
        if index == 0:
            self.ui.SearchFilters.setCurrentIndex(1)  # ID Number
        elif index == 1:
            self.ui.SearchFilters.setCurrentIndex(6)  # Program Code
        elif index == 2:
            self.ui.SearchFilters.setCurrentIndex(8)  # College Code

    #Function for searching
    def search_table(self):
        search_text = self.ui.search_text.text().strip().lower()
        selected_filter = self.ui.SearchFilters.currentIndex()

        print(f"🔎 Search input:'{search_text}'")
        print(f"🔎 Selected filter:'{selected_filter}'")

        current_index = self.ui.stackedWidget.currentIndex()

        if current_index == 0:
            table_widget = self.student_table
            selected_filter = selected_filter - 1
        elif current_index == 1:
            table_widget = self.program_table
            selected_filter = selected_filter - 6
        elif current_index == 2:
            table_widget = self.college_table
            selected_filter = selected_filter - 8
        else:
            print("⚠️ No valid table selected!")
            return
    
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, selected_filter)
            
            if not search_text:
                table_widget.setRowHidden(row, False)
            else:
                if item and search_text in item.text().strip().lower():
                    table_widget.setRowHidden(row, False)
                else:
                    table_widget.setRowHidden(row, True)

    #Function for sorting the tables
    def sort_table(self):
        current_index = self.ui.stackedWidget.currentIndex()

        if current_index == 0:
            table_widget = self.student_table
            filename = config_file.student_filename
            table_type = "STUDENTS"
            sort_combo = self.ui.comboBox
            sort_mapping = {
                1: (1, QtCore.Qt.SortOrder.AscendingOrder),  # First Name (A-Z)
                2: (1, QtCore.Qt.SortOrder.DescendingOrder),  # First Name (Z-A)
                3: (2, QtCore.Qt.SortOrder.AscendingOrder),  # Last Name (A-Z)
                4: (2, QtCore.Qt.SortOrder.DescendingOrder),  # Last Name (Z-A)
                5: (0, QtCore.Qt.SortOrder.AscendingOrder),  # Student ID (Ascending)
                6: (0, QtCore.Qt.SortOrder.DescendingOrder),  # Student ID (Descending)
                7: (3, QtCore.Qt.SortOrder.AscendingOrder),  # Year Level (1-4)
                8: (3, QtCore.Qt.SortOrder.DescendingOrder),  # Year Level (4-1)
                9: (5, QtCore.Qt.SortOrder.AscendingOrder),  # Program Code (A-Z)
                10: (4, QtCore.Qt.SortOrder.AscendingOrder)  # Gender
            }

        elif current_index == 1:
            table_widget = self.program_table
            filename = config_file.program_filename
            table_type = "PROGRAMS"
            sort_combo = self.ui.comboBox_2
            sort_mapping = {
                1: (0, QtCore.Qt.SortOrder.AscendingOrder), #Program Code (A-Z)
                2: (0, QtCore.Qt.SortOrder.DescendingOrder), #Z-A
                3: (1, QtCore.Qt.SortOrder.AscendingOrder),  #Program Name (A-Z)
                4: (1, QtCore.Qt.SortOrder.DescendingOrder), #Z-A
                5: (2, QtCore.Qt.SortOrder.AscendingOrder), #College Code (A-Z)
                6: (2, QtCore.Qt.SortOrder.DescendingOrder) #Z-A
            }
        elif current_index == 2:
            table_widget = self.college_table
            filename = config_file.college_filename
            table_type = "COLLEGES"
            sort_combo = self.ui.comboBox_3
            sort_mapping = {
                1: (0, QtCore.Qt.SortOrder.AscendingOrder), #College Code (A-Z)
                2: (0, QtCore.Qt.SortOrder.DescendingOrder), #Z-A
                3: (1, QtCore.Qt.SortOrder.AscendingOrder),  #College Name (A-Z)
                4: (1, QtCore.Qt.SortOrder.DescendingOrder), #Z-A
            }
        else:
            print("⚠️ No active table found.")
            return

        selected_sort_index = sort_combo.currentIndex()

        if selected_sort_index not in sort_mapping:
            print(f"🔄 Restoring {table_type} Table to Original Order from CSV...")
            self.load_csv_to_table(table_widget, filename, table_type)
            return
        
        column_index, sort_order = sort_mapping[selected_sort_index]

        print(f"🔄 Sorting {table_type} Table by Column Index: {selected_sort_index}")

        table_widget.sortItems(column_index, sort_order)

    def update_programs_after_college_delete(self, deleted_college_code):
        program_filename = config_file.program_filename
        updated_data = []

        with open(program_filename, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        if not data:
            print("⚠️ Warning: program.csv is empty or missing headers.")
            return
    
        header = data[0]
        rows = data[1:]

        for row in rows:
            if row[2] == deleted_college_code:
                print(f"🔄 Updating program {row[0]} (was under {deleted_college_code}) to 'N/A'")
                row[2] = "N/A"  # Replace college_code with "N/A"
            updated_data.append(row)

        with open(program_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerows(updated_data)

        print(f"✅ Programs under {deleted_college_code} updated to 'N/A'.")
        self.load_csv_to_table(self.program_table, program_filename, "PROGRAMS")

        self.update_students_after_program_delete("N/A")

    def update_students_after_program_delete(self, deleted_program_code):
        student_filename = config_file.student_filename
        updated_data = []

        with open(student_filename, "r", newline="") as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        if not data:
            print("⚠️ Warning: student.csv is empty or missing headers.")
            return

        header = data[0]
        rows = data[1:]

        for row in rows:
            if row[5] == deleted_program_code:  # If program_code matches deleted program
                print(f"🔄 Updating student {row[0]} (was in {deleted_program_code}) to 'Unenrolled'")
                row[5] = "Unenrolled"  # Replace program_code with "Unenrolled"
            updated_data.append(row)

        with open(student_filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)
            csv_writer.writerows(updated_data)

        print(f"✅ Students under {deleted_program_code} updated to 'Unenrolled'.")
        self.load_csv_to_table(self.student_table, student_filename, "STUDENTS")

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())