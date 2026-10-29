from flask import Flask, request, render_template_string
from marksheet_generator import load_marks, get_grade

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Automated Marksheet Generator</title>
<style>
body{font-family:Arial,sans-serif;background:#f4f6f8;margin:0;color:#1f2937}
main{max-width:760px;margin:48px auto;padding:20px}
.card{background:white;padding:28px;border-radius:16px;box-shadow:0 8px 30px #0001}
h1{margin-top:0} form{display:flex;gap:10px;flex-wrap:wrap}
input{flex:1;min-width:180px;padding:12px;border:1px solid #ccd2da;border-radius:9px;font-size:16px}
button{padding:12px 18px;border:0;border-radius:9px;background:#111827;color:white;font-weight:700;cursor:pointer}
.result{margin-top:24px;padding:20px;border-radius:12px;background:#f8fafc}
.error{margin-top:20px;padding:14px;border-radius:10px;background:#fff1f2;color:#9f1239}
table{width:100%;border-collapse:collapse;margin-top:12px}td,th{padding:10px;border-bottom:1px solid #e5e7eb;text-align:left}
small{color:#64748b}
</style>
</head>
<body><main><div class="card">
<h1>Automated Marksheet Generator</h1>
<p>Enter a student roll number to generate the marksheet.</p>
<form method="post"><input name="roll_no" type="number" placeholder="Enter Roll No." required><button type="submit">Generate</button></form>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
{% if student %}
<div class="result"><h2>{{ student.name }} — Roll {{ student.roll }}</h2>
<table>
<tr><th>Subject</th><th>Marks</th></tr>
<tr><td>Maths</td><td>{{ student.maths }}</td></tr>
<tr><td>Physics</td><td>{{ student.physics }}</td></tr>
<tr><td>Programming</td><td>{{ student.programming }}</td></tr>
<tr><th>Total</th><th>{{ student.total }}/300</th></tr>
</table>
<p><strong>Percentage:</strong> {{ student.percentage }}%</p>
<p><strong>Grade:</strong> {{ student.grade }} &nbsp; <strong>Result:</strong> {{ student.result }}</p>
</div>{% endif %}
<p><small>PS No. 93 • Python + Pandas + Flask</small></p>
</div></main></body></html>"""

@app.route("/", methods=["GET", "POST"])
def home():
    student_data = None
    error = None
    if request.method == "POST":
        try:
            roll_no = int(request.form["roll_no"])
            df = load_marks()
            if df is None:
                error = "Unable to load marks data."
            else:
                match = df[df["RollNo"] == roll_no]
                if match.empty:
                    error = f"Roll number {roll_no} not found."
                else:
                    s = match.iloc[0]
                    marks = [float(s["Maths"]), float(s["Physics"]), float(s["Programming"])]
                    total = sum(marks)
                    percentage = total / 3
                    student_data = {
                        "roll": roll_no, "name": s["Name"],
                        "maths": int(marks[0]) if marks[0].is_integer() else marks[0],
                        "physics": int(marks[1]) if marks[1].is_integer() else marks[1],
                        "programming": int(marks[2]) if marks[2].is_integer() else marks[2],
                        "total": int(total) if total.is_integer() else total,
                        "percentage": f"{percentage:.2f}",
                        "grade": get_grade(percentage),
                        "result": "FAIL" if any(mark < 40 for mark in marks) else "PASS",
                    }
        except (ValueError, TypeError):
            error = "Please enter a valid roll number."
    return render_template_string(PAGE, student=student_data, error=error)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
