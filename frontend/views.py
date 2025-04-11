from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    """Home page view

    Args:
        request (GET): The request object

    Returns:    
        HTTPResponse: The rendered home page
    """
    
    context = {
        "title": "Home",
        "user": request.user,
    }
    return render(request, "frontend/index.html", context)

def chatbot(request):
    return render(request, "frontend/chatbot.html")

def emergency(request):
    return render(request, "frontend/emergency.html")

def health_education(request):
    return render(request, "frontend/health_education.html")

def health_news(request):
    return render(request, "frontend/health_news.html")