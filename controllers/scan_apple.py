import tensorflow as tf
import tensorflow.lite as tflite
import tensorflow.keras.utils as keras_utils
import tensorflow.keras.preprocessing.image as tfimage
import numpy as np
from PIL import Image
from io import BytesIO
import requests

class Scanner:
    # Pre-processing
    @staticmethod
    # def preprocessing(save_path_tmp):
    #     # PreProcessing here
    #     # TODO: Add your image preprocessing code here
    #     # For example, you can resize, normalize, or apply any transformations to the image
    #     # image_path = 'image/image.jpeg'  # Replace with the actual path to the user-provided image
    #     image = tfimage.load_img(save_path_tmp, target_size=(150, 150))
    #     image = tfimage.img_to_array(image)
    #     image = np.expand_dims(image, axis=0)
    #     image = image.astype('float32')
    #     image /= 255.0
    #     preprocessed_image = image

    #     return preprocessed_image

    def preprocessing(image_url):
        response = requests.get(image_url)
        image_content = response.content
        image = Image.open(BytesIO(image_content))
        image = image.convert('RGB')
        image = image.resize((150, 150))
        image = np.array(image).astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
        

    # Classification
    @staticmethod
    def img_classification(preprocessed_image):
        # Classification here
        # Load the TensorFlow Lite model
        interpreter = tflite.Interpreter(model_path='controllers/fruitmate_model.tflite')
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Set the input tensor
        input_index = input_details[0]['index']
        interpreter.set_tensor(input_index, preprocessed_image)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_index = output_details[0]['index']
        output = interpreter.get_tensor(output_index)[0]

        # Map the class labels
        labels = ['unripe', 'ripe', 'overripe']
        pred_data = {label: str(pred) for label, pred in zip(labels, output)}

        # Get the predicted class with the highest probability
        classification_result = max(pred_data, key=pred_data.get)

        
        return classification_result
