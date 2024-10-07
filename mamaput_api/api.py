from mamaput_api.constants import PROJECT_ROOT, MAMAPUT_DATABASE
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask
import logging
import sys
from os import path, getenv
from mamaput_api.database import db
from dotenv import load_dotenv


from mamaput_api.resources.user_resource import UsersResource, USERS_ENDPOINT
from mamaput_api.resources.address_resource import AddressesResource, ADDRESSES_ENDPOINT
from mamaput_api.resources.category_resource import CategoriesResource, CATEGORIES_ENDPOINT
from mamaput_api.resources.menu_resource import MenusResource, MENUS_ENDPOINT
from mamaput_api.resources.order_resource import OrdersResource, ORDERS_ENDPOINT
from mamaput_api.resources.review_resource import ReviewsResource, REVIEW_ENDPOINT
from mamaput_api.resources.payment_resource import PaymentsResource, PAYMENT_ENDPOINT
from mamaput_api.resources.cart_resource import CartsResource, CART_ENDPOINT
from mamaput_api.resources.shipping_info_resource import ShippingInfoResource, \
    SHIPPING_ENDPOINT
from mamaput_api.resources.order_details_resource import OrderDetailsResource, \
    ORDERDETAILS_ENDPOINT

load_dotenv()  # Load environment variables from .env file
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def create_app(db_location):
    # def create_app():  # prooduction code
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-RESTful API,
    and Flask-SQLAlchemy connection

    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """
    # This configures our logging, writes all logs to file "mamaput_api.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler(
            "mamaput_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'QZ0_IC8I_I1ueVP9Gl5bNUZbFv2hyfkcuOhWVfAWfUQ'
    app.config['SECRET_KEY'] = getenv(
        'SECRET_KEY', 'default_secret_key')  # Production config
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app, resources={
    #      r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})
    CORS(app, resources={
         r"/api/*": {"origins": ["https://moray-large-vervet.ngrok-free.app ", "https://live-fast-skylark.ngrok-free.app"]}})

    app.config["SQLALCHEMY_DATABASE_URI"] = db_location

    # app.config['SQLALCHEMY_DATABASE_URI'] = getenv(
    #     'DATABASE_URL', "sqlite:////{PROJECT_ROOT}" + "/mamaput.db")
    JWTManager(app)
    db.init_app(app)

    api = Api(app)
    api.add_resource(UsersResource, USERS_ENDPOINT,
                     f"{USERS_ENDPOINT}/<id>", f"{USERS_ENDPOINT}/login")
    api.add_resource(UsersResource, "/api/login", endpoint="login")
    api.add_resource(UsersResource, "/api/token", endpoint="token")
    api.add_resource(UsersResource, "/api/register", endpoint="register")
    api.add_resource(AddressesResource, ADDRESSES_ENDPOINT,
                     f"{ADDRESSES_ENDPOINT}/<id>")
    api.add_resource(CategoriesResource, CATEGORIES_ENDPOINT,
                     f"{CATEGORIES_ENDPOINT}/<id>")
    api.add_resource(MenusResource, MENUS_ENDPOINT,
                     f"{MENUS_ENDPOINT}/<id>")
    api.add_resource(OrdersResource, ORDERS_ENDPOINT,
                     f"{ORDERS_ENDPOINT}/<id>")
    api.add_resource(OrdersResource, "/api/checkerToken",
                     endpoint="checkerToken")
    api.add_resource(ReviewsResource, REVIEW_ENDPOINT,
                     f"{REVIEW_ENDPOINT}/<id>")
    api.add_resource(OrderDetailsResource, ORDERDETAILS_ENDPOINT,
                     f"{ORDERDETAILS_ENDPOINT}/<id>")
    api.add_resource(PaymentsResource, PAYMENT_ENDPOINT,
                     f"{PAYMENT_ENDPOINT}/<id>")
    api.add_resource(ShippingInfoResource, SHIPPING_ENDPOINT,
                     f"{SHIPPING_ENDPOINT}/<id>")
    api.add_resource(CartsResource, CART_ENDPOINT,
                     f"{CART_ENDPOINT}/<id>")
    return app


app = create_app(f"sqlite:////{PROJECT_ROOT}/{MAMAPUT_DATABASE}")


if __name__ == "__main__":
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{MAMAPUT_DATABASE}")
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
