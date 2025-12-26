from flask import Flask
from configurations.config import Config
from controllers.users import user_controller
from controllers.products import product_controller
from controllers.carts import cart_controller
from controllers.orders import order_controller
from controllers.reviews import review_controller
from controllers.promotions import promotion_controller
from controllers.analytics import analytics_controller
from controllers.support import support_controller

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        app.register_blueprint(user_controller)
        app.register_blueprint(product_controller)
        app.register_blueprint(cart_controller)
        app.register_blueprint(order_controller)
        app.register_blueprint(review_controller)
        app.register_blueprint(promotion_controller)
        app.register_blueprint(analytics_controller)
        app.register_blueprint(support_controller)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)