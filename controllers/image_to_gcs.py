from google.cloud import storage
import json

# Initialize GCS Client
storage_client = storage.Client.from_service_account_json('config/google-cloud-storage/serviceAccount.json')

def save_image_to_gcs(image, filename):
    try:
        bucket_name = 'img-history-storage-bucket'
        bucket = storage_client.bucket(bucket_name)
        image.filename = filename
        blob = bucket.blob('history/' + image.filename)  # Save to "history" folder

        # Set stream position to the beginning
        image.seek(0)

        blob.upload_from_file(image)

        image_url = blob.public_url

        return image_url
    except:
        error_message = {'message': 'Image not uploaded to GCS!'}
        return json.dumps(error_message), 500

def save_image_to_tmp_gcs(image, filename):
    try:
        bucket_name = 'img-history-storage-bucket'
        bucket = storage_client.bucket(bucket_name)
        image.filename = filename
        blob = bucket.blob('tmp/' + image.filename)  # Save to "tmp" folder

        # Set stream position to the beginning
        image.seek(0)

        blob.upload_from_file(image)

        image_url_tmp = blob.public_url

        return image_url_tmp
    except:
        error_message = {'message': 'Image not uploaded to temporary GCS!'}
        return json.dumps(error_message), 500

def delete_image_from_tmp_gcs(filename):
    try:
        bucket_name = 'img-history-storage-bucket'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('tmp/' + filename)  # Path to the image in "tmp" folder
        blob.delete()
    except:
        error_message = {'message': 'Failed to delete image from temporary GCS!'}
        return json.dumps(error_message), 500
