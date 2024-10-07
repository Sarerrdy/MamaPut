import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.address import Address
from schemas.address_schema import AddressSchema

ADDRESSES_ENDPOINT = "/api/addresses"
logger = logging.getLogger(__name__)


class AddressesResource(Resource):
    def get(self, id=None):
        """
        AddressesResource GET method. Retrieves all addresses found in the
        mamaput database. If this id is provided then the address with the
        associated address_id is retrieved.

        :param id: Address ID to retrieve, this path parameter is optional
        :return: Address, 200 HTTP status code
        """
        if not id:
            user_id = request.args.get("user_id")
            logger.info(
                f"Retrieving all addresses, optionally filtered by "
                f"user_id={user_id}"
            )

            return self._get_all_addresses(user_id), 200

        logger.info(f"Retrieving address by id {id}")

        try:
            return self._get_address_by_id(id), 200
        except NoResultFound:
            abort(404, message="address not found")

    def _get_address_by_id(self, address_id):
        """retrieve address by address id"""
        address = Address.query.filter_by(address_id=address_id).first()
        address_json = AddressSchema().dump(address)

        if not address_json:
            raise NoResultFound()

        logger.info(f"Address retrieved from database {address_json}")
        return address_json

    def _get_all_addresses(self, user_id):
        """retrieve all addresses"""
        if user_id:
            addresses = Address.query.filter_by(user_id=user_id).all()
        else:
            addresses = Address.query.all()

        addresses_json = [
            AddressSchema().dump(address) for address in addresses]

        logger.info("Address successfully retrieved.")
        return addresses_json

    def post(self):
        """
        AddressesResource POST method. Adds a new Address to the database.

        :return: Address.address_id, 201 HTTP status code.
        """
        address = AddressSchema().load(request.get_json())

        try:
            db.session.add(address)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this address is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return address.address_id, 201
