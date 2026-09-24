from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from mainapp.models import Customer, Enquiry, Feedback, Complaint
from . models import CarInfo
from custapp.models import Booking
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminhome(request):
    try:
        if request.session['adminid']!=None:
            adminid=request.session['adminid']
            
            # Get booking statistics
            total_bookings = Booking.objects.count()
            active_bookings = Booking.objects.filter(status='active').count()
            
            # Calculate total revenue from completed bookings
            completed_bookings = Booking.objects.filter(status='completed')
            total_revenue = sum(booking.total_amount for booking in completed_bookings)
            
            # Get recent bookings (both active and completed)
            recent_bookings = Booking.objects.all().order_by('-bookingdate')[:5]
            
            context = {
                'adminid': adminid,
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'total_revenue': total_revenue,
                'recent_bookings': recent_bookings
            }
            
            return render(request,'adminhome.html', context)
    except KeyError:
        return redirect('mainapp:login')
def adminlogout(request):
    try:
        del request.session['adminid']        
    except KeyError:
        return redirect('mainapp:login')
    return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def customermgmt(request):
    try:
        if request.session['adminid']!=None:
            cust=Customer.objects.all()
            adminid=request.session['adminid']
            return render(request,'customermgmt.html',locals())
    except KeyError:
        return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def carmgmt(request):
    try:
        if request.session['adminid']!=None:
            adminid=request.session['adminid']
            carinfo=CarInfo.objects.all()
            if request.method=='POST':
                carname=request.POST['carname']
                carno=request.POST['carno']
                drivername=request.POST['drivername']
                carrent=request.POST['carrent']
                carpic=request.FILES['carpic']    
                availability='available'           
                ci=CarInfo(carname=carname,carno=carno,drivername=drivername,carrent=carrent,carpic=carpic,availability=availability)
                ci.save()
                messages.success(request,'Car is added')
            return render(request,'carmgmt.html',locals())
    except KeyError:
        return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def enquirymgmt(request):
    try:
        if request.session['adminid']!=None:
            enq=Enquiry.objects.all()
            adminid=request.session['adminid']
            return render(request,'enquirymgmt.html',locals())
    except KeyError:
        return redirect('mainapp:login')
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def bookedcars(request):
    try:
        if request.session['adminid']!=None:
            adminid=request.session['adminid']
            bookedcars = Booking.objects.all()
            return render(request,'bookedcars.html',locals())
    except KeyError:
        return redirect('mainapp:login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewfeedback(request):
    try:
        if request.session['adminid']!=None:
            adminid=request.session['adminid']
            feedbacks = Feedback.objects.all().order_by('-feedbackdate')
            return render(request,'viewfeedback.html',locals())
    except KeyError:
        return redirect('mainapp:login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewcomplaints(request):
    try:
        if request.session['adminid']!=None:
            adminid=request.session['adminid']
            complaints = Complaint.objects.all().order_by('-complaintdate')
            return render(request,'viewcomplaints.html',locals())
    except KeyError:
        return redirect('mainapp:login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def resolvecomplaint(request, cid):
    try:
        if request.session['adminid']!=None:
            complaint = Complaint.objects.get(cid=cid)
            complaint.status = 'resolved'
            complaint.save()
            messages.success(request, 'Complaint marked as resolved')
            return redirect('adminapp:viewcomplaints')
    except KeyError:
        return redirect('mainapp:login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deletecar(request, cid):
    try:
        if request.session['adminid']!=None:
            CarInfo.objects.filter(carid=cid).delete()
            messages.success(request, 'Car deleted successfully')
            return redirect('adminapp:carmgmt')
    except KeyError:
        return redirect('mainapp:login')