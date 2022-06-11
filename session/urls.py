from django.urls import path, include
from .views import loginuser, userpost, userapply, otherprofile, tuitionprofile, ownerprofile, logoutuser, notification, registration, change_pass, UserProfile, userProfile

app_name = 'session'

urlpatterns = [
    path('login/', loginuser, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('signup/', registration, name='signup'),
    path('password/', change_pass, name='password'),
    path('userpro/', userProfile, name='userProfile'),
    path('otherpro/<str:username>/', otherprofile, name='otherprofile'),
    path('notification/', notification, name='notification'),
    path('ownerprofile/', ownerprofile, name='ownerprofile'),
    path('tuitionpro/', tuitionprofile, name='tuitionpro'),
    path('userpost/', userpost, name='userpost'),
    path('userapply/', userapply, name='userapply'),

]