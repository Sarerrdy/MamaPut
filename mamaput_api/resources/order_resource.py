import logging
import json

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from database import db
from models.order import Order
from models.order_details import Order_Detail
from schemas.order_schema import OrderSchema
from schemas.order_details_schema import OrderDetailsSchema
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
        req_data = request.get_json()
        # new_order = Order()
        # new_order.total_price = order_data["total_price"]
        # new_order.date_ordered = order_data["date_ordered"]
        # new_order.expected_date_of_delivery = order_data["expected_date_of_delivery"],
        # new_order.status = order_data["status"],
        # new_order.user_id = order_data["user_id"]
        neworder = req_data["orders"]["order"]
        # neworder2 = neworder[0]
        # logger.info(f"NEWORDER: {neworder}")

        orderDetails = req_data["orders"]["order_details"]
        # logger.info(f"DETAILS: {orderDetails}")

        # update order details
        # for orderDetail in orderDetails:
        #     orderDetail.order = neworder

        # logger.info(f"order: {neworder}")
        # logger.info(f"orderDetails: {orderDetails}")

        order = OrderSchema().load(neworder)
        order.date_ordered = datetime.now()

        # order.expected_date_of_delivery = datetime.strptime(
        #     "2024-09-26T11:00:00", '%Y-%m-%dT%H:%M:%S')

        orderDetailsSchema = OrderDetailsSchema(many=True)
        orderDts = orderDetailsSchema.load(orderDetails)

        try:

            db.session.add(order)
            # update order details
            for orderDetail in orderDts:
                # details = Order_Detail
                # details.quantity = orderDetail.quantity
                # details.discount = orderDetail.discount
                orderDetail.order = order
                orderDetail.order_id = order.order_id

            db.session.add_all(orderDts)
            db.session.commit()

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this order is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            # orderDetail_json = [
            #     OrderDetailsSchema().dump(details) for details in orderDts]
            # logger.info(f"RETURNED: {orderDetail_json}")
            # return orderDetail_json, 201
            return order.order_id, 201
