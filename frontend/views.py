from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decouple import config
from .models import Clinic
import google.generativeai as genai
import requests

# Configure Gemini API
genai.configure(api_key=config('GEMINI_API_KEY'))

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
    response = ""
    if request.method == "POST":
        symptoms = request.POST.get("symptoms")
        lang = request.POST.get("language", "en")
        try:
            # Initialize Gemini model (e.g., gemini-pro)
            model = genai.GenerativeModel('gemini-2.0-flash')
            # Craft prompt for health context
            prompt = f"""
            You are a health assistant for underserved communities in Mombasa.
            Language: {'Swahili' if lang == 'sw' else 'English'}.
            User symptoms: {symptoms}.
            Suggest a possible condition (disclaimer: not a diagnosis) and recommend visiting a clinic.
            Keep response concise, friendly, and culturally sensitive.
            """
            # Generate response
            result = model.generate_content(prompt)
            response = result.text
        except Exception as e:
            # Fallback for API errors
            response = f"Error: Could not connect to AI. Try example: 'I have a fever' -> Possible flu, visit a clinic."
    clinics = Clinic.objects.all()[:3]  # Show 3 clinics
    return render(request, 'frontend/chatbot.html', {'response': response, 'clinics': clinics})

API_KEY = '9e102f2b3b62445597925e29d1cb7aee'

def health_education(request):
    page = int(request.GET.get('page', 1))
    page_size = 9

    url = f'https://newsapi.org/v2/top-headlines?category=health&page={page}&pageSize={page_size}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'articles': articles})
    
    return render(request, 'frontend/health_education.html', {'articles': articles})


def health_news(request):
    return render(request, "frontend/health_news.html")