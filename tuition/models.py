from distutils.command.upload import upload
import email
from email.mime import image
from email.policy import default
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

class PostManager(models.Manager):
    def sorted(self, title):
        return self.order_by(title)
    def less_than(self, size):
        return self.filter(salary__lt=size)
# Create your models here.

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

class District(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name        

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=17)
    content = models.TextField()

    def __str__(self):
        return self.name

# class Post(models.Model):
#     CATEGORY = (
#         ('Techer', 'Teacher'),
#         ('Student', 'Student'),
#     )
#     MEDIUM = (
#         ('Bangla', 'Bangla'),
#         ('English', 'English'),
#         ('Hindi', 'Hindi'),
#         ('Urdu', 'Urdu'),
#         ('Arabic', 'Arabic'),
#     )

#     # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100)
#     slug = models.CharField(max_length=100, default=title)
#     email = models.EmailField()
#     salary = models.FloatField()
#     details = models.TextField()
#     available = models.BooleanField()
#     category = models.CharField(max_length=100, choices=CATEGORY)
#     created_at = models.DateTimeField(default=now)
#     image = models.ImageField(default='tuition/images/default.jpeg',upload_to='tuition/images/')
#     medium = MultiSelectField(max_length=200, max_choices=5, choices=MEDIUM, default='Bangla')
#     subject = models.ManyToManyField(Subject, related_name='subject_set')
#     class_in = models.ManyToManyField(Class_in, related_name='class_set')
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         super(Post, self).save(*args, **kwargs)
#         img = Image.open(self.image.path)
#         if img.height > 300 or img.width > 300:
#             output_size=(300,300)
#             img.thumbnail (output_size)
#             img.save(self.image.path)

    
class Post(models.Model):
    CATEGORY = (
        ('Student', 'Student'),
        ('Tutor', 'Tutor')
    )
    MEDIUM = (
        ('Bangla', 'Bangla'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Urdu', 'Urdu'),
        ('Arabic', 'Arabic'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default=title)
    email = models.EmailField()
    salary = models.FloatField()
    details = models.TextField()
    available = models.BooleanField()
    category = models.CharField(max_length=100, choices=CATEGORY)
    created_at = models.DateTimeField(default=now)
    image = models.ImageField(default='default.png',upload_to='tuition/images/')
    medium = MultiSelectField(max_length=200, max_choices=5, choices=MEDIUM, default='Bangla')
    subject = models.ManyToManyField(Subject, related_name='subject_set')
    class_in = models.ManyToManyField(Class_in, related_name='class_set')
    district = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    views = models.ManyToManyField(User, related_name='post_views')
    applicants = models.ManyToManyField(User, related_name='applicant_set')

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

    def get_subject_list(self):
        sub = self.subject.all()
        subjects = ""
        for s in sub:
            subjects += str(s.name) + " "
        return subjects

    def get_class_list(self):
        cls = self.class_in.all()
        classes = ""
        for c in cls:
            classes += str(c.name) + " "
        return classes

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
