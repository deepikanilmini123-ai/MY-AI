import firebase_admin
from firebase_admin import credentials, db

class FirebaseManager:
    def __init__(self):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://my-gameing-site-default-rtdb.asia-southeast1.firebasedatabase.app/'
                })
            self.db_ref = db.reference()
            self.enabled = True
            print("[Firebase]: Connected to Realtime Database successfully!")
        except Exception as e:
            print(f"[Firebase Warning]: {e}")
            self.enabled = False

    def log_interaction(self, user_input, response):
        """Chat Logs සේව් කිරීම"""
        if not self.enabled:
            return
        try:
            ref = self.db_ref.child('logs')
            ref.push({'user': user_input, 'ai': response})
        except Exception as e:
            print(f"[Firebase Log Error]: {e}")

    def add_to_dataset(self, prompt, response):
        """Firebase Realtime Database එකට Save කිරීම"""
        if not self.enabled:
            return False
        try:
            ref = self.db_ref.child('dataset')
            ref.push({
                'prompt': prompt,
                'response': response
            })
            return True
        except Exception as e:
            print(f"[Firebase Train Error]: {e}")
            return False