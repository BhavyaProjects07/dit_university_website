from django.db import models
from django.contrib.auth.models import User



#adm form model
# Choices for dropdowns
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

PROGRAM_CHOICES = [
    ('btech', 'B.Tech'),
    ('mtech', 'M.Tech'),
    ('bba', 'BBA'),
    ('mba', 'MBA'),
    ('bca', 'BCA'),
    ('mca', 'MCA'),
    ('bpharm', 'B.Pharm'),
    ('mpharm', 'M.Pharm'),
]

class AdmissionForm(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Contact Information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Academic Information
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    specialization = models.CharField(max_length=100)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # Document Uploads
    photo = models.ImageField(upload_to='uploads/photos/')
    signature = models.ImageField(upload_to='uploads/signatures/')
    tenth_marksheet = models.FileField(upload_to='uploads/marksheets/')
    twelfth_marksheet = models.FileField(upload_to='uploads/marksheets/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program}"




# model for Inquiry form 

class AdmissionInquiry(models.Model):
    PROGRAM_CHOICES = [
        ('btech', 'B.Tech'),
        ('mtech', 'M.Tech'),
        ('bba', 'BBA'),
        ('mba', 'MBA'),
        ('bsc', 'B.Sc'),
        ('phd', 'Ph.D'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    program_of_interest = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_of_interest}"
    





# Model for contact
class ContactMessage(models.Model):
    INQUIRY_CHOICES = [
        ('admission', 'Admission Inquiry'),
        ('program', 'Program Information'),
        ('campus', 'Campus Facilities'),
        ('scholarship', 'Scholarships & Financial Aid'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES)
    message = models.TextField()
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.inquiry_type}"
    




class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, default='Unknown')

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



# model for storing the programs detail in DB

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    duration = models.CharField(max_length=100)  # e.g., "4 Years", "3 Years"
    level = models.CharField(max_length=100)     # e.g., "Undergraduate", "Postgraduate"
    description = models.TextField(blank=True, null=True)
    syllabus = models.TextField(blank=True, null=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='programs'
    )
    def __str__(self):
        return self.name




# API models for student dashboard


class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.CharField(max_length=100, unique=True , default='unknown')

    def __str__(self):
        return self.classroom
    


class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.student.username}"
    

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.username} - {self.subject.name} - {status}"
    
    @staticmethod
    def calculate_attendance_percentage(student, subject):
        total_classes = Attendance.objects.filter(student=student, subject=subject).count()
        attended_classes = Attendance.objects.filter(student=student, subject=subject, is_present=True).count()
        
        if total_classes == 0:
            return 0
        return round((attended_classes / total_classes) * 100, 2)