from django.shortcuts import render,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from website.forms import AdmissionFormModelForm , AdmissionInquiryForm , ContactMessageForm
from rest_framework.response import Response
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
# Views


from website.models import Department,Program,Classroom,Subject, Attendance,Profile
from website.serializers import DepartmentSerializer , ProgramDetailSerializer , ClassroomSerializer , SubjectSerializer , AttendanceSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # /departments/id/programs_details
    @action(detail=True, methods=['get'], url_path='programs_details')
    def department_programs(self, request, pk=None):
        department = self.get_object()
        programs = Program.objects.filter(department=department)
        serializer = ProgramDetailSerializer(programs, many=True)
        return Response(serializer.data)
    
    # /departments/id/programs_details/id
    @action(detail=True, methods=['get'], url_path='programs_details/(?P<program_id>\d+)')
    def program_details(self, request, pk=None, program_id=None):
        department = get_object_or_404(Department, id=pk)
        program = get_object_or_404(Program, id=program_id, department=department)

        # Render template correctly
        return render(request, 'sub_templates/programs_details.html', {'program': program})


class ProgramDetailViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramDetailSerializer


#send programs to the programs.html related to the department ID
def programs(request):
    programs = Program.objects.filter(department__id__in=[1, 2, 3]).select_related('department')
    return render(request, 'programs.html', {'programs': programs})


def home(request):
    return render(request, 'home.html')

def academics(request):
    if request.method == "POST":
        form = AdmissionInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            print(f"✅ Saved to DB: {inquiry.first_name}, {inquiry.last_name}, {inquiry.email}, {inquiry.phone}, {inquiry.program_of_interest}")

            messages.success(
                request, 
                "Thank you for showing your interest at DIT University. Our admission counselor will reach out to you as soon as possible."
            )
            return redirect("/ACADEMICS")  # Redirect to academics page
        else:
            print("❌ Form errors:", form.errors.as_json())  # Debugging
    else:
        form = AdmissionInquiryForm()

    return render(request, "academics.html", {"form": form})




def campus(request):
    return render(request, 'campus.html')


def research1(request):
    return render(request,'sub_templates/research1.html')

def research2(request):
    return render(request,'sub_templates/research2.html')

def research3(request):
    return render(request,'sub_templates/research3.html')




def admissions(request):
    if request.method == "POST":
        form = AdmissionInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            print(f"✅ Saved to DB: {inquiry.first_name}, {inquiry.last_name}, {inquiry.email}, {inquiry.phone}, {inquiry.program_of_interest}")

            messages.success(
                request, 
                "Thank you for showing your interest at DIT University. Our admission counselor will reach out to you as soon as possible."
            )
            return redirect("/ADMISSIONS")  # Redirect to admissions page
        else:
            print("❌ Form errors:", form.errors.as_json())  # Debugging
    else:
        form = AdmissionInquiryForm()

    return render(request, "admissions.html", {"form": form})




def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        print("🔍 Raw POST Data:", request.POST)  # Debugging Step

        if form.is_valid():
            contact_message = form.save(commit=False)  # Save but don’t commit yet

            print(f"✅ Saved to DB: {contact_message.first_name}, {contact_message.last_name}, {contact_message.email}, {contact_message.phone}, {contact_message.inquiry_type}")
            
            contact_message.save()  # Now save it to the database
            
            messages.success(request, "Thank you for your message. We will get back to you soon.")
            return redirect('/CONTACT')  # Redirect to prevent resubmission
        
        else:
            print("❌ Form Errors:", form.errors.as_data())  # Print validation errors
    
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})







def admission_form(request):
    if request.method == "POST":
        form = AdmissionFormModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Dear {request.POST.get('first_name')}, your application form has been submitted.")
            return redirect('/form')  # Redirect after success
        else:
            messages.error(request, "There was an error in the form submission. Please check the details.")

    else:
        form = AdmissionFormModelForm()
        

    return render(request, "adm_form.html", {"form": form})




# Generate a 4-digit OTP

from django.shortcuts import redirect

def auth_view(request):
    next_url = request.GET.get('next', '/')  # Default redirect to dashboard
    
    if request.method == "POST":
        action = request.POST.get("action")

        # ✅ SIGNUP - Request OTP
        if action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "message": "Email already exists! Please log in."})

            otp = str(random.randint(1000, 9999))

            # Store in session
            request.session["otp_email"] = email
            request.session["otp_username"] = username  
            request.session["otp_password"] = password  
            request.session["otp_code"] = otp
            request.session['next_url'] = next_url  # Store intended destination in session
            request.session.modified = True  

            # Send OTP
            send_mail(
                "Your OTP Code",
                f"Your OTP for account verification is: {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": f"OTP sent to {email}"})

        # ✅ VERIFY OTP - Create user & log in
        elif action == "verify_otp":
            email = request.session.get("otp_email")
            username = request.session.get("otp_username")  
            password = request.session.get("otp_password")  
            otp_code = request.session.get("otp_code")  

            entered_otp = request.POST.get("otp")

            if not email or not username or not password or not otp_code:
                return JsonResponse({"success": False, "message": "Session expired. Please try signing up again."})

            if entered_otp != otp_code:
                return JsonResponse({"success": False, "message": "Invalid OTP! Please try again."})

            # Create and log in the user
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            
            return redirect(request.session.get('next_url', '/'))  # Redirect to intended URL
        
        # ✅ LOGIN HANDLING - Authenticate user
        elif action == "signin":
            email = request.POST.get("email")
            password = request.POST.get("password")
            print(f"User password is : {password}")

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    send_mail(
                        "Dear User, You have just logged into Bhavya's DIT University",
                        "Hello, this is a notification that you have successfully logged in.",
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    return redirect(next_url)  # Redirect to intended URL
                else:
                    messages.error(request, "Invalid email or password!")
            except User.DoesNotExist:
                messages.error(request, "Email not registered! Please sign up.")

    return render(request, "auth.html")


# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect("auth")




from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        subjects = Subject.objects.filter(student=request.user)

        for subject in subjects:
            subject.attendance = Attendance.calculate_attendance_percentage(request.user, subject)

        # Include profile data in the context
        profile = Profile.objects.get(user=request.user)  # Assuming a one-to-one relationship
        
        return render(request, 'sub_templates/dash.html', {
            'subjects': subjects,
            'profile': profile  # Add profile here
        })
    else:
        return redirect('/Log in')
    
    
@login_required
def upload_profile_picture(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()

    return redirect('dashboard')  # Redirect back to the dashboard after upload




# dashboad model view sets

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer




class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filter subjects for the logged-in student
    def get_queryset(self):
        return Subject.objects.filter(student=self.request.user)
    

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure only authenticated users can access their own attendance
        return Attendance.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        # Ensure attendance is linked to the logged-in user
        serializer.save(student=self.request.user)


import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Configure Gemini API
genai.configure(api_key="AIzaSyBFioTK7-BkdaXo8Fz4EOdRiBXTzobTJ-w")
model = genai.GenerativeModel('gemini-2.0-flash')

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message.strip():
                return JsonResponse({'response': "Please enter a valid question."})

            # Generate AI response
            response = model.generate_content(user_message)
            bot_response = response.text.strip() if response.text else "I'm not sure how to respond."

            return JsonResponse({'response': bot_response})

        except Exception as e:
            return JsonResponse({'response': "Sorry, something went wrong. Please try again."})
