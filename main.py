import requests
from datetime import datetime, timedelta
from requests.structures import CaseInsensitiveDict


# create loop to request input of desired location to play golf
# determine whether or not it is something that will be found within geoapify
while True:
    try:
        initial = input('What is the address of your desired course\n')
        address = ''
        for i in initial:
            if i == ' ':
                address += '%20'
            elif i == ',':
                address += '%2C'
            else:
                address += i

        url = "https://api.geoapify.com/v1/geocode/search?text={0}&apiKey=452f8d1b052c49e2b18ed1d000ba5017".format(address)

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        lat_lon = requests.get(url, headers=headers)
        lat_lon = lat_lon.json()
        if len(lat_lon['features']) < 1:
            print('That is not a location we can find in our system')
            raise ValueError
        break
    except:
        print('please enter a valid address\n')


# determine what the offset time is compared so we are able to accurately represent the locations time
offset = lat_lon['features'][0]['properties']['timezone']['offset_DST']
hours_diff = ''
if offset[0] == '-':
    hours_diff += offset[0]
    if offset[1] != 0:
        hours_diff += offset[1]
    hours_diff += offset[2]
else:
    if offset[0] != 0:
        hours_diff += offset[0]
    hours_diff += offset[1]
hours_diff = int(hours_diff) + 4


# surface data of latitude and longitude
longitude = lat_lon['features'][0]['properties']['lon']
latitude = lat_lon['features'][0]['properties']['lat']


# run openweather api and jsonify data
weather_key = 'f557fd02f45c8e7873127cb3211b299e'
weather = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'.format(latitude, longitude, weather_key))
result = weather.json()



# create variable describing the time of sunset using result from openweather and offset time difference
# print result to confirm to use the location as well and sunset time
dt = (datetime.fromtimestamp(result['sys']['sunset']) + timedelta(hours=hours_diff, minutes=0)).time()
print('The location you submitted is -- ' + result['name'] + ', ' + result['sys']['country'])
print(dt)


# calculate how many holes of golf we can get in on a given night