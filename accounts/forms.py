from django import forms
from django.db.models import fields
from .models import UserAccount

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
        'onkeyup'    : 'passChecker()',
    }))
    c_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
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
        