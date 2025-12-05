from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate'),
    path('callback/', views.mpesa_callback, name='callback'),
    path('simulate/<str:checkout_request_id>/', views.simulate_payment_callback, name='simulate_callback'),
    path('status/<uuid:pk>/', views.payment_status, name='status'),
]
