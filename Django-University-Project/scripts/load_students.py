"""Run with:  python manage.py runscript load_students"""
from csv import DictReader
from datetime import datetime, timezone

from myApp.models import Module, Student

DATETIME_FORMAT = "%m/%d/%Y"

modules = {
    "MOD002619": "Web Programming",
    "MOD002643": "Image Processing",
    "MOD002691": "Final Project",
    "MOD003212": "Introduction to Programming",
    "MOD003484": "Software Principles",
}

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the student data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


def run():
    if Student.objects.exists() or Module.objects.exists():
        print("Student data already loaded...exiting.")
        print(ALREADY_LOADED_ERROR_MESSAGE)
        return

    print("Creating module data")
    for mcode, mname in modules.items():
        Module(code=mcode, name=mname).save()

    print("Loading student data")
    with open("./students.csv") as fh:
        for row in DictReader(fh):
            stu = Student()
            stu.firstName = row["fname"]
            stu.lastName = row["lname"]
            stu.age = row["age"]
            stu.email = row["email"]
            stu.enrolmentDate = datetime.strptime(row["enrolment date"], DATETIME_FORMAT).replace(tzinfo=timezone.utc)
            stu.save()

            # Now add the module enrolments
            module_codes = [c for c in row["modules"].split("| ") if c]
            for code in module_codes:
                stu.modules.add(Module.objects.get(code=code.strip()))
    print("Done.")
