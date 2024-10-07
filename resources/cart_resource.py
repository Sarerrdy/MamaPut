import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.cart import Cart
from schemas.cart_schema import CartSchema

CART_ENDPOINT = "/api/carts"
logger = logging.getLogger(__name__)


class CartsResource(Resource):
    def get(self, id=None):
        """
        CartsResource GET method. Retrieves all carts found in the
        mamaput database. If this id is provided then the cart with the
        associated cart_id is retrieved.

        :param id: Cart ID to retrieve, this path parameter is optional
        :return: Cart, 200 HTTP status code
        """
        if not id:
            user_id = request.args.get("user_id")
            logger.info(
                f"Retrieving all carts, optionally filtered by "
                f"user_id={user_id}"
            )

            return self._get_all_carts(user_id), 200

        logger.info(f"Retrieving cart by id {id}")

        try:
            return self._get_cart_by_id(id), 200
        except NoResultFound:
            abort(404, message="cart not found")

    def _get_cart_by_id(self, cart_id):
        """retrieve cart by cart id"""
        cart = Cart.query.filter_by(cart_id=cart_id).first()
        cart_json = CartSchema().dump(cart)

        if not cart_json:
            raise NoResultFound()

        logger.info(f"Cart retrieved from database {cart_json}")
        return cart_json

    def _get_all_carts(self, user_id):
        """retrieve all carts"""
        if user_id:
            carts = Cart.query.filter_by(user_id=user_id).all()
        else:
            carts = Cart.query.all()

        carts_json = [
            CartSchema().dump(cart) for cart in carts]

        logger.info("Cart successfully retrieved.")
        return carts_json

    def post(self):
        """
        CartesResource POST method. Adds a new Cart to the database.

        :return: Cart.cart_id, 201 HTTP status code.
        """
        cart = CartSchema().load(request.get_json())

        try:
            db.session.add(cart)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this cart is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return cart.cart_id, 201
