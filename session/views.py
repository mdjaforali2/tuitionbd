from __future__ import division
from dis import dis
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import UserProfile, Division, District, Upazilla
from tuition.models import Post 
import json
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, UpdateView
from django.shortcuts import render
from django.contrib import auth




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
            email = EmailMessage(mail_subject, message, to=[send_mail,])
            email.send()
            messages.success(request, 'Succesfully created an account!')
            return redirect('/session/login')
    else:
        form = SignUpForm()
    return render(request, 'session/signup.html', {'form':form})











class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or Email'

# Create your views here.
def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username, password=password) or authenticate(email=username, password=password)
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



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        userinput = request.POST['username']
        try:
            username = User.objects.get(email=userinput).username
        except User.DoesNotExist:
            username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"Successfully Logged In")
            return redirect('homeview')
        else:
            messages.error(request,'Invalid credentials, Please check username/email or password. ')
    else:
        form = AuthenticationForm()
    return render(request, "session/login.html", {'form': form})




def logoutuser(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('/session/login')



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
            return redirect('/session/ownerprofile/')
    else:
        form = UserProfileForm(instance=instance)

    return render(request, 'session/userproCreate.html')

# class UserProfileListView(ListView):
#     model = UserProfile
#     context_object_name = 'userprofile'

class UserProfileCreateView(CreateView):
    template_name = 'session/userproCreate.html'
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('session:ownerprofile')

class UserProfileUpdateView(UpdateView):
    template_name = 'session/userproCreate.html'
    model = UserProfile
    form_class = UserProfileForm


def userprofilecreate(request):
    userprofiles = UserProfile.objects.all()
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Succesfully Created!')
            return redirect ('/session/ownerprofile/') 
    else:
        form = UserProfileForm()
    return render(request, 'session/userproCreate.html', {'form': form, 'userprofiles':userprofiles}) 


def userproupdate(request, id):
    userprofiles = UserProfile.objects.all()                                        
    data = UserProfile.objects.get(id=id) 
    form = UserProfileForm(instance = data)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=data)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully Updated!')
            return redirect ('/session/ownerprofile/') 
    return render(request, 'session/userproupdate.html', {'form': form, 'userprofiles':userprofiles})


# class UserprofileView(FormView):
#     template_name = 'session/userproCreate.html'
#     model = UserProfile
#     form_class = UserProfileForm
#     success_url = reverse_lazy('session:ownerprofile')


def load_districts(request):
    division_id = request.GET.get('division')
    districts = District.objects.filter(division_id=division_id).order_by('name')
    return render(request, 'session/district_filter.html', {'districts': districts})

def load_upazillas(request):
    district_id = request.GET.get('district')
    upazillas = Upazilla.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'session/upazilla_filter.html', {'upazillas': upazillas})

# def load_unions(request):
#     upazilla_id = request.GET.get('upazilla')
#     unions = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
#     return render(request, 'session/union_filter.html', {'unions': unions})


def ownerprofile(request):
    user = request.user
    return render(request, 'session/userprofile.html', {'user':user})

def otherprofile(request, id):
    user = User.objects.get(id=id)
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
            form = TuitionProfileForm(request.POST, request.FILES, instance=instance)
        else:
            form = TuitionProfileForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            # sub = form.cleaned_data['subject']
            # for i in sub:
            #     obj.subject.add(i)
            #     obj.save()
            # class_in = form.cleaned_data['class_in']
            # for i in class_in:
            #     obj.class_in.add(i)
            #     obj.save()
            messages.success(request, 'Successfully Saved Your Tuition Profile')
            return redirect('/session/ownerprofile/')
    else:
        form = TuitionProfileForm(instance=instance)

    context = {
        'form' : form,
    }
    return render(request, 'session/tuitionProfileCreate.html', context)


def userpost(request):
    results = Post.objects.filter(user=request.user)
    context = {
    'object_list' : results,
    }
    return render(request, 'tuition/mypostlist.html', context)


def userapply(request):
    results = Post.objects.filter(applicants=request.user)
    context = {
    'object_list' : results,
    }
    return render(request, 'tuition/applylist.html', context)










from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "session/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'TuitionBD Admin Team' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="session/password_reset.html", context={"password_reset_form":password_reset_form,})
