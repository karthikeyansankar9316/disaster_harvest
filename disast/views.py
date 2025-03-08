from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CitizenSignupForm, AgencySignupForm
from .models import Disaster, CommunityPost
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DisasterForm
from .models import Disaster
from .utils import scrape_disaster_data

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        print(form.errors) 
        if form.is_valid():
            print("validating")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_agency:
                    return redirect('agency_dashboard')  # Redirect to agency dashboard
                elif user.is_citizen:
                    return redirect('citizen_dashboard')  # Redirect to citizen dashboard
                else:
                    return redirect('home')  # Default fallback
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = CustomAuthenticationForm()
        print(form.errors) 
    return render(request, 'login.html', {'form': form})


import requests

def home(request):
    # Your OpenWeatherMap API configuration
    API_KEY = 'your_openweather_api_key'
    CITY = 'your_city_name'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

    weather_data = {}
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")

    disasters = Disaster.objects.all()  # Existing disasters data
    return render(request, 'home.html', {'disasters': disasters, 'weather': weather_data})

def home(request):
    disaster = [
        {
            "image_url": "/static/imgs/disaster1.jpg",
            "title": "Flood in Wayanad",
            "description": "Severe land slide in wayanad,kerala affecting thousands.",
            "link": "#",
        },
        {
            "image_url": "/static/imgs/disaster2.jpg",
            "title": "Earthquake near Tibet",
            "description": "earthquake - 167 km southwest of Shigatse, Tibet.",
            "link": "https://www.volcanodiscovery.com/earthquakes/china.html?quake=12061036",
        },{
            "image_url": "/static/imgs/3.jpg",
            "title": "Tornado",
            "description": "Severe Tornado in japan.",
            "link": "#",
        },
        {
            "image_url": "/static/imgs/4.jpg",
            "title": "Blast",
            "description": "Blast in nepal.",
            "link": "#",
        },
        {
            "image_url": "/static/imgs/5.jpg",
            "title": "flood in nepal",
            "description": "flood in nepal affecting thousands.",
            "link": "#",
        },
        {
            "image_url": "/static/imgs/6.jpg",
            "title": "Forest Fire",
            "description": "Fire.",
            "link": "#",
        },
    ]
    API_KEY = 'dc9f9ace5054345fa3cb5ccb8c8ea7f8'
    CITY = 'Avadi'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

    weather_data = {}
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")

    disasters = Disaster.objects.all()  # Existing disasters data
    return render(request, "home.html", {"disaster": disaster, 'weather': weather_data})


from .models import User

# Citizen Signup View
def csignup(request):
    if request.method == 'POST':
        form = CitizenSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            user.is_citizen = True  # Mark as a citizen
            user.save()  # Save to DB
            login(request, user)  # Log the user in
            return redirect('citizen_dashboard')  # Redirect to citizen dashboard
    else:
        form = CitizenSignupForm()  # Initialize the form for GET request
    return render(request, 'csignup.html', {'form': form})

# Agency Signup View
def asignup(request):
    if request.method == 'POST':
        form = AgencySignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            user.is_agency = True  # Mark as an agency
            user.save()  # Save to DB
            login(request, user)  # Log the user in
            return redirect('agency_dashboard')  # Redirect to agency dashboard
    else:
        form = AgencySignupForm()  # Initialize the form for GET request
    return render(request, 'asignup.html', {'form': form})




from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

from .utils import scrape_disaster_data
import os
from django.conf import settings
@login_required
def citizen_dashboard(request):
    disasters = Disaster.objects.all()
    return render(request, 'citizen_dashboard.html', {'disasters': disasters})
@login_required
def agency_dashboard(request):
    # Scrape and save new disaster data before querying the database
    scrape_disaster_data()  # Scrape new disasters and save them to the database
    
    # Fetch the disasters (both scraped and manually added) for the current user (the agency)
    disasters = Disaster.objects.all()
    
    # Generate the map
    disaster_map = generate_disaster_map(disasters)

    map_dir = os.path.join(settings.BASE_DIR, 'static', 'maps')

    # Ensure the directory exists
    if not os.path.exists(map_dir):
        os.makedirs(map_dir)

    # Define the full file path for the map
    map_path = os.path.join(map_dir, 'disaster_map.html')
    disaster_map.save(map_path)

    # Get cluster centers
    #clusters = cluster_disaster_locations(disasters)
    clusters = list(cluster_disaster_locations(disasters))
    return render(request, "agency_dashboard.html", {
        "disasters": disasters,  # Pass disasters to the dashboard
        "map_path": map_path,    # Pass map path to the template
        "clusters": clusters     # Pass clusters data
    })


@login_required

def add_disaster(request):
    if request.method == "POST":
        form = DisasterForm(request.POST)
        if form.is_valid():
            disaster = form.save(commit=False)
            disaster.created_by = request.user
            disaster.save()
            return redirect("agency_dashboard")
    else:
        form = DisasterForm()
    return render(request, "add_disaster.html", {"form": form})    



def scrape_and_update_disasters(request):
    scrape_disaster_data()
    return redirect("disaster_dashboard")  # Redirect to the dashboard

def disaster_dashboard(request):
    disasters = Disaster.objects.all()
    return render(request, "dashboard.html", {"disasters": disasters})

def filter_disasters_by_date(request, date):
    disasters = Disaster.objects.filter(date=date)
    return render(request, "disasters_by_date.html", {"disasters": disasters, "date": date})


from .models import Disaster
from .geospatial import generate_disaster_map, cluster_disaster_locations

def disaster_map_view(request):
    # Fetch all disasters
    disasters = Disaster.objects.all()

    # Generate the map
    disaster_map = generate_disaster_map(disasters)

    # Save the map to an HTML file
    map_path = "static/maps/disaster_map.html"
    disaster_map.save(map_path)

    # Get cluster centers
    clusters = cluster_disaster_locations(disasters)

    return render(request, "disaster_map.html", {
        "map_path": map_path,
        "clusters": clusters
    })












