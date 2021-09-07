from django import forms
from django.db.models import fields
from .models import UserAccount,UserProfile

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id':'username',
        'onkeyup' : 'checkUsername()',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id':'e_mail',
        'onkeyup' : 'checkEmail()',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter a password',
        'id'         : 'pass1',
        'onkeyup'    : 'passCheck()',
    }))
    c_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
        'id'         : 'pass2',
        'onkeyup'    : 'passChecker()',
    }))
    class Meta:
        model = UserAccount
        fields = ['first_name','last_name','username','email','phone','password']
    
    def __init__(self,*args, **kwargs):
        super(UserRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your Last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Your Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserRegistrationForm,self).clean()
        password     = cleaned_data.get('password')
        c_password   = cleaned_data.get('c_password')

        if password!=c_password:
            raise forms.ValidationError(
                "Password does not match !"
            )


class UserAccForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(UserAccForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    class Meta:
        model = UserAccount 
        fields = ('first_name','last_name','username','phone')

class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False,error_messages={'invalid':('Image Files Only')},
    widget=forms.FileInput)
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    class Meta:
        model = UserProfile 
        fields = ('address_line1','address_line2','profile_pic','region','country')
