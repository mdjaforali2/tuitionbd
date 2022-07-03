from __future__ import division
from dataclasses import field
from logging import PlaceHolder
from re import A
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Division, District, Upazilla, Qualification
from django.urls import reverse_lazy

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
        exclude = ('user', 'biodata', 'union', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blood_group'].label = 'Blood Group'
        self.fields['birth_date'].label = 'Birth Date'
        self.fields['role'].label = 'I am looking for a'
        self.fields['phone'].initial = '+880'



        # self.fields['union'].queryset = Union.objects.none()
        # if 'upazilla' in self.data:
        #     try:
        #         upazilla_id = int(self.data.get('upazilla'))
        #         self.fields['union'].queryset = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass
        # elif self.instance.pk:
        #     self.fields['union'].queryset = self.instance.upazilla.union_set.order_by('name')

            
from .models import TuitionProfile

class TuitionProfileForm(forms.ModelForm):
    class Meta:
        model = TuitionProfile
        # fields = '__all__'
        exclude = ('user','userprofile', 'id')
        widgets = {
            'class_in':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
            'subject':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
        }        
        labels = {
            'salary' : 'Salary Range',
            'status' : 'Availability',
            'more_options' : 'More Options I Offer: (Max choices 3)',
            'style': 'Style of Teaching:',
            'place' : 'Places I prefer to Teach: (Max choices 3)',
            'approach' : 'Approches I Follow: (Max choices 3)',
            'experience' : 'Years of Experience as a Tutor',
            'qualification' : 'Latest Qualification',
            'graduated_from' : 'Graduated From / Studying At:',
            'major_subject' : 'Major Subject: (If you do not have any major leave it as General)',
            'classes' : 'Classes I could Teach: (Max Choices 9)',
            'subjects' : 'Subjects I could Teach (Max Choices 10):',
            'current_status' : 'Educational Status:',
            'id_certificate' : 'Upload an image of your College/University ID or Certificate from where you Graduated:'
        }

    def __init__(self, *args, **kwargs):
        super(TuitionProfileForm,self).__init__(*args, **kwargs)
        self.fields['salary'].widget.attrs['placeholder'] = '2500 - 5000'
        self.fields['graduated_from'].widget.attrs['placeholder'] = 'Comilla Victoria Govt College'
        self.fields['major_subject'].widget.attrs['placeholder'] = 'English'
        self.fields['qualification'].queryset = Qualification.objects.all().order_by('-id')
        self.fields['division'].label = 'Enter Address, Division:'


        self.fields['upazilla'].label = 'City Corporation / Upazilla / Cantonment'
        self.fields['address'].label = 'House, Road No, Village/Mouza, Union / Ward No:'
        self.fields['address'].widget.attrs['placeholder'] = '87/Ka, Nazrul Avenue, 2nd Kandirpar, Ward-10'
       



        self.fields['division'].queryset = Division.objects.all().order_by('name')

        self.fields['district'].queryset = District.objects.none()
        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['district'].queryset = District.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.division.district

        self.fields['upazilla'].queryset = Upazilla.objects.none()
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['upazilla'].queryset = Upazilla.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['upazilla'].queryset = self.instance.district.upazilla