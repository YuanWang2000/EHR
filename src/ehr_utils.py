"""Phase 6."""
from dataclasses import dataclass
import sqlite3
from datetime import datetime, date


@dataclass
class Lab:  # O(1)
    """Lab class."""

    lab_id: str  # O(1)

    @property
    def name(self) -> str:  # O(1)
        """Lab.lab_name."""
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute(
            f"SELECT LabName FROM labs WHERE LabID='{self.lab_id}'"
        )  # O(1)
        name = str(c.fetchone()[0])  # O(1)
        c.close()  # O(1)
        return name  # O(1)

    # The overall time complexity: O(1)

    @property
    def value(self) -> str:  # O(1)
        """Lab.lab_value."""
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute(
            f"SELECT LabValue FROM labs WHERE LabID='{self.lab_id}'"
        )  # O(1)
        value = str(c.fetchone()[0])  # O(1)
        c.close()  # O(1)
        return value  # O(1)

    # The overall time complexity: O(1)

    @property
    def date_time(self) -> datetime:  # O(1)
        """Lab.lab_datetime."""
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute(
            f"SELECT LabDateTime FROM labs WHERE LabID='{self.lab_id}'"
        )  # O(1)
        date_time = datetime.strptime(
            c.fetchone()[0], "%Y-%m-%d %H:%M:%S.%f"
        )  # O(1)
        c.close()  # O(1)
        return date_time  # O(1)

    # The overall time complexity: O(1)


@dataclass
class Patient:  # O(1)
    """Patient class."""

    patient_id: str  # O(1)

    @property
    def gender(self) -> str:  # O(1)
        """Get patient's gender."""
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        query = "SELECT PatientGender FROM patients WHERE PatientID=?"  # O(1)
        c.execute(query, (self.patient_id,))  # O(1)
        gender = str(c.fetchone()[0])  # O(1)
        c.close()  # O(1)
        return gender  # O(1)

    # The overall time complexity: O(1)

    @property
    def date_birth(self) -> datetime:  # O(1)
        """Get patient's data of birth."""
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        query = (
            "SELECT PatientDateOfBirth FROM patients WHERE PatientID=?"  # O(1)
        )
        c.execute(query, (self.patient_id,))  # O(1)
        date_birth = datetime.strptime(
            c.fetchone()[0], "%Y-%m-%d %H:%M:%S.%f"
        )  # O(1)
        c.close()  # O(1)
        return date_birth  # O(1)

    # The overall time complexity: O(1)

    @property
    def labs(self) -> list[Lab]:
        """Get patient's all the labs."""
        labs = []  # O(1)
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute(
            f"SELECT LabID FROM labs WHERE PatientID='{self.patient_id}'"
        )  # O(1)
        labids = c.fetchall()  # O(1)
        for id in labids:  # O(L) [L: the number of labs for a patient]
            labs.append(Lab(id[0]))  # O(1)
        c.close()  # O(1)
        return labs  # O(1)

    # The overall time complexity: O(L)
    # L: the number of labs for a patient

    @property
    def age(self) -> int:  # O(1)
        """Calculate patient age."""
        today = date.today()  # O(1)
        dob = self.date_birth.date()  # O(1)
        if (today.month, today.day) < (dob.month, dob.day):  # O(1)
            age = today.year - dob.year - 1  # O(1)
        else:  # O(1)
            age = today.year - dob.year  # O(1)
        return age  # O(1)

    # The overall time complexity: O(1)

    def is_sick(
        self, lab_name: str, operator: str, value: float
    ) -> bool:  # O(1)
        """Compare the patient's lab value to threhold."""
        result = False  # O(1)
        hist_value = []  # O(1)
        for lab in self.labs:  # O(N)[N:the total number of labs for a patient]
            if lab.name == lab_name:  # O(1)
                hist_value.append(float(lab.value))  # O(1)
        if operator == ">" and max(hist_value) > value:  # O(1)
            result = True  # O(1)
        elif operator == "<" and min(hist_value) < value:  # O(1)
            result = True  # O(1)
        return result  # O(1)

    # The overall time complexity: O(N)
    # N: the total number of labs for a patient

    def early_lab_age(self) -> int:  # O(1)
        """Find the earliest lab record and calculate the age at that time."""
        lab_times = []  # O(1)
        for lab in self.labs:  # O(N)[N:the total number of labs for a patient]
            lab_times.append(lab.date_time)  # O(1)
        earliest_date = min(lab_times).date()  # O(1)
        dob = self.date_birth.date()  # O(1)
        if (earliest_date.month, earliest_date.day) < (
            dob.month,
            dob.day,
        ):  # O(1)
            earl_age = earliest_date.year - dob.year - 1  # O(1)
        else:  # O(1)
            earl_age = earliest_date.year - dob.year  # O(1)
        return earl_age  # O(1)

    # The overall time complexity: O(N)
    # N: the total number of labs for a patient.


