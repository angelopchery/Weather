from django.shortcuts import render, redirect
import json
import urllib.request
from .forms import weatherForm
from .models import History

def index(request): 
    # Initialize as an empty dictionary
    current_weather = {}
    
    if request.method == 'POST': 
        form = weatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
  
            source = urllib.request.urlopen( 
                'http://api.openweathermap.org/data/2.5/weather?q=' 
                + city + '&appid=068777b420d46864e2736a1016f31bae').read() 
  
            list_of_data = json.loads(source) 

            # Extracting data from API response
            country_code = list_of_data.get('sys', {}).get('country', '')
            lon = list_of_data.get('coord', {}).get('lon', '')
            lat = list_of_data.get('coord', {}).get('lat', '')
            temp = list_of_data.get('main', {}).get('temp', '')
            pressure = list_of_data.get('main', {}).get('pressure', '')
            humidity = list_of_data.get('main', {}).get('humidity', '')

            # Update current weather dictionary
            current_weather.update({
                'city': str(city),
                'country_code': str(country_code),
                'coordinate': str(f"{lon} {lat}"),
                'temp': str(temp),
                'pressure': str(pressure),
                'humidity': str(humidity)
            })

            # Create a new instance of History model and save it
            history_entry = History.objects.create(
                city=city,
                country_code=country_code,
                coordinate=f"{lon} {lat}",
                temp=temp,
                pressure=pressure,
                humidity=humidity
            )
            history_entry.save()

            # Print current weather for debugging
            print(current_weather)

            # Redirect to avoid form resubmission on page reload
            return redirect('index') 
    else: 
        form = weatherForm() 

    # Fetch historical weather data
    wdata = History.objects.all().order_by('-timestamp')

    context = {
        'form': form,
        'current_weather': current_weather,
        'wdata': wdata
    }
    return render(request, "index.html", context)
