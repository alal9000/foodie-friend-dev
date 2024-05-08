from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.account.views import SignupView, LoginView

from app.models import Event, Comment, Profile
from . forms import ProfileForm, CustomSignupForm, EventForm


# function based views
def home(request):
    all_events = Event.objects.order_by('-date_created')
    events_per_page = 12
    paginator = Paginator(all_events, events_per_page)
    page_number = request.GET.get('page')

    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    storage = get_messages(request)
    success_message = None
    for message in storage:
        if message.tags == 'success':
            success_message = message

    return render(request, 'app/dashboard.html', {'events': events, 'success_message': success_message})


def create(request):
    current_user_profile = request.user.profile
    form = EventForm()

    # create event form
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            if current_user_profile:
                new_event.host = current_user_profile
                new_event.save()
                messages.success(request, 'Event created successfully.')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'Error creating event. User profile not found.')

    return render(request, "app/create.html", {
        "form": form
    })



def recommendations(request):
    return render(request, 'app/recommendations.html')



def about(request):
    return render(request, 'app/about.html')



def contact(request):
    return render(request, 'app/contact.html')


def event(request, pk):
    event = Event.objects.get(id=pk)
    current_profile = request.user.profile
    is_guest = current_profile in event.guests.all()
    is_host = event.host == current_profile

    if request.method == 'POST':
        # comment
        if is_guest or is_host:
            comment_text = request.POST.get('comment_text')
            Comment.objects.create(profile=current_profile, event=event, comment=comment_text)
        else:
            messages.error(request, 'You must be an attendee to post a comment.')

        # join event
        if request.user.is_authenticated and not is_host:
            event.guests.add(current_profile)

            return redirect('event', pk=pk)  
    
    comments = Comment.objects.filter(event=event)

    context = {
        'event': event,
        'is_guest': is_guest,
        'comments': comments,
        'is_host': is_host,
    }

    return render(request, 'app/event.html', context)


def profile(request):
    profile = request.user.profile
    attended_events = Event.objects.filter(guests=profile.id)
    hosted_events = Event.objects.filter(host=profile)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    return render(request, "app/profile.html", {"form": form, "attended_events": attended_events, "hosted_events": hosted_events, "profile":profile})


def customer_profile(request):
    return render(request, "app/customer_profile.html")


def remove_attendee(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    current_user_profile = request.user.profile

    if current_user_profile in event.guests.all():
        event.guests.remove(current_user_profile)
        messages.success(request, 'Successfully removed from the event.')
    else:
        messages.error(request, 'You are not currently attending this event.')

    return redirect('home')


def direct_messages(request):
    return render(request, "app/messages.html")


# class based views
class CustomSignupView(SignupView):
    default_success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.default_success_url

    def form_valid(self, form):
        response = super().form_valid(form)
        first_name = form.cleaned_data.get('first_name') 
        if first_name:
            messages.success(self.request, f"Welcome, {first_name}! Your account was created successfully.")
        else:
            messages.success(self.request, "Welcome! Your account was created successfully.")
        return response


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        first_name = self.request.user.first_name
        if first_name:
            messages.success(self.request, f"Welcome, {first_name}! You have successfully logged in.")
        else:
            messages.success(self.request, "Welcome! You have successfully logged in.")
        return response