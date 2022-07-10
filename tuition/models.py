from distutils.archive_util import make_zipfile
from distutils.command.upload import upload
import email
from email.mime import image
from email.policy import default
from logging import PlaceHolder
from pyexpat import model
from secrets import choice
from sre_constants import CATEGORY
from django.db.models.deletion import CASCADE
from unicodedata import category
from django.db import models
from django.utils.timezone import now
from PIL import Image
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from session.models import Division, District, Upazilla, TuitionProfile



class PostManager(models.Manager):
    def sorted(self, title):
        return self.order_by(title)
    def less_than(self, size):
        return self.filter(salary__lt=size)
# Create your models here.



class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=17)
    content = models.TextField()

    def __str__(self):
        return self.name

    
class Post(models.Model):
    CATEGORY = (
        ('Student', 'Student'),
        ('Tutor', 'Tutor')
    )
    MEDIUM = (
        ('Arabic_Medium', 'Arabic'),
        ('Bangla_Medium', 'Bangla'),
        ('English_Medium', 'English'),
    )

    STUDENT_COUNT = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('More than 4', 'More than 4'),
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
    GENRE_CHOICES = (
        ('Male Tutor', 'Male Tutor'),
        ('Female Tutor', 'Female Tutor'),
        ('Male/Female Tutor', 'Male/Female Tutor')
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    starting_from = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50, null=True)
    student_count = models.CharField(max_length=50, choices=STUDENT_COUNT, default='1')
    slug = models.CharField(max_length=100, default=title)
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=100, choices=CATEGORY)
    created_at = models.DateTimeField(default=now)
    medium = MultiSelectField(choices=MEDIUM, max_choices=2, max_length=100)
    classes = MultiSelectField(choices=class_selection, max_choices=7, max_length=150, null=True)
    subjects = MultiSelectField(choices=subjects, max_choices=10, max_length=150, null=True)
    image = models.ImageField(default='student.png',upload_to='tuition/images/')
    salary = models.IntegerField()
    days_per_week = models.CharField(max_length=5, choices=DAYS_PER_WEEK, default='5')
    details = models.TextField()
    likes = models.ManyToManyField(User, related_name='post_likes')
    views = models.ManyToManyField(User, related_name='post_views')
    applicants = models.ManyToManyField(User, related_name='applicant_set')
    candidate = models.ManyToManyField(TuitionProfile, related_name='candidate')
    tutor = models.ManyToManyField(TuitionProfile, related_name='tutor')
    
    def total_likes(self):
        return self.likes.count()
    
    def total_views(self):
        return self.views.count()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail (output_size)
            img.save(self.image.path)
    def __str__(self):
        return self.title + " by :" + self.user.username

 

    def proper_title(self):
        return str(self.title).title()

    def details_short(self):
        details_words = self.details.split(' ')
        if len(details_words) > 20:
            return ''.join(details_words[:20]) + "...."
        else:
            return self.details

    objects = models.Manager()
    items = PostManager()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.user.username + ": "+self.text[0:15]

class Postfile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    def save(self, *args, **kwargs):
        super(Postfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Filter(models.Model):
    GENRE_CHOICES = (
        ('Male Tutor', 'Male Tutor'),
        ('Female Tutor', 'Female Tutor'),
        ('Male/Female Tutor', 'Male/Female Tutor')
    )
    gender = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.SET_NULL, blank=True, null=True)
    available = models.BooleanField(default=True, blank=True)


