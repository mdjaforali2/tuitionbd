from cgitb import text
from email import message
from enum import unique
from multiprocessing import context
from queue import Empty
import re
from django.forms import SlugField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from re import template
from django.shortcuts import render, HttpResponse
from urllib3 import HTTPResponse
from .models import Comment,  Postfile, Contact, Post
from .forms import CommentForm, ContactForm, PostForm, FileModelForm, CommentForm
from django.views import View
from django.views.generic import FormView, DetailView, DeleteView, UpdateView, ListView, CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.db import models
from django.contrib import messages
from django.db.models import Q
import requests
import json
from .templatetags import tag
from session.models import TuitionProfile, User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from session.models import UserProfile, TuitionProfile

# Create your views here.
def contact(request):
    initials = {
        'phone': '+88',
        'content': 'My problem is ',
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, initial=initials)
        # name = request.POST['name']
        # phone = request.POST['phone']
        # content = request.POST['content']
        if form.is_valid():
            # name = form.cleaned_data['name']
            # phone = form.cleaned_data['phone']
            # content = form.cleaned_data['content']
            # print(name, phone, content)
            # obj = Contact(name=name, phone=phone, content=content)
            # obj.save() # model_manager
            form.save()
    else:
        form = ContactForm(initial=initials)
    return render(request, 'contact.html', {'form':form})

# def post(request):
#     if request.method == 'POST':
#         post = PostForm(request.POST)
#         if post.is_valid():
#             post.save()
#     else:
#         post = PostForm()
#     return render(request, 'post.html', {'post':post})

def postview(request):
    posts = Post.objects.all()
    return render(request, 'tuition/postview.html', {'post':posts})




def postcreate(request):
    if request.method == "POST":
        e = 0
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            # upazilla = form.cleaned_data['upazilla']
            # if not District.objects.filter(name=dis).exists():
                # disobj = District(name=dis)
                # disobj.save()

            # sub = form.cleaned_data['subjects']
            # for i in sub:
            #     obj.subjects.add(i)
            #     obj.save()
       
            # class_in = form.cleaned_data['classes']
            # for i in class_in:
            #     obj.classes.add(i)
            #     obj.save()

            us = TuitionProfile.objects.all()     
            for i in us:
                count = 0
                m = 0
                s = 0
                c = 0
                g = 0
                e = 0
                
                if i.user != request.user:
                    if i.status == 'Available':
                        count += 1

                    if i.upazilla == obj.upazilla:
                        count += 1

                    for j in i.medium:
                        for k in obj.medium:
                            if j==k:
                                m+=1
                                break
                    
                    for j in i.subjects:
                        for k in obj.subjects:
                            if j==k:
                                s+=1
                                break
            
                    for j in i.classes:
                        for k in obj.classes:
                            if j==k:
                                c+=1
                                break
                    
                    if obj.gender == 'Any':
                        g += 1

                    else:
                        if obj.gender == i.gender:
                            g += 1
                    
                    if obj.gender:
                        e += 1

                    if count >= 2 and m >= 1 and s >= 1 and c >= 1 and g>=1:
                            receiver = i.user
                            postid = obj.id
                            if receiver != request.user:
                                current_site = get_current_site(request)
                                mail_subject = "Post Alert From TuitionBD"
                                message = render_to_string('tuition/searchmatch.html', {
                                    'user': receiver,
                                    'domain': current_site.domain,
                                    'id': postid,
                                })
                                send_mail = i.user.email
                                email = EmailMessage(mail_subject, message, to=[send_mail])
                                email.send()
                                notify.send(request.user, recipient=receiver, verb=" has created a post which matches your profile" + f'''<a href="/tuition/postdetail/{obj.id}/"> go</a>''')
            messages.success(request, 'Succesfully Posted!')
            return redirect ('/tuition/postlist/')  
    
    else:
        # form = PostForm(district_set=District.objects.all().order_by('name'))
        form = PostForm()
        e = 0
        
    return render(request, 'tuition/postcreate.html', {'form': form, 'e':e})



def postupdate(request, id):                                         
    data = Post.objects.get(id=id)  
    form = PostForm(instance = data)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=data)  
        if form.is_valid():
            form.save()
            dis = form.cleaned_data['district']
            # if not District.objects.filter(name=dis).exists():
            #     disobj = District(name=dis)
            #     disobj.save()
            messages.success(request, 'Succesfully Updated!')
            return redirect ('/tuition/postlist/') 
    return render(request, 'tuition/postcreate.html', {'form': form})

# class ContactView(View):
#     form_class = ContactForm
#     template_name = 'contact.html'
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form':form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("Success")
#         return render(request, self.template_name, {'form':form})
        
class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/'
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your form is successfully submitted.')
        return super().form_valid(form)
    # def form_invalid(self, form):
    #     return super().form_invalid(form)
    # def get_success_url(self):
    #     return reverse_lazy('homeview')


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'tuition/postcreate.html'
    # success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        # id = self.object.id
        return reverse_lazy('tuition:postlist')


