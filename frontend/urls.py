"""
Routes for the frontend app
"""

from django.urls import path
from users.views.authentication import CustomPasswordResetDoneView
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.home, name="index"),
    path("chatbot/", views.chatbot, name="chatbot"),

    # Password Reset Functionality
    path("password-reset-done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),

    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<str:pk>/", views.blog_detail, name="blog_detail")
]
