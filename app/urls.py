from django.urls import path
from . import views
from .views import CustomSignupView, CustomLoginView

urlpatterns = [
  path('', views.home, name="home"),
  path('create', views.create, name="create"),
  path('about', views.about, name="about"),
  path('recommendations', views.recommendations, name="recommendations"),
  path('contact', views.contact, name="contact"),
  path('messages', views.direct_messages, name='messages'),
  path('event/<str:pk>', views.event, name="event"),
  path('event/<int:event_id>/remove_attendee/', views.remove_attendee, name='remove_attendee'),
  # all_auth urls
  path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
  path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
  path('accounts/profile/', views.profile, name='profile'),
  path('accounts/customer_profile/<int:pk>/', views.customer_profile, name='customer_profile'),
]

