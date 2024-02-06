# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

# end-users

1. Setup/Installation:
    * To use this project, you need Python 3.10 or higher installed on your machine. You can download Python from the official website: (https://www.python.org/downloads/). 
2. Input file: 
    * The module expects two input files:
        * A patient information file in tab-separated values (TSV) format.
        * A lab information file in TSV format.
    * The columns names for the input file are expected to be: 
        * Patient file: PatientID, PatientDateOfBirth, ...
        * Lab file: PatientID, LabName, LabValue, ...
3. Examples: 
    * Generate a fake file and read and parse the data files: 
    ```python
    from ehr_utils import parse_data, Patient, Lab
    from datetime import datetime, date
    from fake_files import fake_files
    import sqlite3
    f_patient_info = ["PatientID", "PatientDateOfBirth"]
    f_patient = ["A1", "1970-07-25 13:04:20.717"]
    f_lab_info = ["PatientID", "LabName", "LabValue", "LabDateTime"]
    f_lab = ["A1", "Lab 1", "1.2", "2000-05-25 13:04:20.717"]
    f_patient_file = [f_patient_info, f_patient]
    f_lab_file = [f_lab_info, f_lab]
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
    ```
    This creates a fake patient file and a fake lab file. Then we use parse_data() function to parse the two files and build a single central database including all the patient information and lab information. Users can request the data as they needed. And all the patients' ID are saved in the "result" as a list. Users can find out who is in the database.
    
    ```python
    f_pat_1 = Patient("A1")
    ```
    This code creates a instance of patient A1, then we can request their infomation by calling their properties. 

    * The age in years of the given patient: 
    ```python 
    age = f_pat_1.age
    print(age)
    ```
    When we run these codes, we can get 52 as the age of the patient. 

    * Take the data and return a boolean of whether the patient is sick: 
    ```python 
    sick = f_pat_1.is_sick("lab1", ">", 1.0)
    print(sick)
    ```
    When we run these codes, we can get True as the result to show whether the patient is sick. 

    * Find the earliest lab record and calculate the age at that time: 
    ```python
    records_age = f_pat_1.early_lab_age()
    print(records_age)
    ```
    When we run these codes, we can get the age of the patient when he/she first had a lab record. 


# contributors 

1. The tests directory includes three files that are used to test the EHR library:
    * fake_file.py: It can generate a temporary fake file to test the EHR function.
    * test_fake_files.py: It can test the functions of the fake_file library.
    * test_EHR.py: It can test the functions of the ehr-utils library.
2. To test the module locally, use pytest to run the two test files together.