from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime
from .models import Payment, Transaction
from services.models import Service


@login_required
def initiate_payment(request):
    """Initiate an M-Pesa payment for a service request."""
    service_id = request.GET.get('service')
    service = None
    if service_id:
        service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '')
        amount = request.POST.get('amount', '0')
        
        try:
            amount = float(amount)
        except ValueError:
            amount = service.price if service else 100.00

        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            service=service,
            amount=amount,
            phone_number=phone_number,
            status='pending'
        )

        # Simulate M-Pesa API call (in production, call actual M-Pesa API)
        checkout_request_id = str(uuid.uuid4()).replace('-', '')[:10].upper()
        payment.mpesa_checkout_request_id = checkout_request_id
        payment.save()

        return render(request, 'payments/payment_success.html', {
            'payment': payment,
            'checkout_request_id': checkout_request_id,
        })

    context = {'service': service}
    return render(request, 'payments/initiate_payment.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def mpesa_callback(request):
    """Receive M-Pesa payment callback (simulated for testing)."""
    try:
        data = json.loads(request.body)
        
        # Find the payment by checkout request ID
        checkout_id = data.get('CheckoutRequestID')
        payment = get_object_or_404(Payment, mpesa_checkout_request_id=checkout_id)

        result_code = data.get('ResultCode', '1')
        result_desc = data.get('ResultDesc', 'Unknown')

        # Create transaction record
        transaction = Transaction.objects.create(
            payment=payment,
            result_code=result_code,
            result_desc=result_desc,
            callback_raw=data
        )

        if result_code == '0':
            payment.status = 'completed'
            transaction.mpesa_receipt_number = data.get('MpesaReceiptNumber')
            transaction.mpesa_phone_number = data.get('PhoneNumber')
        else:
            payment.status = 'failed'

        payment.save()
        transaction.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def simulate_payment_callback(request, checkout_request_id):
    """Simulate an M-Pesa payment callback for testing."""
    payment = get_object_or_404(Payment, mpesa_checkout_request_id=checkout_request_id, user=request.user)

    # Simulate successful payment
    data = {
        'CheckoutRequestID': checkout_request_id,
        'ResultCode': '0',
        'ResultDesc': 'The service request was initiated successfully.',
        'MpesaReceiptNumber': 'QQQ4N1ZZGL',
        'PhoneNumber': payment.phone_number
    }

    transaction = Transaction.objects.create(
        payment=payment,
        result_code='0',
        result_desc='Success',
        callback_raw=data,
        mpesa_receipt_number='QQQ4N1ZZGL',
        mpesa_phone_number=payment.phone_number
    )

    payment.status = 'completed'
    payment.save()

    return redirect('payments:status', pk=payment.id)


@login_required
def payment_status(request, pk):
    """View payment status."""
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    transaction = None
    if hasattr(payment, 'transaction'):
        transaction = payment.transaction

    return render(request, 'payments/payment_status.html', {
        'payment': payment,
        'transaction': transaction,
    })
