import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database import db
from models.payment import Payment
from schemas.payment_schema import PaymentSchema

PAYMENT_ENDPOINT = "/api/payments"
logger = logging.getLogger(__name__)


class PaymentsResource(Resource):
    def get(self, id=None):
        """
        PaymentsResource GET method. Retrieves all payments found in the
        mamaput database. If this id is provided then the payment with the
        associated payment_id is retrieved.

        :param id: Payment ID to retrieve, this path parameter is optional
        :return: Payment, 200 HTTP status code
        """
        if not id:
            order_id = request.args.get("order_id")
            logger.info(
                f"Retrieving all payments, optionally filtered by "
                f"order_id={order_id}"
            )

            return self._get_all_payments(order_id), 200

        logger.info(f"Retrieving payment by id {id}")

        try:
            return self._get_payment_by_id(id), 200
        except NoResultFound:
            abort(404, message="payment not found")

    def _get_payment_by_id(self, payment_id):
        """retrieve payment by payment id"""
        payment = Payment.query.filter_by(payment_id=payment_id).first()
        payment_json = PaymentSchema().dump(payment)

        if not payment_json:
            raise NoResultFound()

        logger.info(f"Payment retrieved from database {payment_json}")
        return payment_json

    def _get_all_payments(self, order_id):
        """retrieve all payments"""
        if order_id:
            payments = Payment.query.filter_by(order_id=order_id).all()
        else:
            payments = Payment.query.all()

        payments_json = [
            PaymentSchema().dump(payment) for payment in payments]

        logger.info("Payment successfully retrieved.")
        return payments_json

    def post(self):
        """
        paymentsResource POST method. Adds a new Payment to the database.

        :return: Payment.payment_id, 201 HTTP status code.
        """
        payment = PaymentSchema().load(request.get_json())

        try:
            db.session.add(payment)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this payment is already in the database. "
                f"Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return payment.payment_id, 201
