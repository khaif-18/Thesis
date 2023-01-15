from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from project import router

        # Register Blueprints
        app.register_blueprint(router.router_bp)

        return app