from flask import Blueprint

captcha_solver_blueprint = Blueprint('CaptchaSolverViews', __name__, template_folder='templates')

from .views import *  # noqa
