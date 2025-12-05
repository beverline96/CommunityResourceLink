from django.db import models
from django.contrib.auth.models import User
from services.models import Service
import uuid


class Payment(models.Model):
    """Represents a payment request for a service."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mpesa_request_id = models.CharField(max_length=255, null=True, blank=True)
    mpesa_checkout_request_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.amount} KES - {self.status}"

    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    """Records M-Pesa transaction details and callbacks."""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='transaction')
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    mpesa_transaction_date = models.DateTimeField(null=True, blank=True)
    mpesa_phone_number = models.CharField(max_length=15, null=True, blank=True)
    result_code = models.CharField(max_length=10, null=True, blank=True)
    result_desc = models.TextField(null=True, blank=True)
    callback_raw = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.payment.id}"

    class Meta:
        ordering = ['-created_at']
