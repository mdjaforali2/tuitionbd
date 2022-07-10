from cProfile import label
from dataclasses import field
from logging import PlaceHolder
from xml.etree.ElementInclude import include
from xml.etree.ElementTree import Comment
from django.core import validators
from django import forms
from .models import Contact, Post, Postfile, Filter
from .models import Comment as Com

# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=100, label="Your Name")
#     phone = forms.CharField(max_length=100, label="Your Phone")
#     content = forms.CharField(max_length=100, label="Your Details")

class ContactForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Your Name'}), label='Your Name')
    class Meta:
        model = Contact
        fields = '__all__'
        # widgets = {
        #     'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Name:'}),
        #     'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Phone:'}),
        #     'content':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Say something:', 'rows':5})
        # }
        labels = {
            'content':'Write your message:',
        }
        # help_texts = {
        #     'name':'Your Name',
        #     'phone':'Your Phone Number',
        #     'content':'Your Words',
        # }


    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['phone'].initial = '+8801'
        self.fields['content'].initial = 'Nothing to say.'

    def clean_phone(self):
        value = self.cleaned_data['phone']
        if len(value) > 14 or len(value) <14:
            self.add_error('phone', 'Enter 13 digits number inclue country code [+880]')
        else:
            return value





class ContactFormtwo(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__'
from .fields import ListTextWidget


class PostForm(forms.ModelForm):
    starting_from = forms.DateField(widget=forms.TextInput(
        attrs={'type':'date'}
    ))
    class Meta:
        model = Post
        exclude = ['user','email', 'available', 'category', 'id', 'slug', 'created_at', 'likes', 'views', 'applicants', 'candidate', 'tutor']
        widgets = {
            'class_in':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
            'subject':forms.CheckboxSelectMultiple(attrs={
                'multiple':True,
            })
        }
    def __init__(self, *args, **kwargs):
        _district_set = kwargs.pop('district_set',None)
        super(PostForm,self).__init__(*args, **kwargs)
        self.fields['details'].initial = 'No special requirements.'
        self.fields['salary'].label = 'Budget for this Tuition (Monthly):'
        self.fields['subjects'].label = 'Subjects Selection for this Tuition'
        self.fields['classes'].label = 'Student Class Selection'
        self.fields['image'].label = 'Upload a Photo of the Student/Students'
        self.fields['student_count'].label = 'Number of Student/Students for this Tuition'
        self.fields['details'].label = 'Special Requirements for the Tutor to follow:'
        self.fields['division'].label = 'Enter Address for this Tuition, Division:'
        self.fields['address'].label = 'House, Road No, Village/Mouza, Union / Ward No:'
        self.fields['title'].widget.attrs['placeholder'] = 'I am looking for a Math Tutor'
        self.fields['address'].widget.attrs['placeholder'] = '87/Ka, Nazrul Avenue, 2nd Kandirpar, Ward-10'
        self.fields['gender'].label = 'Looking for a:'
        self.fields['starting_from'].label = 'Tuition Starting From:'

class FileModelForm(forms.ModelForm):
    class Meta:
        model = Postfile
        fields = ['image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Com
        fields = ['text']
        labels = {
            'text':'Comment',
        }


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['gender', 'division', 'district', 'upazilla', 'available',]