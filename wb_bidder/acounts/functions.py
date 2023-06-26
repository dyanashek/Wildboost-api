import time
import datetime
import os
from yookassa import Configuration
from yookassa import Payment as Payment_kassa
from dotenv import load_dotenv

from .models import Payment

load_dotenv()

Configuration.account_id = str(os.environ["ACCOUNT_ID"])
Configuration.secret_key = str(os.environ["SECRET_KEY_PAYMENT"])

def payment_status_check():
    while True:
        payment_status = ''
        payments = Payment.objects.filter(payment_status=None)
            
        if payments:
            for payment in payments:
                try:
                    payment_obj = Payment_kassa.find_one(payment.payment_id)
                    payment_status = payment_obj.status
                except:
                    pass

                if payment_status == "succeeded":
                    payment.payment_status = True
                    payment.save()

                    payment.user.subscribe_plan = payment.subscribe_plan
                    payment.user.expire_date = payment.expire_date
                    payment.user.save()

                elif payment_status == "canceled":
                    payment.payment_status = False
                    payment.save()

        time.sleep(30)

