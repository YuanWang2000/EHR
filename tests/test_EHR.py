"""Test EHR."""
import pytest

from fake_files import fake_files
from ehr_utils import parse_data, Patient, Lab
from datetime import datetime, date
import sqlite3

f_patient_info = [
    "PatientID",
    "PatientDateOfBirth",
    "PatientGender",
    "PatientRace",
]
f_patient_1 = ["A1", "1970-07-25 13:04:20.717", "female", "white"]
f_patient_2 = ["A2", "1980-07-25 13:04:20.717", "male", "white"]
f_lab_info = ["PatientID", "LabName", "LabValue", "LabDateTime"]
f_p1_lab_1 = ["A1", "Lab 1", "1.2", "2000-05-25 13:04:20.717"]
f_p1_lab_2 = ["A1", "Lab 1", "2.2", "2002-05-25 13:04:20.717"]
f_p2_lab_1 = ["A2", "Lab 1", "3.2", "2020-05-25 13:04:20.717"]
f_patient_file = [f_patient_info, f_patient_1, f_patient_2]
f_lab_file = [f_lab_info, f_p1_lab_1, f_p1_lab_2, f_p2_lab_1]

f_pat_1 = Patient("A1")
f_pat_2 = Patient("A2")


def test_parse_data_pat_len() -> None:
    """Test patient data parse length."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert len(result) == 2


def test_parse_data_type() -> None:
    """Test patient data parse type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert type(result) == list


def test_parse_data_result_1() -> None:
    """Test what we got when using parse_data."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert result[0] == f_patient_1[0]


def test_parse_data_result_2() -> None:
    """Test what we got when using parse_data."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert result[1] == f_patient_2[0]


def test_patient_1_labs_len() -> None:
    """Test patient1 labs list."""
    assert len(f_pat_1.labs) == 2


def test_patient_1_labs() -> None:
    """Test patient1 labs."""
    assert isinstance(f_pat_1.labs[1], Lab)


def test_patient_2_labs() -> None:
    """Test patient1 labs."""
    assert isinstance(f_pat_2.labs[0], Lab)


def test_patient_age_1() -> None:
    """Test patient1 age."""
    f_bd = datetime.strptime(f_patient_1[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_pat_age = int(((date.today() - f_bd).days) / 365)
    assert f_pat_1.age == f_pat_age


def test_patient_age_2() -> None:
    """Test patient2 age."""
    f_bd = datetime.strptime(f_patient_2[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_pat_age = int(((date.today() - f_bd).days) / 365)
    assert f_pat_2.age == f_pat_age


def test_patient_is_sick_1() -> None:
    """Test patient1 lab info."""
    t_sign = "<"
    t_value = 1.0
    f_labval = min(float(f_p1_lab_1[2]), float(f_p1_lab_2[2]))
    f_result = eval(f"{f_labval} {t_sign} {t_value}")
    assert f_pat_1.is_sick(f_p1_lab_1[1], t_sign, t_value) == f_result


def test_patient_is_sick_2() -> None:
    """Test patient2 lab info."""
    t_sign = ">"
    t_value = 3.0
    f_labval = float(f_p2_lab_1[2])
    f_result = eval(f"{f_labval} {t_sign} {t_value}")
    assert f_pat_2.is_sick(f_p2_lab_1[1], t_sign, t_value) == f_result


def test_earlist_lab_age_1() -> None:
    """Test earliest lab age for patient1."""
    f_earl_lab = datetime.strptime(
        f_p1_lab_1[3], "%Y-%m-%d %H:%M:%S.%f"
    ).date()  # long line
    f_bd = datetime.strptime(f_patient_1[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_earl_age = int((f_earl_lab - f_bd).days / 365)
    assert f_pat_1.early_lab_age() == f_earl_age


def test_earlist_lab_age_2() -> None:
    """Test earliest lab age for patient2."""
    f_earl_lab = datetime.strptime(
        f_p2_lab_1[3], "%Y-%m-%d %H:%M:%S.%f"
    ).date()  # long line
    f_bd = datetime.strptime(f_patient_2[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_earl_age = int(((f_earl_lab - f_bd).days) / 365)
    assert f_pat_2.early_lab_age() == f_earl_age
