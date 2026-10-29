import pandas as pd

FILE_NAME = "marks.csv"

def load_marks(filename=FILE_NAME):
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

    required = ["RollNo", "Name", "Maths", "Physics", "Programming"]
    if not all(col in df.columns for col in required):
        print("Error: CSV file has missing required columns.")
        return None

    valid_rows = []
    for _, row in df.iterrows():
        try:
            roll_no = int(row["RollNo"])
            marks = [float(row["Maths"]), float(row["Physics"]), float(row["Programming"])]
            if not all(0 <= mark <= 100 for mark in marks):
                print(f"Warning: Row for roll {roll_no} skipped - marks must be between 0 and 100.")
                continue
            valid_rows.append({
                "RollNo": roll_no, "Name": str(row["Name"]).strip(),
                "Maths": marks[0], "Physics": marks[1], "Programming": marks[2]
            })
        except (ValueError, TypeError):
            print("Warning: Invalid row skipped.")
    return pd.DataFrame(valid_rows)

def get_grade(percentage):
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    if percentage >= 40: return "E"
    return "F"

def generate_marksheet(df, roll_no):
    student = df[df["RollNo"] == roll_no]
    if student.empty:
        print(f"Roll number {roll_no} not found.")
        return
    s = student.iloc[0]
    marks = [s["Maths"], s["Physics"], s["Programming"]]
    total = sum(marks)
    percentage = total / 3
    grade = get_grade(percentage)
    result = "FAIL" if any(mark < 40 for mark in marks) else "PASS"
    fmt = lambda x: int(x) if float(x).is_integer() else x
    print(f"Roll No: {roll_no} | Name: {s['Name']}")
    print(f"Maths: {fmt(marks[0])} | Physics: {fmt(marks[1])} | Programming: {fmt(marks[2])}")
    print(f"Total: {fmt(total)}/300 | Percentage: {percentage:.2f}%")
    print(f"Grade: {grade} | Result: {result}")

def main():
    df = load_marks()
    if df is None:
        return
    print("Menu: Single marksheet")
    try:
        roll_no = int(input("Enter Roll no: "))
    except ValueError:
        print("Invalid roll number.")
        return
    generate_marksheet(df, roll_no)

if __name__ == "__main__":
    main()
