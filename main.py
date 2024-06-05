import requests
import datetime
from requests.structures import CaseInsensitiveDict


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


longitude = lat_lon['features'][0]['properties']['lon']
latitude = lat_lon['features'][0]['properties']['lat']


weather_key = 'f557fd02f45c8e7873127cb3211b299e'

weather = requests.get('https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}'.format(latitude, longitude, weather_key))
result = weather.json()

dt = datetime.datetime.fromtimestamp(result['sys']['sunset']).time()

print(result['name'] + ', ' + result['sys']['country'])
print(dt)


# need to be able to access input so you can find exact latitude and longitude here (look up on google potential api)
# need to be able to figure out why the time thing isnt work
# turn time into a useable format based on location
# calculate how many holes of golf we can get in on a given night