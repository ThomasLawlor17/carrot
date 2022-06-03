from django.db import models
from django.forms import CharField, DateField, IntegerField
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
import time

# Create your models here.
TYPES = (
    ('O', 'Outdoor'),
    ('I', 'Indoor'),
    ('T', 'Track'),
)

GEARTYPE = (
    ('S', 'Shoes'),
    ('H', 'Heartrate-monitor'),
    ('W', 'Watch'),
    ('B', 'Bottle'),
    ('O', 'Other'),
)



class Gear(models.Model):
    nickname = models.CharField(max_length=50)
    brand = models.CharField(max_length=40, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    distance = models.IntegerField(default=0, null=True, blank=True)
    type = models.CharField(
        max_length=1,
        choices=GEARTYPE,
        default=GEARTYPE[0][0]
    )
    image = models.CharField(max_length=200, default='https://i.imgur.com/iOWhgv1.png')
    
    def __str__(self):
        return self.nickname
    user = models.ForeignKey(User, on_delete=models.CASCADE)

now = time.localtime()[3]
def default_run_name():
    if now < 11:
        return 'Morning Run'
    elif now >= 11 and now < 14:
        return 'Lunch Run'
    elif now >= 14 and now < 17:
        return 'Afternoon Run'
    elif now >= 17:
        return 'Evening Run'
    else:
        pass

class Run(models.Model):
    name = models.CharField(max_length=50,
    default=default_run_name())
    date = models.DateField(default=date.today)
    distance = models.IntegerField()
    time = models.DurationField()
    type = models.CharField(
        max_length=1,
        choices=TYPES,
        default=TYPES[0][0]
    )
    gear = models.ManyToManyField(Gear)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}|{self.date}|{self.distance}|{self.time}'

    def get_absolute_url(self):
        return reverse('run_detail', kwargs={'run_id': self.id})
        

    class Meta:
        ordering = ['-date']

class Image(models.Model):
    url = models.CharField(max_length=200)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for run_id: {self.run_id} @{self.url}"


class Comment(models.Model):
    comment = models.TextField(max_length=300)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=100, default='https://i.imgur.com/G4NNtuW.png')