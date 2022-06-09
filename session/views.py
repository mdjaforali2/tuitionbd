from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import UserProfile

# Create your views here.
def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homeview')
            else:
                messages.error(request, '')
        else:
            messages.error(request, '')
    else:
        form = AuthenticationForm()
    return render(request, 'session/login.html', {'form':form})

def logoutuser(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('/session/login')

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = "An Account has been Created"
            message = render_to_string('session/account.html', {
                'user': user,
                'domain': current_site.domain,
            })
            send_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[send_mail])
            email.send()
            messages.success(request, 'Succesfully created an account!')
            return redirect('/session/login')
    else:
        form = SignUpForm()
    return render(request, 'session/signup.html', {'form':form})

def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid:
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been successfully changed!')
            return redirect('homeview')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'session/change_pass.html', {'form': form})

def userProfile(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None
    if request.method == "POST":    
        if instance:
            form = UserProfileForm(request.POST, request.FILES, instance=instance)
        else:
            form = UserProfileForm(request.POST, request.FILES,)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Successfully Saved Your Profile')
            return redirect('homeview')
    else:
        form = UserProfileForm(instance=instance)

    context = {
        'form' : form,
    }
    return render(request, 'session/userproCreate.html', context)

def ownerprofile(request):
    user = request.user
    return render(request, 'session/userprofile.html', {'user':user})

def otherprofile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'session/otherprofile.html', {'user':user})

def notification(request):
    return render(request, 'session/notification.html')

from .models import TuitionProfile
from .forms import TuitionProfileForm


def tuitionprofile(request):
    try:
        instance = TuitionProfile.objects.get(user=request.user)
    except:
        instance = None
    if request.method == "POST":    
        if instance:
            form = TuitionProfileForm(request.POST, instance=instance)
        else:
            form = TuitionProfileForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            sub = form.cleaned_data['subject']
            for i in sub:
                obj.subject.add(i)
                obj.save()
            class_in = form.cleaned_data['class_in']
            for i in class_in:
                obj.class_in.add(i)
                obj.save()
            messages.success(request, 'Successfully Saved Your Tuition Profile')
            return redirect('/session/ownerprofile/')
    else:
        form = TuitionProfileForm(instance=instance)

    context = {
        'form' : form,
    }
    return render(request, 'session/tuitionProfileCreate.html', context)
