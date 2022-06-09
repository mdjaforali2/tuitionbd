from distutils.command.upload import upload
from email.policy import default
from random import choices
from secrets import choice
from sre_constants import CATEGORY
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from tuition.models import District, Subject, Class_in
from multiselectfield import MultiSelectField



# Create your models here.
class UserProfile(models.Model):
    GENRE_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )

    CATEGORY = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )

    BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),

        ('O-', 'O-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=GENRE_CHOICES) 
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=14)
    nationality = models.CharField(max_length=30)
    religion = models.CharField(max_length=50)
    biodata = models.TextField()
    profession = models.CharField(max_length=50, choices=CATEGORY, null=True)
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
        ('Bangla_Medium', 'Bangla Medium'),
        ('English_Medium', 'English Medium'),
        ('Arabic_Medium', 'Arabic Medium'),
        ('Sports_Section', 'Sports Section'),
        ('Singing_Seciton', 'Singing Section'),
        ('Dance_Section', 'Dance Section'),
        ('Extra_Curricular_Activities', 'Extra Curricular Activites'),
        ('Language Learning', 'Language Learning'),
        ('Computer Learning', 'Computer Learning'),
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tuitionprofile')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='district')
    style = MultiSelectField(choices=Choice_style, max_choices=3, max_length=100)
    place = MultiSelectField(choices=Choice_Place, max_choices=3, max_length=100)
    approach = MultiSelectField(choices=Choice_Approach, max_choices=3, max_length=100)
    medium = MultiSelectField(choices=Choice_Medium, max_choices=3, max_length=100)
    subject = models.ManyToManyField(Subject, related_name='subjects')
    class_in = models.ManyToManyField(Class_in, related_name='classes')
    salary = models.CharField(max_length=100)
    days_per_week = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self):
        return "Tuition profile by "+ self.user.username + " (ID " + str(self.user.id) + ")" 
