# forms.py
from django import forms
from .models import User 
from django.contrib.auth.models import User



class SignupForm(forms.ModelForm):
    
        cpassword = forms.CharField(widget=forms.PasswordInput)
        class Meta:
            model = User  # Link the form to the User model
            fields = ['username', 'email', 'password', 'cpassword']  # Define the fields that the form will use


        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            cpassword = cleaned_data.get('cpassword')

            # Check if passwords match
            if password and cpassword and password != cpassword:
                raise forms.ValidationError("Passwords do not match.")
            
            return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

        


        
