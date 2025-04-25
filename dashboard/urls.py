from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('report/', views.report_upload, name='report_upload'),
    path('create-shipment/', views.create_shipment, name='create_shipment'),
    path('track-deliveries/', views.track_deliveries, name='track_deliveries'), 

]
