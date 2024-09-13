import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.shipping_info import ShippingInfo
from schemas.shipping_info_schema import ShippingInfoSchema

SHIPPING_ENDPOINT = "/api/shipping_infos"
logger = logging.getLogger(__name__)


class ShippingInfoResource(Resource):
    def get(self, id=None):
        """
        ShippingInfoResource GET method. Retrieves all shippingInfo found in
        the mamaput database. If this id is provided then the shipping_info
        with the associated shipping_info_id is retrieved.

        :param id: Shipping_Info ID to retrieve, this path parameter is
        optional
        :return: ShippingInfo, 200 HTTP status code
        """
        if not id:
            order_id = request.args.get("order_id")
            logger.info(
                f"Retrieving all shipping_info, optionally filtered by "
                f"order_id={order_id}"
            )

            return self._get_all_shipping_info(order_id), 200

        logger.info(f"Retrieving shipping by id: {id}")

        try:
            return self._get_shipping_info_by_id(id), 200
        except NoResultFound:
            abort(404, message="shipping_info not found")

    def _get_shipping_info_by_id(self, shipping_info_id):
        """retrieve shipping_info by shipping_info_id"""
        shipping_info = ShippingInfo.query.filter_by(
            shipping_info_id=shipping_info_id).first()
        shipping_info_json = ShippingInfoSchema().dump(shipping_info)

        if not shipping_info_json:
            raise NoResultFound()

        logger.info(
            f"shipping_info retrieved from database {shipping_info_json}")
        return shipping_info_json

    def _get_all_shipping_info(self, order_id):
        """retrieve all shipping_info"""
        if order_id:
            shipping_infos = ShippingInfo.query.filter_by(
                order_id=order_id).all()
        else:
            shipping_infos = ShippingInfo.query.all()

        shipping_infos_json = [ShippingInfoSchema().dump(
            shippinginfo) for shippinginfo in shipping_infos]

        logger.info("ShippingInfo successfully retrieved.")
        return shipping_infos_json

    def post(self):
        """
        ShippingInfosResource POST method. Adds a new ShippingInfo to the
        database.

        :return: shipping_infos.shipping_info_id, 201 HTTP status code.
        """
        shippinginfo = ShippingInfoSchema().load(request.get_json())

        try:
            db.session.add(shippinginfo)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this shipping_info is already in database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return shippinginfo.shipping_info_id, 201
