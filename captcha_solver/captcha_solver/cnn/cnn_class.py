import os
import cv2
from keras.models import load_model
from typing import List


class CNN:
    def __init__(self, model_name: str = 'latest.h5'):
        self.model = load_model(os.path.join('captcha_solver', 'captcha_solver', 'cnn', 'models', model_name))

    def predict(self, file_path: str) -> List[float]:
        img_data = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img_data = cv2.resize(img_data, (64, 64))

        img_data = img_data.reshape(1, 64, 64, 1)

        img_data = img_data.astype('float32')

        img_data /= 255

        f = self.model.predict(img_data)

        return f
