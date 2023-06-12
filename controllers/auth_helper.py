# import firebase_admin
# from firebase_admin import credentials

# # Inisialisasi Firebase Admin SDK jika belum diinisialisasi sebelumnya
# if not firebase_admin._apps:
#     cred = credentials.Certificate("config/firebase/serviceAccount.json")
#     firebase_admin.initialize_app(cred)

from firebase_admin import auth

def get_uid(request):
    # Get token from request headers
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None
    
    token = auth_header.replace('Bearer ', '')

    try:
        # Verify token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        # Get UID from verified token
        uid = decoded_token['uid']
        return uid
    except auth.InvalidIdTokenError:
        return None
