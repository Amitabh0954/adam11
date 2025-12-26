from flask import Flask
from configurations.config import Config
from controllers.users import user_controller
from controllers.products import product_controller

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        app.register_blueprint(user_controller)
        app.register_blueprint(product_controller)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)