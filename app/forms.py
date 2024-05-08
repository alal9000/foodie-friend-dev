from django.forms import ModelForm, CharField, ImageField, Form, Textarea, EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm, LoginForm

from . models import Event, Profile

#create event
class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = '__all__'
    exclude = ['user']
    widgets = {
            'description': Textarea(attrs={'rows': 4, 'maxlength': 200})
        }


# profile pic upload
class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ('profile_pic',)


# user signup
class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None) 
        self.fields['login'].label = 'Email'  

    def login(self, *args, **kwargs):

        return super().login(*args, **kwargs)
    