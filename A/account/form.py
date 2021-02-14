from django import forms
from .models import Profile

messages={
    'required':'پرکردن فیلد زیر اجباری است'
}

class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=50,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(max_length=20,widget=forms.
            PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

class RegisterForm(forms.Form):
    username=forms.CharField(error_messages=messages,max_length=50,widget=forms.TextInput
    (attrs={'class':'form-control','placeholder':'username'}))
    Email=forms.EmailField(max_length=50,widget=forms.EmailInput
    (attrs={'class':'form-control','placeholder':'Email'}))
    password=forms.CharField(max_length=20,widget=forms.PasswordInput
    (attrs={'class':'form-control','placeholder':'password'}))


class EditProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'})) 
    class Meta():
        model=Profile
        fields=('bio','age','phone')
       
class PhoneLoginForm(forms.Form):
    phone=forms.IntegerField(widget=forms.NumberInput)


    def clean_phone(self):
        phone=Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.validationError("dose not phone")
        return self.cleaned_data['phone']

class VerifycodeForm(forms.Form):
    code=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',}))