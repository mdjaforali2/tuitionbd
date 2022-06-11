from dataclasses import field
from re import A
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(
        attrs={'type':'date'}
    ))
    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ('user','images')
    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        self.fields['phone'].initial = '+880'
        self.fields['role'].label = 'My role here:'

from .models import TuitionProfile

class TuitionProfileForm(forms.ModelForm):
    class Meta:
        model = TuitionProfile
        # fields = '__all__'
        exclude = ('user','id')
        widgets = {
            'class_in':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
            'subject':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
        }        
        labels = {
            'salary' : 'Salary Expectation'
        }