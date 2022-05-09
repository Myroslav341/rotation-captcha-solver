import os

from PIL import Image

from captcha_solver.captcha_solver import get_next_from_pictures_list, add_solved_picture
from captcha_solver.captcha_solver.cnn.cnn_class import CNN
from captcha_solver.lib.thread_base import InfiniteThreadBase


class SolverThread(InfiniteThreadBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cnn = CNN()

    def handler(self):
        picture = get_next_from_pictures_list()

        if not picture:
            return None

        file_path = os.path.join('captcha_solver', 'static', picture.file_name)
        value = self.cnn.predict(file_path)
        value = value[0]

        max_v = max(value)
        index = list(value).index(max_v)
        value = int(index) * 40

        picture.answer = value

        image = Image.open(os.path.join(self.app.config["UPLOAD_FOLDER"], picture.file_name))
        image = image.rotate(-float(picture.answer))

        new_path = os.path.join(self.app.config["UPLOAD_FOLDER"], f"solved_{picture.file_name}")
        image.save(new_path)

        picture.result_picture_file_name = f"solved_{picture.file_name}"
        add_solved_picture(picture=picture)
