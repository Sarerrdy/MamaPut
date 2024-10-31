
import logging
import os
from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
import requests
from paystackapi.paystack import Paystack
from database import db
from models.payment import Payment
from schemas.payment_schema import PaymentSchema

PAYMENT_ENDPOINT = "/api/payments"
logger = logging.getLogger(__name__)
paystack_secret_key = os.getenv('PAYSTACK_SECRET_KEY')
paystack = Paystack(secret_key=paystack_secret_key)


class PaymentsResource(Resource):
    def post(self):
        """ Create a new payment """
        data = request.get_json()
        reference = data.get('reference')

        # Verify the payment with Paystack
        if not self.verify_payment(reference):
            abort(400, message="Payment verification failed!")

        payment = PaymentSchema().load(data)
        db.session.add(payment)
        try:
            db.session.commit()
            return PaymentSchema().dump(payment), 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Payment already exists")

    def verify_payment(self, reference):
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

    def get(self, id=None):
        """ Retrieve all payments or a specific payment by id """
        if id:
            payment = Payment.query.get(id)
            if not payment:
                abort(404, message="Payment not found")
            return PaymentSchema().dump(payment)
        else:
            payments = Payment.query.all()
            return [PaymentSchema().dump(payment) for payment in payments]

    def put(self):
        """ Handle Paystack webhooks """
        payload = request.get_json()
        if payload['event'] == 'charge.success':
            data = payload['data']
            payment_id = data['reference']
            amount = data['amount']
            payment_status = data['status']

            payment = Payment.query.filter_by(payment_id=payment_id).first()
            if payment:
                payment.amount = amount
                payment.payment_status = payment_status
                db.session.commit()
            else:
                abort(404, message="Payment not found")
        return jsonify({"status": "success"})
