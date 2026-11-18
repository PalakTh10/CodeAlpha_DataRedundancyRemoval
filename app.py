
from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    add_student,
    get_students,
    delete_student,
    get_duplicate_attempts
)

from firebase_config import db

app = Flask(__name__)
app.secret_key = "codealpha_project_secret"


@app.route("/")
def home():

    try:
        if db is None:
            raise Exception("Firebase initialization failed")

        students = get_students()
        duplicate_attempts = get_duplicate_attempts()

        # Check actual Firestore connection
        db.collection("students").limit(1).get()

        firestore_status = "Connected"

    except Exception as error:
        print("Firestore connection error:", error)

        students = []
        duplicate_attempts = 0
        firestore_status = "Unavailable"

    return render_template(
        "index.html",
        students=students,
        duplicate_attempts=duplicate_attempts,
        firestore_status=firestore_status
    )


@app.route("/add_student", methods=["POST"])
def add_student_route():

    if db is None:
        flash("Firebase is unavailable. Please try again later.", "error")
        return redirect(url_for("home"))

    student_id = request.form.get("student_id", "").strip()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    success, message = add_student(student_id, name, email)

    flash(message, "success" if success else "error")

    return redirect(url_for("home"))


@app.route("/delete_student", methods=["POST"])
def delete_student_route():

    if db is None:
        flash("Firebase is unavailable. Please try again later.", "error")
        return redirect(url_for("home"))

    student_id = request.form.get("student_id", "").strip()

    if not student_id:
        flash("Please select a valid student ID.", "error")
        return redirect(url_for("home"))

    success, message = delete_student(student_id)

    flash(message, "success" if success else "error")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
