from cProfile import label
from logging import PlaceHolder
from xml.etree.ElementTree import Comment
from django.core import validators
from django import forms
from .models import Contact, Post, Postfile
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
        # labels = {
        #     'name':'Your Name',
        #     'phone':'Your Phone Number',
        #     'content':'Your Words',
        # }
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
    class Meta:
        model = Post
        exclude = ['user', 'id', 'slug', 'created_at', 'likes', 'views', 'applicants']
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
        self.fields['district'].widget = ListTextWidget(data_list=_district_set, name='district-set')
        self.fields['details'].initial = 'Nothing to say.'

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