from django.urls import path
from . import views

urlpatterns = [
    path('viewcars/', views.viewcars, name='viewcars'),
    path('book/<int:cid>/', views.book, name='book'),
    path('viewbookings/', views.viewbookings, name='viewbookings'),
    path('response/', views.response, name='response'),
    path('returncar/<int:id>/', views.returncar, name='returncar'),
    path('submitfeedback/', views.submitfeedback, name='submitfeedback'),
    path('submitcomplaint/', views.submitcomplaint, name='submitcomplaint'),
] 