from flask import Flask, request
from datetime import datetime
from firebase_admin import auth
import json
import string
import random
import os

from controllers.scan_apple import Scanner
from controllers.image_to_gcs import save_image_to_gcs, save_image_to_tmp_gcs, delete_image_from_tmp_gcs
from controllers.history_to_firestore import save_history_to_firestore
from controllers.history_to_firestore import get_data_firestore_by_id

app = Flask(__name__)

app.debug = True

scanner = Scanner()

# Route for / or index
@app.route('/', methods=['GET'])
def index():
    try:
        return json.dumps({'message': "Application running!"})
    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500

# Route for login (just for testing on development)
@app.route('/api/user/login', methods=['POST'])
def login():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return json.dumps({'error': 'Content type not supported'}), 415

        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return json.dumps({'error': 'Email and password must be filled in'}), 400

        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        uid = user.uid

        return json.dumps({'token': custom_token.decode(), 'uid': uid}), 200

    except auth.InvalidIdTokenError as e:
        return json.dumps({'error': str(e)}), 401

    except Exception as e:
        return json.dumps({'error': str(e)}), 500

# Route For Scan Apple
@app.route('/api/scan-apple', methods=['POST'])
def scan_apple():

    image = request.files['image']
    email = request.form['email']

    try:
        def generate_random_filename(length=10):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choices(characters, k=length))
            random_name = random_string
            return random_name

        user = auth.get_user_by_email(email)
        uid = user.uid

        random_name = generate_random_filename(10)
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{current_datetime}_{uid}_{random_name}.jpg'

        image_url_tmp = save_image_to_tmp_gcs(image, filename=filename)

        preprocessed_image = scanner.preprocessing(image_url_tmp)

        classification_result = scanner.img_classification(preprocessed_image)

        image_url = save_image_to_gcs(image, filename=filename)

        delete_image_from_tmp_gcs(filename)

        save_history_to_firestore(uid, image_url, classification_result)

        response = {'code': 200, 'message': 'Classification Success!', 'prediction': classification_result}
        response_json = json.dumps(response)
        return response_json, 200
    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500


# Route For History
@app.route('/api/history', methods=['GET'])
def get_scan_history():
    try:
        email = request.args.get('email')

        if not email:
            return json.dumps({'error': 'Email must be included in the query parameters!'}), 400

        user = auth.get_user_by_email(email)
        uid = user.uid
        return get_data_firestore_by_id(uid)

    except auth.InvalidIdTokenError as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 401

    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500

if __name__ == '__main__':
    app.run()
