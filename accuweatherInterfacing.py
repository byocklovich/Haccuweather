import requests
import json
import os
import socket
import datetime
import random

#https://developer.accuweather.com/apis
def findCoords():
    position_url = 'http://freegeoip.net/json'
    try:
        r = requests.get(position_url)
    except:
        return -1
        
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    location = str(lat) + ',' + str(lon)
    return location
    
#37.4192,-122.0574
def getLatLong(address):
    latLongResponse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCqZ57fGEK_jDqxBqn8VuDpGBZvGRVa-KY" %address).json()
    lat = latLongResponse['results'][0]['geometry']['location']['lat']
    lon = latLongResponse['results'][0]['geometry']['location']['lng']
    return str(lat) + ',' + str(lon)

def getKeys(locations):
    my_keys = []
    for date in locations:
        date_keys = []
        for location in date:
            if location == -1:
                return -1
            area_response = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=HackPSU2017&q=%s&details=true&toplevel=true' %location)
            date_keys.append( area_response.json()['Key'] )
        my_keys.append(date_keys)
    return my_keys
    
def getApparelTemp(temp):
    if temp < 40:
        return "Winter Apparel"
    elif temp > 40 and temp <= 55:
        return "Fall/Spring Apparel"
    else:
        return "Summer Apparel"
        
def getApparelWeather(weatherType):
    weatherType = weatherType.lower()
    randNum = int(random.random()*10000)
    if ("sunny" in weatherType) or ("sunshine" in weatherType) or ("hot" in weatherType):
        reList = [
                "It will be sunny for this event, consider bringing sunglasses or a hat if you are outside.", 
                "It will be hot at this event. Sunglasses might be useful if this event is outside!"
            ]
        num = randNum % len(reList)
        return reList[num]
    elif ("rain" in weatherType) or ("showers" in weatherType) or ("storm" in weatherType):
        reList = [
                "Rain is forecasted for this event. Consider bringing an umbrella or rain coat.", 
                "It might be rain at this event. Plan to bring a rain coat or umbrella.", 
                "It's forecasted to storm during this event. Bringing a rain coat or umbrella might be a good idea."
            ]
        num = randNum % len(reList)
        return reList[num]
    elif ("fog" in weatherType):
        reList = [
                "It's going to be foggy for this event. Be careful if you're driving!", 
                "It'll be foggy for this event, make sure you turn your headlights on if you're driving!"
            ]
        num = randNum % len(reList)
        return reList[num]
    elif ("cloud" in weatherType):
        reList = [
                "Clouds are forecasted for this event.", 
                "It's forecasted to be overcast for this event."
            ]
        num = randNum % len(reList)
        return reList[num]
    elif ("snow" in weatherType) or ("flurries" in weatherType) or ("cold" in weatherType):
        reList = [
                "It will be cold for this event. Wear a warm coat.", 
                "It will be chilly. If this event is outside, bundle up!"
            ]
        num = randNum % len(reList)
        return reList[num]
    elif ("ice" in weatherType) or ("sleet" in weatherType) or ("freezing" in weatherType):
        reList = [
                "It's an icy day, be careful traveling!", 
                "Roads may be dangerous!"
            ]
        num = randNum % len(reList)
        return reList[num]
    else:
        return ''
    
def getTemperature(keys):
    day_weather = []
    index = 0
    for date in keys:
        key_weather = []
        for key in date:
            weatherJSON = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/15day/%s?apikey=HackPSU2017&details=true&metric=false' %key)
            day = weatherJSON.json()['DailyForecasts'][index]
            avg_temp = ( day['Temperature']['Minimum']['Value'] + day['Temperature']['Maximum']['Value'] )/2
            key_weather.append(avg_temp)
        day_weather.append(key_weather)
    return day_weather
    
def getWeatherType(keys):
    day_weather_type = []
    index = 0
    for date in keys:
        key_weather = []
        for key in date:
            weatherJSON = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/15day/%s?apikey=HackPSU2017&details=false&metric=false' %key)
            day = weatherJSON.json()['DailyForecasts'][index]
            weather_type_day = (day['Day']['IconPhrase'])
            weather_type_night = (day['Night']['IconPhrase'])
            key_weather.append([weather_type_day, weather_type_night])
        day_weather_type.append(key_weather)
    return day_weather_type

def output():
    my_output = ''
    events = [[['127 S Fraser St, State College, PA 16801, USA', 'morning shopping', '21'], ['Miami Beach, FL, USA', 'Soccer Practice', '7']], [['Los Angeles, CA, USA', 'Ballet Practice', '12'], ['Burke Center 242, 5101 Jordan Rd', 'really long class', '12']]]
    locations = []
    for day in events:
        day_events = []
        for event in day:
            if event[0] == 'cur':
                day_events.append(findCoords())
            else:
                day_events.append(getLatLong(event[0]))
        locations.append(day_events)
            
    my_keys = getKeys(locations)
    my_temps = getTemperature(my_keys)
    my_types = getWeatherType(my_keys)
    print(my_types)
    today = datetime.datetime.now().date()

    for i in range( len(events) ):
        day = today + datetime.timedelta(days=i)
        my_output += ('Events on ' + str(day) + ':\n')
        for n in range( len(events[i] ) ):
            my_output += ( '\t' + events[i][n][1] + ' at ' + events[i][n][0] + ':\n' )
            my_output += ( '\t\t' + str(my_temps[i][n]) + 'F ' + getApparelTemp(my_temps[i][n]) + '\n')
            if int(events[i][n][2]) >= 21 or int(events[i][n][2]) <= 7:
                my_output += ( '\t\t' + getApparelWeather(my_types[i][n][1]) + '\n')
            else:
                my_output += ( '\t\t' + getApparelWeather(my_types[i][n][0]) + '\n')
    return my_output
                
if __name__ == '__main__':
    print(output())
