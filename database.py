
from firebase_config import db
from firebase_admin import firestore


# Count duplicate registration attempts in Firestore
def increment_duplicate_attempts():
    stats_ref = db.collection("project_stats").document("metrics")

    stats_ref.set({
        "duplicate_attempts": firestore.Increment(1)
    }, merge=True)


# Get total duplicate attempts
def get_duplicate_attempts():
    stats_ref = db.collection("project_stats").document("metrics")
    stats = stats_ref.get()

    if stats.exists:
        return stats.to_dict().get("duplicate_attempts", 0)

    return 0


# Add a new student
def add_student(student_id, name, email):

    student_id = student_id.strip()
    name = name.strip()
    email = email.strip().lower()

    if not student_id or not name or not email:
        return False, "All fields are required."

    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid email address."

    students_ref = db.collection("students")

    try:
        # Check duplicate Student ID
        if students_ref.document(student_id).get().exists:
            increment_duplicate_attempts()
            return False, "Duplicate Student ID! Student not added."

        # Check duplicate email
        duplicate_email = list(
            students_ref.where("email", "==", email).limit(1).stream()
        )

        if duplicate_email:
            increment_duplicate_attempts()
            return False, "Duplicate email! Student not added."

        # Save student in Firestore
        students_ref.document(student_id).set({
            "student_id": student_id,
            "name": name,
            "email": email
        })

        return True, "Student added successfully!"

    except Exception as error:
        return False, f"Database error: {error}"


# Read all students
def get_students():

    students = db.collection("students").stream()

    records = []

    for student in students:
        data = student.to_dict()

        records.append((
            student.id,
            data.get("name", data.get("name ", "")),
            data.get("email", "")
        ))

    records.sort(key=lambda x: x[0])

    return records


# Delete a student
def delete_student(student_id):

    try:
        student_ref = db.collection("students").document(student_id)

        if not student_ref.get().exists:
            return False, "Student record not found."

        student_ref.delete()

        return True, "Student deleted successfully!"

    except Exception as error:
        return False, f"Database error: {error}"