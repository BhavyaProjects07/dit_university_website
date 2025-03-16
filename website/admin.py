from django.contrib import admin
from website.models import AdmissionForm,AdmissionInquiry,ContactMessage,Department,Program,Classroom,Subject,Attendance
# admin -- admin-bhavya
# pass -- ronaldo
# Register your models here.
admin.site.register(AdmissionForm)
admin.site.register(AdmissionInquiry)
admin.site.register(ContactMessage)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Attendance)
# admin.site.register(Programs_Details)





class SubjectAdmin(admin.ModelAdmin):
    
    search_fields = ("subject_name", "subject_code")  # Enable search functionality