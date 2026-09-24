from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from adminapp.models import CarInfo
from . models import Booking, Response
from mainapp.models import Customer, Feedback, Complaint
import datetime
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def custhome(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            custname=Customer.objects.get(contactno=custid).name
            return render(request,'custhome.html',locals())
    except KeyError:
        return redirect('mainapp:login')
def custlogout(request):
    try:
        del request.session['custid']        
    except KeyError:
        return redirect('mainapp:login')
    return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewcars(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            custname=Customer.objects.get(contactno=custid).name
            
            # Get all car IDs that are currently booked
            booked_car_ids = Booking.objects.filter(status='active').values_list('carid', flat=True)
            
            # Show only cars that are available AND not currently booked
            carinfo = CarInfo.objects.filter(
                availability='available'
            ).exclude(
                carid__in=booked_car_ids
            )
            
            return render(request,'viewcars.html',locals())
    except KeyError:
        return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def book(request,cid):
    try:
        if request.session['custid']!=None:
            if request.method == 'POST':
                car = CarInfo.objects.get(carid=cid)
                custid = request.session['custid']
                cust = Customer.objects.get(contactno=custid)
                
                # Get booking details
                distance = int(request.POST.get('distance'))
                days = int(request.POST.get('days'))
                pickup_date = request.POST.get('pickup_date')
                pickup_time = request.POST.get('pickup_time')
                
                # Calculate total amount
                base_amount = car.carrent * days
                distance_charge = 10 * distance
                total_amount = base_amount + distance_charge
                
                # Create booking record
                booking = Booking(
                    carid=cid,
                    bookedby=cust.name,
                    contactno=cust.contactno,
                    carname=car.carname,
                    carno=car.carno,
                    drivername=car.drivername,
                    carrent=car.carrent,
                    bookingdate=datetime.datetime.today(),
                    distance=distance,
                    days=days,
                    total_amount=total_amount
                )
                booking.save()
                
                # Update car availability
                car.availability = 'booked'
                car.save()
                
                messages.success(request, 'Car booked successfully!')
                return redirect('custapp:viewbookings')
            else:
                car = CarInfo.objects.get(carid=cid)
                return render(request, 'book.html', {'car': car})
    except KeyError:
        return redirect('mainapp:login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewbookings(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            custname=Customer.objects.get(contactno=custid).name
            # Get all bookings for this customer, ordered by booking date
            booking=Booking.objects.filter(contactno=custid).order_by('-bookingdate')
            return render(request,'viewbookings.html',locals())
    except KeyError:
        return redirect('mainapp:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def response(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            custname=Customer.objects.get(contactno=custid).name
            cust=Customer.objects.get(contactno=custid)
            if request.method=='POST':
                responsetype=request.POST['responsetype']
                subject=request.POST['subject']
                message=request.POST['message']
                posteddate=datetime.datetime.today()
                givenby=cust.name
                contactno=cust.contactno                
                sr=Response(givenby=givenby,contactno=contactno,responsetype=responsetype,subject=subject,message=message,posteddate=posteddate)
                sr.save()
                messages.success(request,'Response is submitted')
            return render(request,'response.html',locals())
    except KeyError:
        return redirect('mainapp:login')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def returncar(request,id):
    try:
        if request.session['custid']!=None:
            custid = request.session['custid']
            # Get the booking first to check if it exists and belongs to this customer
            booking = Booking.objects.get(carid=id, contactno=custid, status='active')
            if booking:
                # Update car availability
                car = CarInfo.objects.get(carid=id)
                car.availability = 'available'
                car.save()
                
                # Update booking status
                booking.status = 'completed'
                booking.save()
                
                messages.success(request, 'Car has been returned successfully')
                return redirect('custapp:viewbookings')
            else:
                messages.error(request, 'Invalid booking')
                return redirect('custapp:viewbookings')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found')
        return redirect('custapp:viewbookings')
    except CarInfo.DoesNotExist:
        messages.error(request, 'Car not found')
        return redirect('custapp:viewbookings')
    except KeyError:
        return redirect('mainapp:login')
    except Exception as e:
        messages.error(request, 'An error occurred while returning the car')
        return redirect('custapp:viewbookings')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def submitfeedback(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            customer=Customer.objects.get(contactno=custid)
            custname=customer.name
            if request.method=='POST':
                feedback=request.POST['feedback']
                feedbackdate=datetime.datetime.today()
                Feedback(name=customer.name, contactno=customer.contactno, 
                        emailaddress=customer.emailaddress, feedback=feedback,
                        feedbackdate=feedbackdate).save()
                messages.success(request,'Thank you for your feedback!')
                return redirect('custapp:custhome')
            return render(request,'submitfeedback.html',locals())
    except KeyError:
        return redirect('mainapp:login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def submitcomplaint(request):
    try:
        if request.session['custid']!=None:
            custid=request.session['custid']
            customer=Customer.objects.get(contactno=custid)
            custname=customer.name
            if request.method=='POST':
                complaint=request.POST['complaint']
                complaintdate=datetime.datetime.today()
                Complaint(name=customer.name, contactno=customer.contactno,
                         emailaddress=customer.emailaddress, complaint=complaint,
                         complaintdate=complaintdate).save()
                messages.success(request,'Your complaint has been submitted. We will look into it.')
                return redirect('custapp:custhome')
            return render(request,'submitcomplaint.html',locals())
    except KeyError:
        return redirect('mainapp:login')

def book_car(request, car_id):
    car = CarInfo.objects.get(carid=car_id)
    return render(request, 'book.html', {'car': car})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def calculate_payment(request, cid):
    try:
        if request.session['custid']!=None:
            if request.method == 'POST':
                car = CarInfo.objects.get(carid=cid)
                distance = int(request.POST.get('distance'))
                days = int(request.POST.get('days'))
                pickup_date = request.POST.get('pickup_date')
                pickup_time = request.POST.get('pickup_time')
                
                # Calculate base amount (daily rate × number of days)
                base_amount = car.carrent * days
                
                # Calculate distance charge (₹10 per km)
                distance_charge = 10 * distance
                
                # Calculate total amount
                total_amount = base_amount + distance_charge
                
                context = {
                    'car': car,
                    'distance': distance,
                    'days': days,
                    'pickup_date': pickup_date,
                    'pickup_time': pickup_time,
                    'base_amount': base_amount,
                    'distance_charge': distance_charge,
                    'total_amount': total_amount
                }
                
                return render(request, 'payment.html', context)
    except KeyError:
        return redirect('mainapp:login')
    return redirect('custapp:viewcars')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def process_payment(request, cid):
    try:
        if request.session['custid']!=None:
            if request.method == 'POST':
                car = CarInfo.objects.get(carid=cid)
                custid = request.session['custid']
                cust = Customer.objects.get(contactno=custid)
                
                # Get booking details from session or form
                distance = int(request.POST.get('distance'))
                days = int(request.POST.get('days'))
                pickup_date = request.POST.get('pickup_date')
                pickup_time = request.POST.get('pickup_time')
                
                # Calculate total amount
                base_amount = car.carrent * days
                distance_charge = 10 * distance
                total_amount = base_amount + distance_charge
                
                # Create booking record
                booking = Booking(
                    carid=cid,
                    bookedby=cust.name,
                    contactno=cust.contactno,
                    carname=car.carname,
                    carno=car.carno,
                    drivername=car.drivername,
                    carrent=car.carrent,
                    bookingdate=datetime.datetime.today(),
                    distance=distance,
                    days=days,
                    total_amount=total_amount
                )
                booking.save()
                
                # Update car availability
                car.availability = 'booked'
                car.save()
                
                messages.success(request, 'Payment successful! Your car is booked.')
                return redirect('custapp:viewbookings')
    except KeyError:
        return redirect('mainapp:login')
    return redirect('custapp:viewcars')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def payment(request, cid):
    try:
        if request.session['custid']!=None:
            car = CarInfo.objects.get(carid=cid)
            if request.method == 'POST':
                distance = int(request.POST.get('distance'))
                days = int(request.POST.get('days'))
                pickup_date = request.POST.get('pickup_date')
                pickup_time = request.POST.get('pickup_time')
                
                # Calculate base amount (daily rate × number of days)
                base_amount = car.carrent * days
                
                # Calculate distance charge (₹10 per km)
                distance_charge = 10 * distance
                
                # Calculate total amount
                total_amount = base_amount + distance_charge
                
                context = {
                    'car': car,
                    'distance': distance,
                    'days': days,
                    'pickup_date': pickup_date,
                    'pickup_time': pickup_time,
                    'base_amount': base_amount,
                    'distance_charge': distance_charge,
                    'total_amount': total_amount
                }
                
                return render(request, 'payment.html', context)
            return render(request, 'payment.html', {'car': car})
    except KeyError:
        return redirect('mainapp:login')