from django.contrib import admin
from .models import User, Payment, Update, Subscription
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'date_joined', 'expire_date', 'subscribe_plan', 'verified') 
    list_filter = ('expire_date',) 
    empty_value_display = '-пусто-'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_status', 'payment_amount', 'expire_date', 'subscribe_plan', 'payment_time') 
    list_filter = ('payment_time',) 
    empty_value_display = '-пусто-'

class UpdateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'version', 'url', 'description', 'important', 'creation_date') 
    empty_value_display = '-пусто-'

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'adverts', 'products', 'renew') 
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin) 
admin.site.register(Payment, PaymentAdmin) 
admin.site.register(Update, UpdateAdmin) 
admin.site.register(Subscription, SubscriptionAdmin) 

