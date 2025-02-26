student_filename = "studentInfo.csv"
program_filename = "studentProgram.csv"
college_filename = "studentCollege.csv"

student_fieldnames = ["id_number", "first_name", "last_name", "year_level", "gender", "program_code"]
program_fieldnames = ["program_code", "program_name", "college_code"]
college_fieldnames = ["college_code", "college_name"]

header_names = {
    "STUDENTS": [
        ("id_number", "ID Number"),
        ("first_name", "First Name"),
        ("last_name", "Last Name"),
        ("year_level", "Year Level"),
        ("gender", "Gender"),
        ("program_code", "Program Code"),
    ],
    "PROGRAMS": [
        ("program_code", "Program Code"),
        ("program_name", "Program Name"),
        ("college_code", "College Code"),
    ],
    "COLLEGES": [
        ("college_code", "College Code"),
        ("college_name", "College Name"),
    ],
}