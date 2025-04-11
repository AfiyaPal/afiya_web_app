"""
Routes for the frontend app
"""

from django.urls import path
from users.views.authentication import CustomPasswordResetDoneView
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.home, name="home"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("health-education/", views.health_education, name="health_education"),
    path("health-news/", views.health_news, name="health_news"),  
    
    # Password Reset Functionality
    path("password-reset-done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
]
