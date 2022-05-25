from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Run, Gear, Profile
from .forms import CommentForm, UserForm, ProfileForm
import time

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
def account_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'account/detail.html', { 'user': user })

# Run Views


def run_index(request,):
    runs = Run.objects.all()
    return render(request, 'runs/index.html', {'runs': runs})
def runs_detail(request, run_id, user_id):
    run = Run.objects.get(id=run_id)
    gear_not_added = Gear.objects.exclude(id_in = run.gear.all().values_list('id'))
    comment_form = CommentForm
    profile = Profile.objects.get(user=user_id)
    return render(request, 'runs/detail.html', { 'run': run, 'gear': gear_not_added, 'comment_form': comment_form, 'profile': profile })

# Run comments

def add_comment(request, run_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.run_id = run_id
        new_comment.save()
    return redirect('detail', run_id=run_id)

# Run Class Forms

class RunCreate(CreateView):
    model = Run
    fields = ['name', 'date', 'distance', 'time', 'image', 'type']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class RunUpdate(UpdateView):
    model = Run
    fields = '__all__'
class RunDelete(DeleteView):
    model = Run
    success_url = '/runs/'

# Gear Functions
def assoc_gear(request, run_id, gear_id):
    Run.objects.get(id=run_id).gear.add(gear_id)
    return redirect('detail', run_id=run_id)
def rmv_gear(request, run_id, gear_id):
    Run.objects.get(id=run_id).gear.remove(gear_id)
    return redirect('detail', run_id=run_id)

# Gear Class Forms

class GearList(ListView):
    model = Gear
class GearDetail(DetailView):
    model = Gear
class GearCreate(CreateView):
    model = Gear
    fields = '__all__'
class GearUpdate(UpdateView):
    model = Gear
    fields = '__all__'
class GearDelete(DeleteView):
    model = Gear
    success_url = '/gear/'

