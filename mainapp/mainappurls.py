from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('services/',views.services,name='services'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.login,name='login'),
    path('cars/economical/',views.economical_cars,name='economical_cars'),
    path('cars/suv/',views.suv_cars,name='suv_cars'),
    path('cars/luxury/',views.luxury_cars,name='luxury_cars'),
    path('cars/convertible/',views.convertible_cars,name='convertible_cars'),
]