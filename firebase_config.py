
import firebase_admin
from firebase_admin import credentials, firestore

db = None
firebase_error = None

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "codealpha-data-redundancy-firebase-adminsdk-fbsvc-6a05c8af0e.json"
        )

        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("Firebase initialized successfully!")

except Exception as error:
    firebase_error = str(error)
    print("Firebase initialization failed:", firebase_error)
