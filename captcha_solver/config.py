import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "")

    API_URL = "http://localhost:5000"

    DEBUG = os.getenv("DEBUG", True)
    TESTING = bool(os.getenv("TESTING", False))

    UPLOAD_FOLDER = '/Users/a1/univ/master/machine-learning/captcha_solver/static'
