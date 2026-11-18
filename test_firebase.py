
from firebase_config import db

try:
    students = db.collection("students").stream()

    print("\nFirebase Connection Successful!")
    print("\nStudent Records:")

    for student in students:
        print(student.id, student.to_dict())

except Exception as e:
    print("Firebase Connection Failed:", e)