class PostListView(ListView):
    template_name = 'tuition/postlist.html'
    queryset = Post.objects.all()
    # context_object_name = 'posts'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['posts'] = context.get('objects_list')
        # context['msg'] = 'This is a post list'
        # context['districts'] = District.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'tuition/postdetail.html'
    up = 0
    tp = 0
    def get_context_data(self, *args, **kwargs):
        self.object.views.add(self.request.user)
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super().get_context_data(*args, **kwargs)
        post = context.get('object')
        comments = Comment.objects.filter(post=post.id, parent=None)
        replies = Comment.objects.filter(post=post.id).exclude(parent=None) 
        DictofReply = {}
        for reply in replies:
            if reply.parent.id not in DictofReply.keys():
                DictofReply[reply.parent.id] = [reply]
            else:
                DictofReply[reply.parent.id].append(reply)

        if UserProfile.objects.filter(user=self.request.user).exists():
            up = 1
        else:
            up = 0

        if TuitionProfile.objects.filter(user=self.request.user).exists():
            tp = 1
        else:
            tp = 0

        applied_applicants = post.applicants.all()
        selected_candidate = post.candidate.all()
        total_candidate = post.candidate.all().count()
        tutor_count = post.tutor.all().count()

        if total_candidate>= 1:
            count = 1
        elif total_candidate == 0:
            count = 0

        if tutor_count >= 1:
            t_c = 1
        elif tutor_count == 0:
            t_c = 0

        context['applied_applicants'] = applied_applicants
        context['selected_candidate'] = selected_candidate
        context['count'] = count
        context['t_c'] = t_c
        context['up'] = up
        context['tp'] = tp
        context['liked'] = liked
        context['comments'] = comments
        context['DictofReply'] = DictofReply
        return context

class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'tuition/postcreate.html'
    # success_url = '/'
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)
    def get_success_url(self):
        id = self.object.id
        return reverse_lazy('tuition:postdetail', kwargs={'pk':id})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'tuition/delete.html'
    success_url = reverse_lazy('tuition:postlist')


def search(request):
    query = request.POST.get('search', '')
    if query:
        queryset = (Q(title__icontains=query)) |  (Q(details__icontains=query)) | (Q(medium__icontains=query)) | (Q(category__icontains=query)) | (Q(subject__name__icontains=query)) | (Q(class_in__name__icontains=query)) | (Q(user__username__icontains=query))
        results = Post.objects.filter(queryset).distinct()
    else:
        results = []

    context = {
        'object_list' : results
    }
    # context['districts'] = District.objects.all()
    return render(request, 'tuition/search.html', context)


def filter(request):
    if request.method == "POST":
        subject = request.POST['subject']
        class_in = request.POST['class_in']
        salary_from = request.POST['salary_from']
        salary_to = request.POST['salary_to']
        # available = request.POST['available']
        district = request.POST['district']

        # if available:
        #     results = results.filter(available=True)
        if district or subject or class_in:
            queryset = (Q(district__icontains=district)) & (Q(class_in__name__icontains=class_in)) & (Q(subject__name__icontains=subject)) 
            results = Post.objects.filter(queryset).distinct()
            if salary_from:
                results = results.filter(salary__gte=salary_from)
            if salary_to:
                results = results.filter(salary__lte=salary_to)
        else:
            results = []

        context = {
        'object_list' : results,
        
        }

        # context['districts'] = District.objects.all()
        return render(request, 'tuition/search.html', context)


def postview(request):
    api_request = requests.get("https://jsonplaceholder.typicode.com/posts")
    try:
        api = json.loads(api_request.content)
    except:
        api = "Error 404"
    return render(request, 'tuition/postlistapi.html', {'api':api})

from django.http import HttpResponseRedirect
from notifications.signals import notify

