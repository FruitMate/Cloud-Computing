import firebase_admin
from firebase_admin import firestore
from datetime import datetime
import json

cred = firebase_admin.credentials.Certificate(
    "config/firebase/serviceAccount.json")
firebase_admin.initialize_app(cred)

# Inizialize Firestore
db = firestore.client()

# Save data to Firestore
def save_history_to_firestore(uid, image_url, classification_result):
    try:
        data = {
            'uid': uid,
            'image_url': image_url,
            'classification_result': classification_result,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        db.collection('classification_results').add(data)
        response = {'code': 200, 'message': 'Data saved successfully!'}
        response_json = json.dumps(response)
        return response_json, 200
    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500

# Get data from Firestore
def get_data_firestore_by_id(uid):
    try:
        query = db.collection('classification_results').where(
            'uid', '==', uid).get()
        results = []

        for doc in query:
            data = doc.to_dict()
            results.append(data)

        response = {'code': 200, 'data': results}
        response_json = json.dumps(response)
        return response_json, 200
    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500
