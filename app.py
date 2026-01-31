from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "minorprojectkey"

def performance_status(marks):
    if marks < 40:
        return "At Risk"
    elif marks < 60:
        return "Below Average"
    elif marks < 80:
        return "Average"
    else:
        return "Safe"

def calculate_sgpa(marks):
    if marks < 40:
        return round(4.0 + (marks / 40), 2)
    elif marks < 60:
        return round(5.0 + ((marks - 40) / 20) * 1.4, 2)
    elif marks < 80:
        return round(6.5 + ((marks - 60) / 20) * 1.4, 2)
    else:
        return round(8.0 + ((marks - 80) / 20) * 1.5, 2)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["file"]
        df = pd.read_csv(file)

        df["SGPA"] = df["Marks"].apply(calculate_sgpa)
        df["Status"] = df["Marks"].apply(performance_status)
        df.insert(0, "S.No", range(1, len(df) + 1))

        return render_template("result.html", tables=[df.to_html(index=False)])

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
