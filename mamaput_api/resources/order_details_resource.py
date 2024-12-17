import logging
from models.menu import Menu

from flask import jsonify, request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.order import Order
from models.order_details import Order_Detail
from schemas.order_details_schema import OrderDetailsSchema
# from schemas.menu_order_schema import MenuOrderSchema

ORDERDETAILS_ENDPOINT = "/api/orderdetails"
logger = logging.getLogger(__name__)


class OrderDetailsResource(Resource):
    def get(self, id=None):
        """
        OrderDetailsResource GET method. Retrieves all orderdetails found in
        the mamaput database, unless the id path parameter is provided. If
        this id is provided then the orderdetails with the associated id
        is retrieved.

        :param id: Orderdetails ID to retrieve, this path parameter is optional
        :return: Orderdetail, 200 HTTP status code
        """
        if not id:
            order_id = request.args.get("order_id")
            logger.info(
                f"Retrieving all orderDetailss, optionally filtered by "
                f"status={order_id}"
            )

            return self._get_all_orderdetails(order_id), 200

        logger.info(f"Retrieving orders by id {id}")

        try:
            return self._get_orderdetails_by_id(id), 200
        except NoResultFound:
            abort(404, message="Orderdetail not found")

    def _get_orderdetails_by_id(self, order_details_id):
        """retrieve Orderdetail by Orderdetail id"""
        orderdetail = Order_Detail.query.filter_by(
            order_details_id=order_details_id).join(Menu).first()
        orderdetail_json = OrderDetailsSchema().dump(orderdetail)

        if not orderdetail_json:
            raise NoResultFound()

        logger.info(f"Orderdetails retrieved from database {orderdetail_json}")
        return orderdetail_json

    def _get_all_orderdetails(self, order_id):
        """retrieve all Orderdetails"""
        if order_id:
            orderdetails = Order_Detail.query.filter_by(
                order_id=order_id).join(Menu).all()
            for detail in orderdetails:
                logger.info(
                    f"OrderDetail: {detail.order_details_id}, Menu: {detail.menu}, Order: {detail.order}")
            logger.info(f"ORDER-DETAILS: {orderdetails}")
        else:
            orderdetails = Order_Detail.query.all()

        orderdetails_json = OrderDetailsSchema(many=True).dump(orderdetails)
        logger.info(f"ORDER-DETAILS: {orderdetails}")
        return orderdetails_json
        # orderdetails_json = [
        #     OrderDetailsSchema().dump(orderdetail)
        #     for orderdetail in orderdetails]

        logger.info("Orders successfully retrieved.")
        return orderdetails_json

    def post(self):
        """
        OrdersResource POST method. Adds a new Orderdetails item to
        the database.

        :return: Order_Detail.order_id, 201 HTTP status code.
        """
        orderdetail = OrderDetailsSchema().load(request.get_json())

        try:
            db.session.add(orderdetail)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this orderdetail is already in the database"
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return Order_Detail.order_details_id, 201
