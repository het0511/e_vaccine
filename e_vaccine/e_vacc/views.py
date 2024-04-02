from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.db.models import F
# Create your views here.

def home(request):
    return render(request,'index.html');

def hospital_login(request):
    login_error = False
    rights_error = False
    if request.method == 'POST':
        username = request.POST.get('hospitalUsername')
        password = request.POST.get('hospitalPassword')
        try:
            user = doctor_user.objects.get(username=username, password=password) 
        except doctor_user.DoesNotExist:
            user = None

        if user is not None:
            if user.status == 'pending':
                rights_error = True
                return render(request, 'hospital_login.html', {'rights_error': rights_error})
            else:
                request.session['username'] = user.username
                request.session['name'] = user.doctor_name
                return redirect('/hospital_dashboard')
        else:
            login_error = True
    return render(request,'hospital_login.html',{'show_error': login_error});

def parent_login(request):
    login_error = False
    
    if request.method == 'POST':
        username = request.POST.get('parentUsername')
        password = request.POST.get('parentPassword')
        
        try:
            user = parent_user.objects.get(username=username, password=password) 
        except parent_user.DoesNotExist:
            user = None

        if user is not None:
            request.session['username'] = user.username
            request.session['name'] = user.fullname
            # Redirect to the parent dashboard or any appropriate page upon successful login
            return redirect('appointment')  # Replace 'parent_dashboard' with the appropriate URL name
        else:
            login_error = True
    
    return render(request, 'parent_login.html', {'show_error': login_error})

def new_doctor(request):
    pass_error = False
    no_registered_hospital = False
    username_exists_error = False
    email_exists_error = False
    contact_exists_error = False

    if request.method== 'POST':
        hospital_name = request.POST.get('hospitalName')
        staff_name = request.POST.get('staffName')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        if password!= confirm_password:
            pass_error = True
            return render(request,'new_doctor.html',{'pass1_error': pass_error});
        try:
            hospital_instance = hospital_user.objects.get(hospital_name=hospital_name)
        except hospital_user.DoesNotExist:
            no_registered_hospital = True
            return render(request,'new_doctor.html',{'no_hospital': no_registered_hospital})

        if doctor_user.objects.filter(username=username).exists():
            username_exists_error = True
            return render(request, 'new_doctor.html', {'username_exists_error': username_exists_error})

        if doctor_user.objects.filter(email=email).exists():
            email_exists_error = True
            return render(request, 'new_doctor.html', {'email_exists_error': email_exists_error})

        if doctor_user.objects.filter(contact_no=contact_no).exists():
            contact_exists_error = True
            return render(request, 'new_doctor.html', {'contact_exists_error': contact_exists_error})

        doctor_instance = doctor_user.objects.create(
            doctor_name=staff_name,
            hospital_id=hospital_instance,
            email=email,
            contact_no=contact_no,
            username=username,
            password=password,
            status='pending'
        )
        return redirect('/hospital_login')
    return render(request, 'new_doctor.html')

def new_parent(request):
    pass_error = False
    username_exists_error = False
    email_exists_error = False
    contact_exists_error = False

    if request.method== 'POST':
        fullname = request.POST.get('fullName')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        if password!= confirm_password:
            pass_error = True
            return render(request,'new_parent.html',{'pass1_error': pass_error});

        if parent_user.objects.filter(username=username).exists():
            username_exists_error = True
            return render(request, 'new_parent.html', {'username_exists_error': username_exists_error})

        if parent_user.objects.filter(email=email).exists():
            email_exists_error = True
            return render(request, 'new_parent.html', {'email_exists_error': email_exists_error})

        if parent_user.objects.filter(contact_no=contact_no).exists():
            contact_exists_error = True
            return render(request, 'new_parent.html', {'contact_exists_error': contact_exists_error})

        parent_instance = parent_user.objects.create(
            fullname=fullname,
            email=email,
            contact_no=contact_no,
            username=username,
            password=password
        )
        return redirect('/parent_login')
    return render(request, 'new_parent.html')

