from django.contrib import admin
from .models import Payment, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment', 'mpesa_receipt_number', 'result_code', 'created_at')
    list_filter = ('result_code', 'created_at')
    search_fields = ('payment__id', 'mpesa_receipt_number')
    readonly_fields = ('created_at', 'callback_raw')
