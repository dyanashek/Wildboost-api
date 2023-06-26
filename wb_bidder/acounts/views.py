from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.db.models import Max
from yookassa import Configuration, Payment
from dotenv import load_dotenv
import datetime
import time
import threading
import os

from .serializers import UserSerializer, ExpireSerializer, PaymentSerializer
from .models import User, Subscription, Update
from .functions import payment_status_check

load_dotenv()

Configuration.account_id = str(os.environ["ACCOUNT_ID"])
Configuration.secret_key = str(os.environ["SECRET_KEY_PAYMENT"])

threading.Thread(daemon=True, target=payment_status_check).start()

@api_view(['POST'])
def signup_api(request):
    serialized = UserSerializer(data=request.data)

    if serialized.is_valid():
        User.objects.create_user(
            email = serialized.data['email'],
            username = serialized.data['username'],
            password = serialized.data['password'],
            expire_date = datetime.date.today() + datetime.timedelta(days = 3),
            subscribe_plan = 1
        )

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_api(request):
    expire_date = request.user.expire_date
    subscribe_plan = request.user.subscribe_plan
    verified = request.user.verified
    email = request.user.email

    return Response(
        {"expire_date" : expire_date, "subscribe_plan" : subscribe_plan, "verified" : verified, "email" : email}, 
        status=status.HTTP_200_OK
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def subscription_change_api(request):
    if 'email' in request.data:
        users = User.objects.filter(email=request.data.get('email'))

        if users:
            return Response({"error" : "such e-mail already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    serialiezer = ExpireSerializer(request.user, data=request.data, partial=True)

    if serialiezer.is_valid():
        serialiezer.save()
        return Response(serialiezer.data, status=status.HTTP_200_OK)

    return Response(serialiezer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def change_password_api(request):

    if 'password' in request.data and 'email' in request.data:
        user = User.objects.get(email=request.data.get('email'))

        if user:
            user.set_password(request.data.get('password'))
            user.save()
            return Response({"success" : "password has been changed"}, status=status.HTTP_200_OK)

    return Response({"error" : "not enouth data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_api(request):
    payment_id = request.data.get('payment_id')
    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
        payment = serializer.save(user=request.user)

        while True:

            try:
                response = Payment.find_one(payment_id)
                payment_status = response.status
            except:
                return Response({"error" : "payment not found"}, status=status.HTTP_400_BAD_REQUEST)

            if payment_status == "succeeded":
                request.user.expire_date = serializer.validated_data.get('expire_date')
                request.user.subscribe_plan = serializer.validated_data.get('subscribe_plan')
                request.user.save()
                payment.payment_status = True
                payment.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif payment_status == "canceled":
                payment.payment_status = False
                payment.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                time.sleep(30)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import json
@api_view(['GET'])
def subscriptions_info_api(request):
    subscriptions = Subscription.objects.all()
    sub_js = json.dumps(list(subscriptions.values()), ensure_ascii=False)
    return Response(sub_js, status=status.HTTP_200_OK)   

@api_view(['GET'])
def update_api(request):
    last_update = Update.objects.get(pk=Update.objects.aggregate(pk=Max("pk"))['pk'])
    update_js = json.dumps(model_to_dict(last_update))
    return Response(update_js, status=status.HTTP_200_OK)     

