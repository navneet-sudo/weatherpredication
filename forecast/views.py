import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Import the custom form
from .forms import CityForm
from django.contrib.auth.decorators import login_required

# Function to get the location name using reverse geocoding (Nominatim API)
def get_location_name(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url)
        location_data = response.json()
        return location_data.get('display_name', 'Unknown location')
    except Exception as e:
        return 'Error fetching location'

# View for handling user sign-up
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form here
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful sign-up
            return redirect('weather_view')  # Redirect to your weather page after signup
    else:
        form = CustomUserCreationForm()  # Use the custom form here

    return render(request, 'registration/signup.html', {'form': form})

# View for handling weather logic
@login_required
def weather_view(request):
    weather_data = None
    news_data = None
    alert_message = ''
    background_class = 'default'
    map_data = None
    location_name = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            # Fetch weather data using coordinates
            api_key = 'c347dff8c8922b1f14b361c4acf8efb9'
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
            response = requests.get(url)
            data = response.json()

            if data.get('cod') == 200:
                weather_data = {
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'main': data['weather'][0]['main'],
                }
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                map_data = {'lat': lat, 'lon': lon}

                # Fetch the location name using reverse geocoding
                location_name = get_location_name(lat, lon)

                # Set weather alerts
                weather_condition = data['weather'][0]['main']
                background_class, alert_message = set_weather_alerts(weather_condition)

        elif 'get_weather' in request.POST:
            if form.is_valid():
                city = form.cleaned_data['city']
                api_key = 'c347dff8c8922b1f14b361c4acf8efb9'
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
                response = requests.get(url)
                data = response.json()

                if data.get('cod') == 200:
                    weather_data = {
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'main': data['weather'][0]['main'],
                    }
                    lat = data['coord']['lat']
                    lon = data['coord']['lon']
                    map_data = {'lat': lat, 'lon': lon}

                    # Fetch the location name using reverse geocoding
                    location_name = get_location_name(lat, lon)

                    # Set weather alerts
                    weather_condition = data['weather'][0]['main']
                    background_class, alert_message = set_weather_alerts(weather_condition)
            else:
                alert_message = '❌ City not found. Please enter a valid city.'
    else:
        form = CityForm()

    return render(request, 'forecast/weather.html', {
        'form': form,
        'weather_data': weather_data,
        'news_data': news_data,
        'alert_message': alert_message,
        'background_class': background_class,
        'map_data': map_data,
        'location_name': location_name  # Add location name to context
    })

# Helper function to set background classes and weather alerts
def set_weather_alerts(weather_condition):
    background_class = 'default'
    alert_message = ''

    if weather_condition == 'Thunderstorm':
        alert_message = '⚠ Thunderstorm Alert! Stay indoors and avoid outdoor activities.'
        background_class = 'thunderstorm'
    elif weather_condition == 'Rain':
        alert_message = '🌧 Rain Alert! Carry an umbrella.'
        background_class = 'rain'
    elif weather_condition == 'Clear':
        alert_message = '☀ Clear Skies. Enjoy your day!'
        background_class = 'clear'
    elif weather_condition == 'Clouds':
        alert_message = '☁ Cloudy skies. It might be gloomy.'
        background_class = 'clouds'
    elif weather_condition == 'Snow':
        alert_message = '❄ Snowfall Alert! Stay warm and drive carefully.'
        background_class = 'snow'
    elif weather_condition == 'Drizzle':
        alert_message = '🌦 Light Drizzle. It might get wet.'
        background_class = 'drizzle'
    elif weather_condition == 'Fog':
        alert_message = '🌫 Fog Alert! Drive with caution.'
        background_class = 'fog'
    elif weather_condition == 'Mist':
        alert_message = '🌫 Misty Conditions. Be careful outdoors.'
        background_class = 'mist'
    elif weather_condition == 'Smoke':
        alert_message = '🔥 Smoke Alert! Stay indoors to avoid inhalation.'
        background_class = 'smoke'
    elif weather_condition == 'Haze':
        alert_message = '🌫 Hazy conditions. It might affect visibility.'
        background_class = 'haze'
    elif weather_condition == 'Overcast':
        alert_message = '☁ Overcast Clouds. It might be dull today.'
        background_class = 'overcast'
    elif weather_condition == 'Scattered clouds':
        alert_message = ' 🌤 Scattered Clouds. Partly cloudy, but still sunny!'
        background_class = 'scattered'
    else:
        alert_message = '🌍 Weather: ' + weather_condition
        background_class = 'default'

    return background_class, alert_message
