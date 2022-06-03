from distutils import errors
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .models import Run, Gear, Profile, Image
from .forms import CommentForm, UserForm, ProfileForm, RunForm
import uuid
import boto3


S3_BASE_URL = 'https://s3-ca-central-1.amazonaws.com'
BUCKET = 'carrot-run'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# User functions

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('runs_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
@login_required
def account_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'account/detail.html', { 'user': user })

# Run Views

@login_required
def runs_index(request):
    runs = Run.objects.all()
    return render(request, 'runs/index.html', {'runs': runs})
@login_required
def run_detail(request, run_id):
    run = Run.objects.get(id=run_id)
    gear_not_added = Gear.objects.exclude(id__in = run.gear.all().values_list('id'))
    comment_form = CommentForm
    user = run.user
    print(run.type)
    return render(request, 'runs/detail.html', { 'run': run, 'gear': gear_not_added, 'comment_form': comment_form, 'user': user })
@login_required
def add_image(request, run_id):
  image_file = request.FILES.get('image-file', None)
  if image_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(image_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      image = Image(url=url, run_id=run_id)
      image.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('run_detail', run_id=run_id)

# Run comments
@login_required
def add_comment(request, run_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.run_id = run_id
        new_comment.save()
    return redirect('run_detail', run_id=run_id)


class CommentUpdate(UpdateView, LoginRequiredMixin):
    model = Comment
    fields = ['comment']
    success_url = 'run_detail'

class CommentDelete(DeleteView, LoginRequiredMixin):
    model = Comment
    success_url = 'run_detail'


# Change create run method for duration field
# def run_new(request):
#     form = RunForm()
#     return render(request, 'main_app/run_form.html', {'form': form})



# Run Class Forms
class RunCreate(CreateView, LoginRequiredMixin):
    model = Run
    fields = ['name', 'date', 'distance', 'time', 'type']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        


class RunUpdate(UpdateView, LoginRequiredMixin):
    model = Run
    fields = ['name', 'date', 'distance', 'time', 'type']
class RunDelete(DeleteView, LoginRequiredMixin):
    model = Run
    success_url = '/runs/'

# Gear Functions
@login_required
def assoc_gear(request, run_id, gear_id):
    Run.objects.get(id=run_id).gear.add(gear_id)
    return redirect('run_detail', run_id=run_id)
@login_required
def rmv_gear(request, run_id, gear_id):
    Run.objects.get(id=run_id).gear.remove(gear_id)
    return redirect('run_detail', run_id=run_id)

# Gear Class Forms

def gear_index(request):
    gear = Gear.objects.filter(user=request.user)
    return render(request, 'gear/index.html', {'gear': gear})


class GearDetail(DetailView, LoginRequiredMixin):
    model = Gear
class GearCreate(CreateView, LoginRequiredMixin):
    model = Gear
    fields = ['nickname', 'brand', 'model', 'type']
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.type == 'S':
            self.object.image = 'https://i.imgur.com/iOWhgv1.png'
        elif self.object.type == 'H':
            self.object.image = 'https://i.imgur.com/R215nCk.png'
        elif self.object.type == 'W':
            self.object.image = 'https://i.imgur.com/wjLfRiM.png'
        elif self.object.type == 'B':
            self.object.image = 'https://i.imgur.com/qD7bE9m.jpg'
        elif self.object.type == 'O':
            self.object.image = 'https://i.imgur.com/5gATmuA.png'
        self.object.user = self.request.user
        self.object.save()
        return redirect('/gear/')
    success_url = '/gear/'
class GearUpdate(UpdateView, LoginRequiredMixin):
    model = Gear
    fields = '__all__'
    success_url = '/gear/'
class GearDelete(DeleteView, LoginRequiredMixin):
    model = Gear
    success_url = '/gear/'

