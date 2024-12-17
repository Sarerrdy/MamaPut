import smtplib
from email.mime.text import MIMEText
import logging
from os import getenv

logger = logging.getLogger(__name__)

# Production configuration for sender email and password
sender = getenv('MAIL_USERNAME')
password = getenv('MAIL_PASSWORD')


def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, [to_email], msg.as_string())
        server.quit()

        logger.info(f"Email sent to {to_email} successfully")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}")


def send_order_confirmation(email, order_id):
    subject = 'Order Confirmation'
    body = f""" Your order has been placed successfully with Order_Number: #{order_id}.\nWe will notify you once your order has shipped.\nIf you have any questions, feel free to contact us.\nYou can view your order history by signing into your profile page at: https://mamaputapp.onrender.com/profile\nBest regards, MamaPut"""
    send_email(email, subject, body)


def send_new_order_notification(order_id):
    subject = 'New Order Received'
    body = f"A new order has been received with order number: #{order_id}"
    send_email(sender, subject, body)


def send_order_status_update(email, order_id, status):
    subject = 'Order Status Update'
    body = f"Your order status has been updated to: {status}.\nOrder Number: #{order_id}\nBest regards, MamaPut"
    send_email(email, subject, body)
