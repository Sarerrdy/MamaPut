import logging
import time

from flask import request
from flask_restful import Resource, abort, current_app

# from api import mail

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
import jwt

from database import db
from mailer import send_new_order_notification, send_order_confirmation, send_order_status_update
from models.order import Order
from models.menu import Menu
from models.user import User

from schemas.order_schema import OrderSchema
from schemas.order_details_schema import OrderDetailsSchema
from schemas.user_Address_schemas import AddressSchema
from schemas.payment_schema import PaymentSchema
from schemas.shipping_info_schema import ShippingInfoSchema


ORDERS_ENDPOINT = "/api/orders"
logger = logging.getLogger(__name__)


def verify_auth_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except:
        return
    return data


def generate_auth_token(self, expires_in=300):
    return jwt.encode(
        {'sub': "12345", 'exp': time.time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')


class OrdersResource(Resource):
    def get(self, id=None):
        """
        OrdersResource GET method. Retrieves all orders found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the order with the associated id is retrieved.

        :param id: Order ID to retrieve, this path parameter is optional
        :return: Order, 200 HTTP status code        """

        if request.endpoint == "checkerToken":
            return self._get_checker(), 200
        # if request.endpoint == "verifycheckerToken":
        #     return self._verify_checker(), 200

        if not id:
            status = request.args.get("status")
            checkerToken = request.args.get("checkerToken")
            user_id = request.args.get("user_id")
            logger.info(
                f"Retrieving all orders, optionally filtered by "
                f"status={status}"
            )
            if checkerToken:
                return self._verify_checker(checkerToken), 200
            if user_id:
                # return all oders by this user
                return self._get_order_by_userid(user_id), 200
            return self._get_all_orders(status), 200

        logger.info(f"Retrieving orders by id {id}")

        try:
            return self._get_order_by_id(id), 200
        except NoResultFound:
            abort(404, message="order not found")

    def _get_order_by_id(self, order_id):
        """retrieve order by order id"""
        if order_id:
            order = Order.query.get_or_404(order_id)
            order_schema = OrderSchema()
            order_json = order_schema.dump(order)
            logger.info(
                "Orders successfully retrieved from  _get_order_by_id(self, order_id)")
            return order_json
        else:
            # orders = Order.query.all()
            # orders_schema = OrderSchema(many=True)
            # orders_json = orders_schema.dump(orders)
            return 404

    def _get_order_by_userid(self, user_id):
        """retrive all orders associated to user_id"""
        if user_id:
            order = Order.query.filter_by(
                user_id=user_id).all()
            order_schema = OrderSchema(many=True)
            order_json = order_schema.dump(order)
            logger.info(
                "Orders successfully retrieved from _get_order_by_userid(user_id).")
            return order_json
        else:
            return 404

    def _get_all_orders(self, status):
        """retrieve all order"""
        if status:
            orders = Order.query.filter_by(status=status).all()
        else:
            orders = Order.query.all()

        orders_json = [
            OrderSchema().dump(order) for order in orders]

        logger.info("Orders successfully retrieved.")
        logger.info(
            "Orders successfully retrieved from _get_all_orders(self, status)")
        return orders_json

    def _get_checker(self):
        """generate unique order identifier"""
        token = generate_auth_token(300)
        return token

    def _verify_checker(self, token):
        """check validity of Token"""
        token = verify_auth_token(token)
        logger.info(f"Token: {token}")
        if token:
            logger.info("Token correct")
            return True
        logger.info("Token failed")
        return False

    # Post Menthod

    def post(self):
        """
        OrdersResource POST method. Adds a new order item to the database.

        :return: order.order_id, 201 HTTP status code.
        """
        # from api import mail  # Import here to avoid circular import
        req_data = request.get_json()
        neworder = req_data["orders"]["order"]
        orderDetails = req_data["orders"]["order_details"]
        newAddress = req_data["orders"]["orderAddress"]
        payment = req_data["orders"]["payments"]
        shipping = req_data["orders"]["shipping_info"]

        # order
        order = OrderSchema().load(neworder)
        order.date_ordered = datetime.now()
        # order details
        orderDetailsSchema = OrderDetailsSchema(many=True)
        orderDts = orderDetailsSchema.load(orderDetails)

        # payment

        payment["payment_date"] = None
        payment = PaymentSchema().load(payment)

        # shipping
        # shippingJson = json.loads(shipping)
        shipping["shipped_date"] = None

        if shipping["shipping_Method"] == "express":
            deliverytime = datetime.now() + timedelta(hours=2)  # 2 hours delivery
            shipping["expected_delivery_date"] = deliverytime.isoformat()
        elif shipping["shipping_Method"] == "standard":
            deliverytime = datetime.now() + timedelta(hours=5)  # 5 hours delivery
            shipping["expected_delivery_date"] = deliverytime.isoformat()
        else:
            deliverytime = datetime.now() + timedelta(minutes=15)  # 15 minutes delivery
            shipping["expected_delivery_date"] = deliverytime.isoformat()
        shipping = ShippingInfoSchema().load(shipping)

        try:
            # add order
            order.expected_date_of_delivery = shipping.expected_delivery_date
            db.session.add(order)
            db.session.commit()

            # update new address only with id==0
            if (newAddress["address_id"] == 0):
                newAddressJson = AddressSchema().load(newAddress)
                newAddressJson.address_id = None
                db.session.add(newAddressJson)
                db.session.commit()
                shipping.address_id = newAddressJson.address_id

            # update order details
            for orderDetail in orderDts:
                orderDetail.order = order
                orderDetail.order_id = order.order_id
                menu = Menu.query.filter_by(
                    menu_id=orderDetail.menu_id).first()
                orderDetail.menu = menu
            db.session.add_all(orderDts)

            # update payment with order_id
            payment.order_id = order.order_id
            db.session.add(payment)

            # update shipping with address id and order id
            shipping.order_id = order.order_id
            if (int(newAddress["address_id"]) > 0):
                shipping.address_id = newAddress["address_id"]
            db.session.add(shipping)

            # commit all datatset
            db.session.commit()

            if payment.payment_Method == "payondelivery":
                try:
                    # Send confirmation email to user and notification to admin
                    user = User.query.get_or_404(order.user_id)
                    send_order_confirmation(user.email, order.order_id)
                    send_new_order_notification(order.order_id)

                except IntegrityError as e:
                    logger.error(
                        f"Email sending failed!"
                        f"Error: {e}"
                    )

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this order is already in the database. "
                f"Error: {e}"
            )
            abort(500, message="Unexpected Error!")
        else:
            if payment.payment_Method == "payondelivery":
                return order.order_id, 201
            else:
                payment = PaymentSchema().dump(payment)
                return payment

    # Put endpoint
    def put(self, id):
        """
        OrdersResource PUT method. Updates an order item in the database.

        :param order_id: ID of the order item to update.
        :return: Updated order item JSON, 200 HTTP status code if successful,
        404 if not found.
        """
        order = Order.query.filter_by(order_id=id).first()
        if order is None:
            abort(404, message="Order item not found!")

        try:
            order_data = request.get_json()
            loaded_order = OrderSchema().load(order_data, partial=True)
            old_status = order.status  # Track the old status
            order.status = loaded_order.status
            # Update other fields as necessary
            db.session.commit()

            # Notify the user if the status has changed
            if old_status != order.status:
                user = User.query.get_or_404(order.user_id)
                send_order_status_update(
                    user.email, order.order_id, order.status)

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, could not update order item. "
                f"Error: {e}"
            )
            abort(500, message="Unexpected Error!")
        else:
            return (OrderSchema().dump(order)), 200
