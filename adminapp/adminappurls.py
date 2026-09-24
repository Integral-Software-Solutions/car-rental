from django.urls import path 
from . import views

urlpatterns=[
    path('adminhome/',views.adminhome,name='adminhome'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('customermgmt/',views.customermgmt,name='customermgmt'),
    path('carmgmt/',views.carmgmt,name='carmgmt'),
    path('enquirymgmt/',views.enquirymgmt,name='enquirymgmt'),
    path('bookedcars',views.bookedcars,name='bookedcars'),
    path('viewfeedback/',views.viewfeedback,name='viewfeedback'),
    path('viewcomplaints/',views.viewcomplaints,name='viewcomplaints'),
    path('resolvecomplaint/<cid>',views.resolvecomplaint,name='resolvecomplaint'),
    path('deletecar/<cid>',views.deletecar,name='deletecar'),
]