def manage_child_data(request):
    if 'username' in request.session:
        username = request.session['username']
        try:
            parent_user_obj = parent_user.objects.get(username=username)
            try:
                child_data_obj = child_data.objects.get(parent_id=parent_user_obj)
                form_data = {
                    'name': child_data_obj.name,
                    'dob': child_data_obj.date_of_birth.strftime('%Y-%m-%d'),
                    'age': child_data_obj.age,
                    'address': child_data_obj.address
                }
            except child_data.DoesNotExist:
                form_data = None

            if request.method == 'POST':
                name = request.POST.get('name')
                dob = request.POST.get('dob')
                age = request.POST.get('age')
                address = request.POST.get('address')

                if form_data:
                    child_data_obj.name = name
                    child_data_obj.date_of_birth = dob
                    child_data_obj.age = age
                    child_data_obj.address = address
                else:
                    child_data_obj = child_data(
                        parent_id=parent_user_obj,
                        name=name,
                        date_of_birth=dob,
                        age=age,
                        address=address
                    )
                
                child_data_obj.save()
                return redirect('/appointment')

            return render(request, 'manage_child_data.html', {'form_data': form_data})
        except parent_user.DoesNotExist:
            return redirect('/parent_login')
    else:
        return redirect('/parent_login')

from django.db.models import F, CharField, Value, Case, When

def hospital_dashboard(request):
    if not request.session.get('username'):
        return redirect('/hospital_login')
    
    # Get the username from the session
    username = request.session.get('username')

    try:
        # Retrieve the doctor_user object based on the username
        doctor_user_obj = doctor_user.objects.get(username=username)
        
        # Retrieve the associated hospital_user object
        hospital_user_obj = doctor_user_obj.hospital_id
        
        # Get the hospital name from the hospital_user object
        hospital_name = hospital_user_obj.hospital_name

        # Retrieve appointments specific to the hospital
        appointments = appointment.objects.filter(hospital_name=hospital_name)

        # Loop through each appointment and annotate with the administered doctor's name
        for app in appointments:
            try:
                administered_instance = administered.objects.get(appointment_id=app.id)
                app.administered_by = administered_instance.doctor_id.doctor_name
            except administered.DoesNotExist:
                app.administered_by = 'N/A'

        # Pass appointments to the template for rendering
        return render(request, 'hospital_dashboard.html', {'appointments': appointments})
    
    except doctor_user.DoesNotExist:
        # Handle the case where the doctor_user object doesn't exist
        return redirect('/hospital_login')

from django.db.models import OuterRef, Subquery

def appointment1(request):
    if not request.session.get('username'):
        return redirect('/parent_login')
    
    # Fetch appointments associated with the logged-in user
    username = request.session['username']
    try:
        parent_user_obj = parent_user.objects.get(username=username)
        # Annotate appointments with doctor's name and contact number
        appointments = appointment.objects.filter(parent_id=parent_user_obj).annotate(
            approved_by=Subquery(
                administered.objects.filter(appointment_id=OuterRef('pk')).values('doctor_id__doctor_name')[:1]
            ),
            contact_number=Subquery(
                administered.objects.filter(appointment_id=OuterRef('pk')).values('doctor_id__contact_no')[:1]
            )
        )
    except parent_user.DoesNotExist:
        appointments = []

    return render(request, 'appointment.html', {'appointments': appointments})

def hospital_logout(request):
    # Clear all cookies and session data
    request.session.flush()
    return redirect('/hospital_login')

def parent_logout(request):
    # Clear all cookies and session data
    request.session.flush()
    return redirect('/parent_login')

def book_appointment(request):
    if not request.session.get('username'):
        return redirect('/parent_login')

    parent_username = request.session.get('username')

    try:
        parent_user_obj = parent_user.objects.get(username=parent_username)
        child_obj = child_data.objects.get(parent_id=parent_user_obj)
    except (parent_user.DoesNotExist, child_data.DoesNotExist):  
        # If parent user or child data doesn't exist, redirect to manage_child_data
        return redirect('/manage_child_data')

    if request.method == 'POST':
        vaccine_type = request.POST.get('vaccineType')
        hospital_name = request.POST.get('hospitalName')

        try:
            # Get the hospital and vaccine objects based on the selected names
            hospital_obj = hospital_user.objects.get(hospital_name=hospital_name)
            vaccine_obj = vaccine.objects.get(vaccine_name=vaccine_type)

            # Create a new appointment object
            new_appointment = appointment(
                hospital_name=hospital_name,
                child_name=child_obj.name,
                vaccine_id=vaccine_obj,
                date=timezone.now().date(),
                time=timezone.now().time(),
                status='pending',
                parent_id=parent_user_obj
            )
            new_appointment.save()  # Save the new appointment object

            # Redirect to the parent dashboard after booking appointment
            return redirect('/appointment')

        except (hospital_user.DoesNotExist, vaccine.DoesNotExist):
            # Handle errors when hospital or vaccine objects are not found
            pass

    # Fetch hospital and vaccine options from the database
    hospitals = hospital_user.objects.all()
    vaccines = vaccine.objects.all()

    return render(request, 'book_appointment.html', {'hospitals': hospitals, 'vaccines': vaccines, 'child_name': child_obj.name})

