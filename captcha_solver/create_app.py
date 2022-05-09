from captcha_solver.captcha_solver.thread import SolverThread
from captcha_solver.config import Config
from captcha_solver.flask import App
from captcha_solver.view import init_views


def create_app():
    app = App("captcha_solver")

    app.config.from_object(Config)

    thread = SolverThread(refresh_time=5, app=app)
    thread.start()

    init_views(app)

    return app
