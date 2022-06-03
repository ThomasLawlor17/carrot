from django.contrib import admin
from .models import Run, Gear, Comment, Image, Profile
# Register your models here.
admin.site.register(Run)
admin.site.register(Gear)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Profile)