def view_child_data(request, appointment_id):
    try:
        # Retrieve the appointment instance based on the appointment ID
        appointment_instance = appointment.objects.get(id=appointment_id)
        
        # Fetch the parent ID from the appointment
        parent_id = appointment_instance.parent_id
        
        # Retrieve the child data associated with the parent ID
        child_data_obj = child_data.objects.get(parent_id=parent_id)
        
        # Render the child data view template with the child's data
        return render(request, 'child_data_view.html', {'child': child_data_obj})
    
    except (appointment.DoesNotExist, child_data.DoesNotExist):
        # Handle error when appointment or child data doesn't exist
        return redirect('/hospital_dashboard')

def doctor_edit_appointment(request, appointment_id):
    try:
        # Retrieve the appointment instance based on the appointment ID
        appointment_instance = appointment.objects.get(id=appointment_id)
    except appointment.DoesNotExist:
        # Handle the case where the appointment ID doesn't exist
        return HttpResponse("Appointment not found", status=404)

    if request.method == 'POST':
        # Extract the updated information from the form
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')

        # Update the appointment instance with the new information
        appointment_instance.date = date
        appointment_instance.time = time
        appointment_instance.status = status
        appointment_instance.save()

        # Get the doctor's username from the session
        doctor_username = request.session.get('username')

        try:
            # Retrieve the corresponding doctor_user instance
            doctor_user_instance = doctor_user.objects.get(username=doctor_username)
        except doctor_user.DoesNotExist:
            # Handle the case where the doctor user doesn't exist
            return HttpResponse("Doctor user not found", status=404)

        # Create or update the administered instance for the appointment
        administered_instance, created = administered.objects.get_or_create(
            appointment_id=appointment_instance,
            defaults={'doctor_id': doctor_user_instance}
        )

        # If the administered instance already exists, update the doctor_id
        if not created:
            administered_instance.doctor_id = doctor_user_instance
            administered_instance.save()

        # Redirect to the hospital dashboard after editing the appointment
        return redirect('/hospital_dashboard')

    # If the request method is GET, render the edit appointment template
    return render(request, 'doctor_edit_appointment.html', {'appointment': appointment_instance})

from django.http import HttpResponseBadRequest

def delete_appointment(request, appointment_id):
    try:
        # Retrieve the appointment instance based on the appointment ID
        appointment_instance = appointment.objects.get(id=appointment_id)
        
        # Check if the administered instance exists for the appointment
        try:
            administered_instance = administered.objects.get(appointment_id=appointment_instance)
            # If administered instance exists, delete it
            administered_instance.delete()
        except administered.DoesNotExist:
            # Administered instance does not exist, proceed to delete appointment
            pass
        
        # Delete the appointment instance
        appointment_instance.delete()
        
        # Redirect to hospital dashboard after deletion
        return redirect('/hospital_dashboard')

    except appointment.DoesNotExist:
        # Handle error when appointment doesn't exist
        return HttpResponseBadRequest("Appointment not found", status=400)

def edit_appointment(request, appointment_id):
    try:
        # Retrieve the appointment instance based on the appointment ID
        appointment_instance = appointment.objects.get(id=appointment_id)
        
        if request.method == 'POST':
            # Extract the updated information from the form
            vaccine_id = request.POST.get('vaccineType')
            hospital_id = request.POST.get('hospitalName')
            
            # Update the appointment instance with the new information
            appointment_instance.vaccine_id_id = vaccine_id
            appointment_instance.hospital_name_id = hospital_id
            appointment_instance.status = 'pending'  # Set status to "pending"
            
            # Save the changes to the appointment instance
            appointment_instance.save()
            
            # Redirect to the appropriate dashboard after editing the appointment
            if request.session.get('username'):
                return redirect('/appointment')
            else:
                return redirect('/hospital_dashboard')
        
        # Fetch all vaccine and hospital options from the database
        vaccines = vaccine.objects.all()
        hospitals = hospital_user.objects.all()
        
        # Render the edit appointment template with the appointment details and options
        return render(request, 'edit_appointment.html', {'appointment': appointment_instance, 'vaccines': vaccines, 'hospitals': hospitals})
    
    except appointment.DoesNotExist:
        # Handle error when appointment doesn't exist
        return HttpResponseBadRequest("Appointment not found", status=400)
