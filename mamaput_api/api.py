from constants import PROJECT_ROOT, MAMAPUT_DATABASE
from flask_restful import Api
from flask import Flask
import logging
import sys
from os import path
from database import db
from resources.user_resource import UsersResource, USERS_ENDPOINT
from resources.address_resource import AddressesResource, ADDRESSES_ENDPOINT
from resources.category_resource import CategoriesResource, CATEGORIES_ENDPOINT
from resources.menu_resource import MenusResource, MENUS_ENDPOINT
from resources.order_resource import OrdersResource, ORDERS_ENDPOINT
from resources.review_resource import ReviewsResource, REVIEW_ENDPOINT

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


def create_app(db_location):
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
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location
    db.init_app(app)

    api = Api(app)
    api.add_resource(UsersResource, USERS_ENDPOINT,
                     f"{USERS_ENDPOINT}/<id>")
    api.add_resource(AddressesResource, ADDRESSES_ENDPOINT,
                     f"{ADDRESSES_ENDPOINT}/<id>")
    api.add_resource(CategoriesResource, CATEGORIES_ENDPOINT,
                     f"{CATEGORIES_ENDPOINT}/<id>")
    api.add_resource(MenusResource, MENUS_ENDPOINT,
                     f"{MENUS_ENDPOINT}/<id>")
    api.add_resource(OrdersResource, ORDERS_ENDPOINT,
                     f"{ORDERS_ENDPOINT}/<id>")
    api.add_resource(ReviewsResource, REVIEW_ENDPOINT,
                     f"{REVIEW_ENDPOINT}/<id>")
    return app


if __name__ == "__main__":
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{MAMAPUT_DATABASE}")
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True, port=5001)
