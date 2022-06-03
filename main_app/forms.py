from django.forms import ModelForm
from .models import Comment, Gear, Profile
from django.contrib.auth.models import User

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class RunForm(ModelForm):
    class Meta:
        fields = ['name', 'date', 'distance', 'time', 'type']