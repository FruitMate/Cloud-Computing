import tensorflow as tf
import tensorflow.lite as tflite
import numpy as np
from PIL import Image
from io import BytesIO
import requests

class Scanner:
    # Pre-processing Image
    @staticmethod
    def preprocessing(image_url):
        response = requests.get(image_url)
        image_content = response.content
        image = Image.open(BytesIO(image_content))
        image = image.convert('RGB')
        image = image.resize((150, 150))
        image = np.array(image).astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
        

    # Classification Image
    @staticmethod
    def img_classification(preprocessed_image):
        interpreter = tflite.Interpreter(model_path='controllers/fruitmate_model.tflite')
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_index = input_details[0]['index']
        interpreter.set_tensor(input_index, preprocessed_image)

        interpreter.invoke()

        output_index = output_details[0]['index']
        output = interpreter.get_tensor(output_index)[0]

        labels = ['unripe', 'ripe', 'overripe']
        pred_data = {label: str(pred) for label, pred in zip(labels, output)}

        classification_result = max(pred_data, key=pred_data.get)
        
        return classification_result