def parse_data(pat_filename: str, lab_filename: str) -> list[str]:  # O(1)
    """Read and parse the data files."""
    # read patient information
    patients = []  # O(1)
    with open(pat_filename, "r", encoding="utf-8-sig") as f1:  # O(1)
        title1 = (
            f1.readline().strip("\n").split("\t")
        )  # O(Cp) [Cp: the number of columns in patient_file]
        id_in1 = title1.index("PatientID")  # O(Cp)
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute("DROP TABLE IF EXISTS patients")  # O(1)
        create_table1 = (
            "CREATE TABLE patients ("
            + ", ".join([f"{column} TEXT" for column in title1])
            + ")"
        )  # O(1)
        c.execute(create_table1)  # O(1)
        for line in f1.readlines():  # O(P)[P: the number of patients]
            patient_info = line.strip("\n").split("\t")  # O(Cp)
            patients.append(patient_info[id_in1])  # O(1)
            insert_sql1 = (
                f"INSERT INTO patients ({', '.join(title1)}) "
                f"VALUES ({', '.join(['?']*len(patient_info))})"
            )  # O(Cp)
            c.execute(insert_sql1, patient_info)  # O(Cp)
        conn.commit()  # O(1)
        c.close()  # O(1)

    # read lab information
    with open(lab_filename, "r", encoding="utf-8-sig") as f2:  # O(1)
        title2 = (
            f2.readline().strip("\n").split("\t")
        )  # O(Cl) [Cl: the number of columns in lab_file]
        title2.append("LabID")  # O(1)
        id_in2 = title2.index("PatientID")  # O(Cl)
        date_in = title2.index("LabDateTime")  # O(Cl)
        conn = sqlite3.connect("data.db")  # O(1)
        c = conn.cursor()  # O(1)
        c.execute("DROP TABLE IF EXISTS labs")  # O(1)
        create_table2 = (
            "CREATE TABLE labs ("
            + ", ".join([f"{column} TEXT" for column in title2])
            + ")"
        )  # O(1)
        c.execute(create_table2)  # O(1)
        for line in f2.readlines():  # O(M)
            lab_info = line.strip("\n").split("\t")  # O(Cl)
            lab_info.append(str(lab_info[id_in2]) + lab_info[date_in])  # O(1)
            insert_sql2 = (
                f"INSERT INTO labs ({', '.join(title2)}) "
                f"VALUES ({', '.join(['?']*len(lab_info))})"
            )  # O(Cl)
            c.execute(insert_sql2, lab_info)  # O(Cl)
        conn.commit()  # O(1)
        c.close()  # O(1)
    return patients  # O(1)


# The overall time complexity for this function: O(P*Cp + M*Cl)
# P: the number of patients
# Cp: the number of columns in patient_file
# M: the total number of rows in lab_file
# Cl: the number of columns in lab_file
