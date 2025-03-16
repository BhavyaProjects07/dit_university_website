from django.contrib import admin
from django.urls import path,include
from website import views
from website.views import auth_view, logout_view 
from rest_framework.routers import DefaultRouter
from website.views import DepartmentViewSet,ProgramDetailViewSet,ClassroomViewSet,SubjectViewSet,AttendanceViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'programs_details', ProgramDetailViewSet, basename='program')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path("",views.home,name='website'),
    path('', include(router.urls)),
    path("Log in/", auth_view, name="auth"), 
    path('dashboard/', views.dashboard, name='dashboard'), # Single Auth Page (Login & Signup)
    path("logout/", logout_view, name="logout"),  # Logout Route
    path("ACADEMICS/",views.academics,name='academics'),
    path("PROGRAMS/",views.programs,name="programs"),
    path('CAMPUS LIFE/',views.campus,name="campus"),
    path('ADMISSIONS/',views.admissions,name='admissions'),
    path("form/",views.admission_form,name="admission_form"),
    path("CONTACT/",views.contact,name="contact"),
    path("Research1/",views.research1,name="research1"),
    path("Research2/",views.research2,name="research2"),
    path("Research3/",views.research3,name="research3"),
    path('departments/<int:pk>/programs_details/<int:program_id>/', 
     DepartmentViewSet.as_view({'get': 'program_details'}), 
     name='details'),

    path('chatbot/', views.chatbot, name='chatbot'),



]