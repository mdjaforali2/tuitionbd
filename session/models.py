from __future__ import division
from distutils.command.upload import upload
from email.policy import default
from random import choices
from secrets import choice
from sre_constants import CATEGORY
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.forms import FloatField, MultipleChoiceField
from multiselectfield import MultiSelectField


# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='district')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Upazilla(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='upazilla')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

# class Union(models.Model):
#     upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE, related_name='union')
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name       
#     class Meta:
#         ordering = ['name']


class Subject(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    def get_total_post(self):
        return self.subject_set.all().count()
    def get_post_list(self):
        return self.subject_set.all()


class Class_in(models.Model): 
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    CATEGORY = (
        ('Student', 'Tutor'),
        ('Teacher', 'Tuition'),
    )

    BLOOD_GROUP = (
        ('A+', 'A+ (A positive)'),
        ('A-', 'A- (A negative)'),
        ('B+', 'B+ (B positive)'),
        ('B-', 'B- (B negative)'),
        ('AB+', 'AB+ (AB positive)'),
        ('AB-', 'AB- (AB negative)'),
        ('O+', 'O+ (O positive)'),
        ('O-', 'O- (O negative)'),
    )

    RELIGION = (
        ('Islam', 'Islam'),
        ('Hindu', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Christianity', 'Chirstianity'),
        ('Other', 'Other'),
    )

    NATIONALITY = (
        ('Bangladeshi', 'Bangladeshi'),
        ('Other', 'Other')
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=20, choices=CATEGORY, null=True)
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP)
    nationality = models.CharField(max_length=30, choices=NATIONALITY)
    religion = models.CharField(max_length=20, choices=RELIGION, null=True)
    biodata = models.TextField()
    # union = models.ForeignKey(Union, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=30, null=True)
    image = models.ImageField(default='default.png', upload_to='session/images/')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class TuitionProfile(models.Model):
    GENRE_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    STATUS = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )
    Choice_style = (
        ('Group_Tuition', 'Group Tuition'),
        ('Private_Tuition', 'Private Tuition'),
    )   
    Choice_Place = (
        ('Class_Rooms', 'Class Rooms'),
        ('Coaching_Center', 'Coaching Center'),
        ('Home_Visit', 'Home Visit'),
        ('My_Place', 'My Place'),
        ('Online', 'Online'),
    )
    Choice_Approach = (
        ('Online_Help', 'Online Help'),
        ('Phone_Help', 'Phone Help'),
        ('Provide_Hand_Notes', 'Provide Hand Notes'),
        ('Video_Tutorials', 'Video Tutorials'),
    )
    Choice_Medium = (
        ('Arabic_Medium', 'Arabic'),
        ('Bangla_Medium', 'Bangla'),
        ('English_Medium', 'English'),
    )
    Choice_More_Options = (
        ('Sports_Section', 'Sports Section'),
        ('Extra_Curricular_Activities', 'Extra Curricular Activities'),
        ('Language Learning', 'Language Learning'),
        ('Computer Learning', 'Computer Learning'),
        ('Singing_Seciton', 'Singing Section'),
        ('Dance_Section', 'Dance Section'),
    )

    DAYS_PER_WEEK = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    )
    Experience = (
        ('No Experience', 'No Experience'),
        ('Less than 1 Year', 'Less than 1 Year'),
        ('1 Year', '1 Year'),
        ('2 Years', '2 Years'),
        ('3 Years', '3 Years'),
        ('4 Years', '4 Years'),
        ('5 Years', '5 Years'),
        ('More than 5 Years', 'More than 5 Years'),
    )

    class_selection = (
        ('Pre-Primary', 'Pre-Primary'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('Class 5', 'Class 5'),
        ('Class 6', 'Class 6'),
        ('Class 7', 'Class 7'),
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10'),
        ('SSC Candidate' , 'SSC Candidate'),
        ('College Student', 'College Student'),
        ('HSC Candidate', 'HSC Candidate'),
        ('University Student', 'University Student'),
        ('Madrasha Student', 'Madrasha Student'),
        ('Technical Student', 'Technical Student'),
        ('Diploma Student', 'Diploma Student'),
        ('Course Student', 'Course Student'),   
    )

    subjects = (
        ('Arabic', 'Arabic'),
        ('Bangla', 'Bangla'),
        ('English', 'English'),
        ('Math', 'Math'),
        ('General Science', 'General Science'),
        ('Bangladesh and Global Studies', 'Bangladesh and Global Studies'),
        ('Religion and Moral Studies', 'Religion and Moral Studies'),
        ('ICT', 'ICT'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Higher Math', 'Higher Math'),
        ('Accounting', 'Accounting'),
        ('Finance, Banking, and Insurance', 'Finance, Banking, and Insurance'),
        ('Business Entrepreneurship', 'Business Entrepreneurship'),
        ('Agricultural Studies', 'Agricultural Studies'),
        ('Statistics', 'Statistics'),
        ('Business Organization and Management', 'Business Organization and Management'),
        ('Production Management and Marketing', 'Production Management and Marketing'),
        ('Economics', 'Economics'),
        ('Psychology', 'Psychology'),
        ('Logic', 'Logic'),
        ('Sociology', 'Sociology'),
        ('Social Work', 'Social Work'),
        ('Geography', 'Geography'),
        ('Studies of Islam', 'Studies of Islam'),
        ('Home Science', 'Home Science'),
        ('All Subjects for the selected Class', 'All Subjects for the selected Class'),
    )

    Qualifications = (
        ('PSC or Equivalent', 'PSC or Equivalent'),
        ('JSC or Equivalent', 'JSC or Equivalent'),
        ('SSC or Equivalent', 'SSC or Equivalent'),
        ('HSC or Equivalent', 'HSC or Equivalent'),
        ('Bachelor', 'Bachelor'),
        ('''Master's''', '''Master's'''),
        ('Master of Philosopy', 'Master of Philosopy')

    )

    CURRENT_STATUS = (
        ('Graduated/Passed', 'Graduated/Passed'),
        ('Studying', 'Studying'),
    )


    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tuitionprofile')
    gender = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True) 
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=150)
    style = MultiSelectField(choices=Choice_style, max_choices=3, max_length=100)
    place = MultiSelectField(choices=Choice_Place, max_choices=3, max_length=100)
    approach = MultiSelectField(choices=Choice_Approach, max_choices=3, max_length=100)
    medium = MultiSelectField(choices=Choice_Medium, max_choices=2, max_length=100)
    classes = MultiSelectField(choices=class_selection, max_choices=9, max_length=150, null=True)
    subjects = MultiSelectField(choices=subjects, max_choices=10, max_length=150, null=True)
    more_options = MultiSelectField(choices=Choice_More_Options, max_choices=3, max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=100, choices=Experience, null=True)
    salary = models.CharField(max_length=100, blank=True)
    days_per_week = models.CharField(max_length=5, choices=DAYS_PER_WEEK, default='5')
    qualification = models.CharField(max_length=20, choices=Qualifications)
    current_status = models.CharField(max_length=100, null=True, choices=CURRENT_STATUS)
    graduated_from = models.CharField(max_length=100, blank=True)
    major_subject = models.CharField(max_length=100, null=True)
    id_certificate = models.ImageField(null = True, blank=True, upload_to='session/id_certificate/')
    status = models.CharField(max_length=100, choices=STATUS)
    
    def save(self):
        super().save()
        img = Image.open(self.id_certificate.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.id_certificate.path)

    def __str__(self):
        return "Tuition profile by "+ self.user.username + " (ID " + str(self.user.id) + ")" 


