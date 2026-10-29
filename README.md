# Automated Marksheet Generator

Python 3 console project for **PS No. 93 – Automated Marksheet Generator**.

## Features
- Reads `marks.csv` using Pandas
- Handles a missing CSV file
- Validates every mark is between 0 and 100 and skips invalid rows with a warning
- Finds a student by roll number
- Calculates total out of 300 and percentage to two decimal places
- Grades: A+ (90+), A (80+), B (70+), C (60+), D (50+), E (40+), F (below 40)
- Result is FAIL if any subject is below 40; otherwise PASS

## Files
```
README.md
marksheet_generator.py
marks.csv
requirements.txt
```

## Install and run
```bash
pip install -r requirements.txt
python marksheet_generator.py
```
## Live Project
https://automated-marksheet-generator.onrender.com/

## Assignment test data
The included CSV contains the sample rows for roll numbers 101–104 plus intentionally invalid roll 106 (Maths = 105) for validation testing.

Expected key cases:
- 101 Anita → 255/300, 85.00%, Grade A, PASS
- 102 Rahul → 135/300, 45.00%, Grade E, PASS
- 999 → Roll number not found
- Invalid row 106 → skipped with warning
- 103 Suman → 165/300, 55.00%, Grade D, FAIL because Maths is below 40
