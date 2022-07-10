from django.urls import path, include
from . import views
from .views import userProfile, login_view, otherpost, userproupdate, userprofilecreate, loginuser, userpost, userapply, otherprofile, tuitionprofile, ownerprofile, logoutuser, notification, registration, change_pass, password_reset_request
from django.contrib.auth import views as auth_views

app_name = 'session'

urlpatterns = [
    # path('login/', loginuser, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('signup/', registration, name='signup'),
    path('password/', change_pass, name='password'),
    # path('userpro/', userProfile, name='userProfile'),
    path('otherpro/<int:id>/', otherprofile, name='otherprofile'),
    path('notification/', notification, name='notification'),
    path('ownerprofile/', ownerprofile, name='ownerprofile'),
    path('tuitionpro/', tuitionprofile, name='tuitionpro'),
    path('userpost/', userpost, name='userpost'),
    path('otherpost/<int:id>/', otherpost, name='otherpost'),
    path('userapply/', userapply, name='userapply'),
    # path('userpro/', UserprofileView.as_view(), name='userProfile'),
    path('userprocreate/', userprofilecreate, name='userProfilecreate'),
    # path('userprocreate/', views.UserProfileCreateView.as_view(), name='userProfilecreate'),
    path('userproupdate/<int:id>/', userproupdate, name='userProfileupdate'),
    # path('userproupdate/<slug:pk>/', views.UserProfileUpdateView.as_view(), name='userProfileupadate'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-upazillas/', views.load_upazillas, name='ajax_load_upazillas'),
    # path('ajax/load-unions/', views.load_unions, name='ajax_load_unions'),

    #path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset", password_reset_request, name="password_reset"),
    

]