    
from rest_framework import serializers
from website.models import Department,Program,Classroom,Subject,Attendance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'



class ProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'  # Includes all fields in the model


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


        from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'classroom', 'student', 'marks']




class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'subject', 'date', 'is_present']
        read_only_fields = ['id', 'date']  # Auto-generated fields