from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('location/<int:location_id>/', views.view_slots, name='view_slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('history/', views.booking_history, name='booking_history'),
    path('explore/', views.explore_locations, name='explore_locations'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'), 
]
