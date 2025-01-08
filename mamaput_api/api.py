from flask_migrate import Migrate
from mailer import send_order_confirmation, send_new_order_notification
import os
from sqlalchemy.exc import IntegrityError
from flask import Flask, abort, jsonify, request
import requests
from constants import PROJECT_ROOT, MAMAPUT_DATABASE
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

import logging
import sys
from os import path, getenv
from database import db
from dotenv import load_dotenv

from models.order import Order
from models.user import User
from models.payment import Payment

from resources.user_resource import UsersResource, USERS_ENDPOINT
from resources.address_resource import AddressesResource, ADDRESSES_ENDPOINT
from resources.category_resource import CategoriesResource, CATEGORIES_ENDPOINT
from resources.menu_resource import MenusResource, MENUS_ENDPOINT
from resources.order_resource import OrdersResource, ORDERS_ENDPOINT
from resources.payment_resource import PaymentsResource, PAYMENT_ENDPOINT
from resources.cart_resource import CartsResource, CART_ENDPOINT
from resources.shipping_info_resource import ShippingInfoResource, SHIPPING_ENDPOINT
from resources.order_details_resource import OrderDetailsResource, ORDERDETAILS_ENDPOINT
from resources.role_resource import RolesResource, ROLES_ENDPOINT
from resources.review_resource import ReviewsResource, REVIEW_ENDPOINT

load_dotenv()  # Load environment variables from .env file
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
CORS(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[logging.FileHandler("mamaput_api.log"), logging.StreamHandler()],
)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'images')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['UPLOAD_FOLDER'] = getenv('UPLOAD_FOLDER')
max_content_length = getenv('MAX_CONTENT_LENGTH')
if max_content_length:
    app.config['MAX_CONTENT_LENGTH'] = int(eval(max_content_length))
app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'default_secret_key')
paystack_secret_key = getenv('PAYSTACK_SECRET_KEY')
app.config['BASE_URL'] = getenv('BASE_URL')

CORS(app, resources={
    r"/api/*": {"origins": ["https://mamaputapp.onrender.com", "http://localhost:4173", "http://localhost:5173", "https://api.paystack.co"]}
})

db_location = f"sqlite:////{PROJECT_ROOT}/{MAMAPUT_DATABASE}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_location
JWTManager(app)
db.init_app(app)

# Register resources
api.add_resource(UsersResource, USERS_ENDPOINT, f"{USERS_ENDPOINT}/<int:id>",
                 f"{USERS_ENDPOINT}/login", f"{USERS_ENDPOINT}/assign_role", f"{USERS_ENDPOINT}/remove_role")
api.add_resource(UsersResource, "/api/login", endpoint="login")
api.add_resource(UsersResource, "/api/token", endpoint="token")
api.add_resource(UsersResource, "/api/register", endpoint="register")
api.add_resource(UsersResource, "/api/assign_role", endpoint="assign_role")
api.add_resource(UsersResource, "/api/remove_role", endpoint="remove_role")
api.add_resource(UsersResource, "/api/reset-password",
                 endpoint="reset_password")
api.add_resource(UsersResource, "/api/forgot-password",
                 endpoint="forgot_password")

api.add_resource(RolesResource, ROLES_ENDPOINT)
api.add_resource(AddressesResource, ADDRESSES_ENDPOINT,
                 f"{ADDRESSES_ENDPOINT}/<id>")
api.add_resource(CategoriesResource, CATEGORIES_ENDPOINT,
                 f"{CATEGORIES_ENDPOINT}/<id>")
api.add_resource(MenusResource, MENUS_ENDPOINT, f"{MENUS_ENDPOINT}/<id>")
api.add_resource(OrdersResource, ORDERS_ENDPOINT, f"{ORDERS_ENDPOINT}/<id>")
api.add_resource(OrdersResource, "/api/checkerToken", endpoint="checkerToken")
api.add_resource(OrderDetailsResource, ORDERDETAILS_ENDPOINT,
                 f"{ORDERDETAILS_ENDPOINT}/<id>")
api.add_resource(PaymentsResource, PAYMENT_ENDPOINT,
                 f"{PAYMENT_ENDPOINT}/<id>")
api.add_resource(ShippingInfoResource, SHIPPING_ENDPOINT,
                 f"{SHIPPING_ENDPOINT}/<id>")
api.add_resource(CartsResource, CART_ENDPOINT, f"{CART_ENDPOINT}/<id>")
api.add_resource(ReviewsResource, f"{REVIEW_ENDPOINT}/<int:menu_id>")


@app.route('/payment/callback', methods=['GET', 'POST'])
def payment_callback():
    reference = request.args.get('reference')
    logger.info("PAYMENT_CALLBACK CALLED")
    if reference:
        payment = Payment.query.filter_by(reference=reference).first()
        if payment and payment.payment_status == 'success':
            return jsonify({"status": "success", "message": "Payment verified"}), 200
    return jsonify({"status": "failed", "message": "Invalid reference"}), 400


@app.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    payload = request.get_json()
    if payload and payload['event'] == 'charge.success':
        reference = payload['data']['reference']
        amount = payload['data']['amount']

        if not verify_payment(reference):
            abort(400, message="Payment verification failed!")

        payment = Payment.query.filter_by(reference=reference).first()
        if payment:
            payment.amount = amount
            payment.payment_status = 'success'
            db.session.commit()

            try:
                order = Order.query.filter_by(
                    order_id=payment.order_id).first()
                user = User.query.filter_by(user_id=order.user_id).first()
                email = user.email

                send_order_confirmation(email, payment.order_id)
                send_new_order_notification(order.order_id)

                logger.info(f"Confirmation mail sent to {email} successfully")
            except IntegrityError as e:
                logger.error(f"Email sending failed! Error: {e}")

            return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed", "message": "Invalid event"}), 400


def verify_payment(reference):
    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
        "Content-Type": "application/json",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['status'] == 'success':
            return True
        return False


if __name__ == "__main__":
    db_location = f"sqlite:////{PROJECT_ROOT}/{MAMAPUT_DATABASE}"
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
