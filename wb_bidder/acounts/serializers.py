from rest_framework import serializers
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'expire_date')
        write_only_fields = ('password',)

class ExpireSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('expire_date', 'subscribe_plan', 'verified', 'email', 'username')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('payment_id', 'payment_amount', 'expire_date', 'subscribe_plan') 

