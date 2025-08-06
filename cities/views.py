from django.shortcuts import render, redirect
import requests
import datetime
from django.contrib import messages
from .models import Weather

def weather_view(request):
    weather_data = {}
    forecast_data = []

    # Use default city if no input
    city = request.GET.get('city', 'Lagos')
    api_key = 'c009dd7b4d6b9e5ec024aa5f31902902'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    try:
        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        if weather_response.status_code == 200:
            data = weather_response.json()
            weather_data = {
                'city': city.title(),
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'date': datetime.datetime.now().strftime('%A, %b %d | %I:%M %p')
            }

            # Save to DB
            Weather.objects.create(
                city=weather_data['city'],
                temperature=weather_data['temperature'],
                description=weather_data['description'],
                icon=weather_data['icon'],
                humidity=weather_data['humidity'],
                wind=weather_data['wind']
            )

        else:
            messages.error(request, 'City not found. Please try again.')
            
        if forecast_response.status_code == 200:
            data = forecast_response.json()
            daily_forecasts = {}
            for entry in data['list']:
                date = entry['dt_txt'].split()[0]
                time = entry['dt_txt'].split()[1]
                if time == "12:00:00":  # Pick forecast for midday
                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            'day': datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%a"),
                            'temp': int(entry['main']['temp']),
                            'icon': entry['weather'][0]['icon']
                        }
            # Get only the next 5 days
            forecast_data = list(daily_forecasts.values())[:5]

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")

    return render(request, 'cities/weather.html', {
        'weather': weather_data,
        'forecast': forecast_data
    })
