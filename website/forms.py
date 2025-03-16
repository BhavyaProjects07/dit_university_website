from django import forms
from website.models import AdmissionForm , AdmissionInquiry ,ContactMessage

class AdmissionFormModelForm(forms.ModelForm):
    class Meta:
        model = AdmissionForm
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'signature': forms.FileInput(attrs={'accept': 'image/*'}),
            'tenth_marksheet': forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
            'twelfth_marksheet': forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
        }



class AdmissionInquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionInquiry
        fields = ['first_name', 'last_name', 'email', 'phone', 'program_of_interest']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'program_of_interest': forms.Select(attrs={'class': 'form-control'}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'inquiry_type', 'message', 'consent']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
            'consent': forms.CheckboxInput(),
        }