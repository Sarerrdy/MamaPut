import logging

from flask import request
from flask_restful import Resource, abort

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.address import Address
from schemas.user_Address_schemas import AddressSchema

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
            address_schema = AddressSchema(many=True)
            addresses_json = address_schema.dump(addresses)

            # addresses_json = [
            #     AddressSchema().dump(address) for address in addresses]

            logger.info("Address successfully retrieved.")
            return addresses_json
        else:
            return {'message': "this User has no registered address"}, 400

    def post(self):
        """
        AddressesResource POST method. Adds a new Address to the database.

        :return: Address.address_id, 201 HTTP status code.
        """

        req_data = request.get_json()
        newAdr = req_data["newaddress"]
        address = AddressSchema().load(newAdr)

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
            address = AddressSchema().dump(address)
            return {'message': "Address was created succesfully", 'data': address}, 201

    def put(self, id):
        """
        AddressResource PUT method. Updates existing address in the database.
        :param id: ID of the address to be updated.
        :return: Updated address data and HTTP status code.
        """
        try:
            req_data = request.get_json(force=True)
            if not req_data:

                return {'message': "No input data provided"}, 405
            addr = AddressSchema().load(req_data)

            existingAddr = Address.query.filter_by(address_id=id).first()

            # assign updated address
            existingAddr.address = addr.address
            existingAddr.town = addr.address
            existingAddr.state = addr.state
            existingAddr.lga = addr.lga
            existingAddr.landmark = addr.landmark
            existingAddr.user_id = addr.user_id

            db.session.commit()
            address = AddressSchema().dump(existingAddr)
            print(f"ADDRESS: {address}")
            return {'message': "Address was updated succesfully", 'data': address}, 201
        except:
            return {"message": "Address update failed"}, 400

    def delete(self, id):
        """
        AddressResource DELETE method. Deletes existing address in the database.
        :param id: ID of the address to be deleted.
        :return: HTTP status code.
        """
        if id is not None:
            existingAddr = Address.query.filter_by(address_id=id).first()
            if not existingAddr:
                return {'message': "Address not found"}, 404
            try:
                # Here we delete the existing address
                db.session.delete(existingAddr)
                db.session.commit()
                return {'message': "Address deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {'message': "An error occurred while deleting the address: " + str(e)}, 500

        else:
            return {'message': "Address id cannot be empty"}, 400