def likepost(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb='has liked on your post' + f''' <a href="/tuition/postdetail/{post.id}/">Go</a>''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def addcomment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        parentid  = request.POST['parentid']
        postid  = request.POST['postid']
        post = Post.objects.get(id=postid)
        if set(comment) == {' '} or comment=='':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if parentid:
            parent = Comment.objects.get(id=parentid)
            newcom= Comment(text=comment, user=request.user, post=post, parent=parent)
            newcom.save()
            if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb='has replied on your comment' + f''' <a href="/tuition/postdetail/{post.id}/">Go</a>''')
        else:
            newcom= Comment(text=comment, user=request.user, post=post)
            newcom.save()
            if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb='has commented on your post' + f''' <a href="/tuition/postdetail/{post.id}/">Go</a>''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addphoto(request, id):
    post = Post.objects.get(id=id)
    images = Postfile.objects.filter(post=post.id)
    if request.method == 'POST':
        form = FileModelForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            obj = Postfile(image=image, post=post)
            obj.save()
            messages.success(request, 'Succesfully uploaded Image')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = FileModelForm()
    context = {
            'form': form,
            'id' : id,
            'images' : images,
        }
    return render(request,'tuition/addphoto.html', context)


def commentedit(request, id, pk):
    comment = Comment.objects.get(id=id)
    form = CommentForm(instance = comment)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment edited successfully!')
            return redirect(f"/tuition/postdetail/{pk}/") 
    return render(request, 'tuition/commentedit.html', {'form': form})

def commentdelete(request, id, pk):
    context = {
        'commentid' : id,
        'postid': pk,
    }
    return render(request, 'tuition/commentdelete.html', context) 

def confirmcommentdelete(request, id, pk):
    Comment.objects.filter(id=id).delete()
    return redirect(f"/tuition/postdetail/{pk}/")

def replyedit(request, id, pk):
    comment = Comment.objects.get(id=id)
    form = CommentForm(instance = comment)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Reply edited successfully!')
            return redirect(f"/tuition/postdetail/{pk}/") 
    return render(request, 'tuition/replyedit.html', {'form': form})
    
def replydelete(request, id, pk):
    Comment.objects.filter(id=id).delete()
    return redirect(f"/tuition/postdetail/{pk}/")


def apply(request,id):
    post = Post.objects.get(id=id)
    if request.user != post.user:
        post.applicants.add(request.user)
        post.save()
        notify.send(request.user, recipient=post.user, verb="has applied on a" + f'''<a href="/tuition/postdetail/{id}/"> Post</a>''' + " of you." + f'''<a href="/session/otherpro/{request.user.id}/"> See Profile</a>''')
        messages.success(request, 'You have successfully applied for this tuition')
        return redirect(f"/tuition/postdetail/{id}/")


def cancel(request,id):
    post = Post.objects.get(id=id)
    if request.user != post.user:
        post.applicants.remove(request.user)
        post.save()
        messages.warning(request, 'Your application has been canceled')
        return redirect(f"/tuition/postdetail/{id}/")
    

def applicants(request, id):
    post = Post.objects.get(id=id)
    applicants = post.applicants.all()
    context = {
        'applicants' : applicants,
        'id' : id,
    }
    return render(request, 'tuition/applicantslist.html', context)


def hire(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    context = {
        'candidate' : selected_candidate,
        'id' : id,
        'post' : post,
    }
    return render(request, 'tuition/hiring_notice.html', context)


def confirm_hiring(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    deposit = post.salary * 0.1
    recipient=selected_candidate.user
    current_site = get_current_site(request)
    context = {
        'candidate' : selected_candidate,
        'id' : id,
        'post' : post,
        'recipient' : recipient,
        'deposit' : deposit,
        'domain' : current_site.domain,
    }
    if request.user == post.user:
        post.candidate.add(selected_candidate)
        post.save()
        mail_subject = "TuitionBD: Application Update"
        message = render_to_string('tuition/candidate_mail.html', context)
        send_mail = recipient.email
        email = EmailMessage(mail_subject, message, to=[send_mail])
        # email.send()
        notify.send(sender=request.user, recipient=recipient, verb="has selected you for this " + f'''<a href="/tuition/postdetail/{id}/">Tuition.</a>''')
        return redirect(f"/tuition/postdetail/{id}/")


def candidate_decision_make(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    deposit = post.salary * 0.1
    context = {
        'candidate' : selected_candidate,
        'id' : id,
        'post' : post,
        'deposit' : deposit,
        'pk' : pk,
    }
    return render(request, 'tuition/candidate_decision_make.html', context)


def candidate_cancel(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    selected_candidate.user
    post.candidate.remove(selected_candidate)
    post.applicants.remove(selected_candidate.user)
    post.available = True
    post.save()
    messages.warning(request, 'Your application has been cancelled')
    notify.send(sender=request.user, recipient=post.user, verb="is no more interested in this" + f'''<a href="/tuition/postdetail/{id}/"> Tuition Post.</a>''' + f'''<a href="/tuition/applicants/{id}/"> Find another Tutor.</a>''')
    return redirect('/')

def candidate_accept(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    if request.user == selected_candidate.user:
        post.tutor.add(selected_candidate)
        post.available = False
        post.save()
    return redirect(f"/tuition/postdetail/{id}/")

def candidate_delete(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    context = {
        'candidate' : selected_candidate,
        'id' : id,
        'post' : post,
        'pk' : pk,
    }
    return render(request, 'tuition/candidate_delete.html', context)


def candidate_delete_confirm(request, id, pk):
    post = Post.objects.get(id=id)
    selected_candidate = TuitionProfile.objects.get(id=pk)
    cancelled_candidate_name = selected_candidate.user.get_full_name()
    post.candidate.remove(selected_candidate)
    post.save()
    messages.warning(request, f'''{cancelled_candidate_name} has been removed from hiring''')
    return redirect(f"/tuition/postdetail/{id}/")

