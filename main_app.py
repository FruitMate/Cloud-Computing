# Import packages
from flask import Flask, request
from datetime import datetime
from firebase_admin import auth
import json
import string
import random
import os

# Import from controllers
from controllers.scan_apple import Scanner
from controllers.image_to_gcs import save_image_to_gcs, save_image_to_tmp_gcs, delete_image_from_tmp_gcs
from controllers.history_to_firestore import save_history_to_firestore
from controllers.history_to_firestore import get_data_firestore_by_id


app = Flask(__name__)

app.debug = True

# Inizialize Scanner object
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
            return json.dumps({'error': 'Tipe konten tidak didukung'}), 415

        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return json.dumps({'error': 'Email dan password harus diisi'}), 400

        user = auth.get_user_by_email(email)

        custom_token = auth.create_custom_token(user.uid)

        uid = user.uid

        return json.dumps({'token': custom_token.decode(), 'uid': uid}), 200


    except auth.InvalidIdTokenError as e:
        return json.dumps({'error': str(e)}), 401

    except Exception as e:
        return json.dumps({'error': str(e)}), 500

# Route for scan apple
@app.route('/api/scan-apple', methods=['POST'])
def scan_apple():

    # Get all request body
    image = request.files['image']
    email = request.form['email']

    try:
        # Generate random text  for filename
        def generate_random_filename(length=10):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choices(characters, k=length))
            random_name = random_string
            return random_name

        # Get user from email login
        user = auth.get_user_by_email(email)

        # Get uid  from user login 
        uid = user.uid

        random_name = generate_random_filename(10)

        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')

        # Create filename for image from request body
        filename = f'{current_datetime}_{uid}_{random_name}.jpg'

        # Save image to temporary GCS and get the public URL
        image_url_tmp = save_image_to_tmp_gcs(image, filename=filename)

        # Run PreProcessing from class Scanner
        preprocessed_image = scanner.preprocessing(image_url_tmp)

        # Run Classification from class Scanner
        classification_result = scanner.img_classification(preprocessed_image)

        # Save image name to GCS and get the public URL
        image_url = save_image_to_gcs(image, filename=filename)

        # Delete the image from temporary GCS
        delete_image_from_tmp_gcs(filename)

        # Save uid, image_url, and classification_result to firestore
        save_history_to_firestore(uid, image_url, classification_result)

        response = {'code': 200, 'message': 'Klasifikasi Berhasil', 'prediction': classification_result}
        response_json = json.dumps(response)
        return response_json, 200
    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500


# Route for history
@app.route('/api/history', methods=['GET'])
# def get_scan_history():

#     # Get request body
#     email = request.form['email']

#     try:
#         # Get user from email login
#         user = auth.get_user_by_email(email)

#         # Get uid from user login
#         uid = user.uid

#         # RUn the function and return the response
#         return get_data_firestore_by_id(uid)
#     except Exception as e:
#         error_message = {'error': str(e)}
#         return json.dumps(error_message), 500

def get_scan_history():
    try:
        # Get email from query parameters
        email = request.args.get('email')

        if not email:
            return json.dumps({'error': 'Email harus disertakan dalam query parameters'}), 400

        # Get user from email login
        user = auth.get_user_by_email(email)

        # Get uid from user login
        uid = user.uid

        # Run the function and return the response
        return get_data_firestore_by_id(uid)

    except auth.InvalidIdTokenError as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 401

    except Exception as e:
        error_message = {'error': str(e)}
        return json.dumps(error_message), 500

if __name__ == '__main__':
    app.run()
