from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  profile_pic = models.ImageField(default="profile2.png", null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return f"{self.user}"

class Event(models.Model):
  ESTABLISHMENTS = (
    ('Cafes', 'cafes'),
    ('Restaurants', 'restaurants'),
    ('Bars', 'bars'),
    ('Clubs', 'clubs'),
  )

  event_title = models.CharField(max_length=100)
  attendees = models.IntegerField(null=True, blank=True)
  location = models.CharField(max_length=100, null=True, blank=True)
  event_datetime = models.DateTimeField(verbose_name="Event Date and Time", null=True, blank=False)
  establishment_type = MultiSelectField(choices=ESTABLISHMENTS, max_length=200, null=True)
  description = models.TextField()
  host = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, blank=True)
  guests = models.ManyToManyField(Profile, related_name='attended_events', blank=True)

  def __str__(self):
      return self.event_title


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"
