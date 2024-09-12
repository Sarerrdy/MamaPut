import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.order import Order
from schemas.order_schema import OrderSchema
# from schemas.menu_order_schema import MenuOrderSchema

ORDERS_ENDPOINT = "/api/orders"
logger = logging.getLogger(__name__)


class OrdersResource(Resource):
    def get(self, id=None):
        """
        OrdersResource GET method. Retrieves all orders found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the order with the associated id is retrieved.

        :param id: Order ID to retrieve, this path parameter is optional
        :return: Order, 200 HTTP status code
        """
        if not id:
            status = request.args.get("status")
            logger.info(
                f"Retrieving all orders, optionally filtered by "
                f"status={status}"
            )

            return self._get_all_orders(status), 200

        logger.info(f"Retrieving orders by id {id}")

        try:
            return self._get_order_by_id(id), 200
        except NoResultFound:
            abort(404, message="order not found")

    def _get_order_by_id(self, order_id):
        """retrieve order by order id"""
        order = Order.query.filter_by(order_id=order_id).first()
        order_json = OrderSchema().dump(order)

        if not order_json:
            raise NoResultFound()

        logger.info(f"Order retrieved from database {order_json}")
        return order_json

    def _get_all_orders(self, status):
        """retrieve all order"""
        if status:
            orders = Order.query.filter_by(status=status).all()
        else:
            orders = Order.query.all()

        orders_json = [
            OrderSchema().dump(order) for order in orders]

        logger.info("Orders successfully retrieved.")
        return orders_json

    def post(self):
        """
        OrdersResource POST method. Adds a new order item to the database.

        :return: order.order_id, 201 HTTP status code.
        """
        order = OrderSchema().load(request.get_json())

        try:
            db.session.add(order)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this order is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return order.order_id, 201
