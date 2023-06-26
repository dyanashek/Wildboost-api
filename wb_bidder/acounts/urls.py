from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'acounts'

urlpatterns = [
    path('token-auth/', obtain_auth_token),
    path('signup/', views.signup_api, name = 'signup_api'),
    path('subscription/', views.subscription_api, name = 'subscription_api'),
    path('subscription/change/', views.subscription_change_api, name = 'subscription_change_api'),
    path('change-password/', views.change_password_api, name = 'change_password_api'),
    path('payment-status/', views.payment_api, name = 'payment_api'),
    path('subscriptions-info/', views.subscriptions_info_api, name = 'subscriptions_info_api'),
    path('update/', views.update_api, name = 'update_api'),
]