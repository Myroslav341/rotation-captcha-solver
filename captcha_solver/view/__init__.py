from captcha_solver.flask import App


def init_views(app: App):
    from captcha_solver.view.blueprint import captcha_solver_blueprint

    app.register_blueprint(captcha_solver_blueprint)
