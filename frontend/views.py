from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decouple import config
import google.generativeai as genai
import requests

# Configure Gemini API
genai.configure(api_key=config('GEMINI_API_KEY'))

def home(request):
    """Home page view."""
    context = {
        "title": "Home",
        "user": request.user,
    }
    return render(request, "frontend/index.html", context)

def chatbot(request):
    """
    Handle chatbot: symptom analysis and clinic search using Gemini with 5 clinics.
    No database storage for clinics.
    """
    response = ""  # Symptom response
    clinic_response = None  # Clinic search feedback
    clinics = []  # List of clinics

    if request.method == "POST":
        # Symptom form handling
        symptoms = request.POST.get("symptoms", "").strip()
        lang = request.POST.get("language", "en")
        if symptoms:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                You are a health assistant for underserved communities in Mombasa.
                Language: {'Swahili' if lang == 'sw' else 'English'}.
                User symptoms: {symptoms}.
                Suggest a possible condition (disclaimer: not a diagnosis) and recommend visiting a clinic.
                Keep response concise, friendly, and culturally sensitive, under 100 words.
                """
                result = model.generate_content(prompt)
                response = result.text.strip()
            except Exception as e:
                response = f"Error: Could not connect to AI. Try example: 'I have a fever' -> Possible flu, visit a clinic."

        # Clinic search handling
        city = request.POST.get("city", "").strip()
        if city:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                clinic_prompt = f"""
                You are a health assistant for underserved communities in Kenya.
                Language: {'Swahili' if lang == 'sw' else 'English'}.
                User request: Find health centers or hospitals in {city}.
                Provide exactly 5 health centers or hospitals in or near {city}.
                Format as JSON:
                [
                    {{"name": "name1", "address": "address1"}},
                    {{"name": "name2", "address": "address2"}},
                    {{"name": "name3", "address": "address3"}},
                    {{"name": "name4", "address": "address4"}},
                    {{"name": "name5", "address": "address5"}}
                ]
                If fewer than 5, return only those found. If none, return empty list.
                Be concise, accurate, and focus on healthcare facilities.
                """
                result = model.generate_content(clinic_prompt)
                clinic_response = result.text.strip()

                # Parse Gemini response (expecting JSON)
                import json
                try:
                    # Clean up markdown code blocks if present
                    cleaned_response = clinic_response.replace('```json', '').replace('```', '').strip()
                    clinics = json.loads(cleaned_response)
                    if clinics:
                        clinic_response = f"Found {len(clinics)} health centers in {city}."
                    else:
                        clinic_response = f"No health centers found in {city}. Try another location."
                except json.JSONDecodeError:
                    clinic_response = f"Error: Invalid response format from AI for {city}."
                    clinics = []
            except Exception as e:
                clinic_response = f"Error: Could not fetch health centers for {city}. Please try again."
                clinics = []

    return render(request, 'frontend/chatbot.html', {
        'response': response,
        'clinic_response': clinic_response,
        'clinics': clinics,
    })

    """Health news page."""
    return render(request, "frontend/health_news.html")