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
dt_og = (datetime.fromtimestamp(result['sys']['sunset']) + timedelta(hours=hours_diff, minutes=0))
dt = dt_og.time()
print('The location you submitted is -- ' + result['name'] + ', ' + result['sys']['country'])
print(dt)


# prompt user for both what their tee time is as well as what their rate of play would be
while True:
    try:
        tee_time = str(input('\nWhat is the tee time you have? ( please use military time format )\n'))
        hours = int(tee_time.split(':')[0])
        if hours < 17 or hours > int(str(dt).split(':')[0]):
            raise ValueError
        pace = float(input('\nHow many hours does it take you to play 9 holes of golf?\n( please enter a number and if applicable, use decimals )\n'))
        break
    except:
        if ValueError:
            print('\nThe time for your tee time is not possible.\nPlease make sure you are using military time and it is not past sunset.')
        else:
            print('please enter an acceptable value for both.\nDid you make sure your rate of play is numeric? ( ex. 2.25 )')


# find the amount of time you have between your tee time and sunset
dt = datetime.strptime(str(dt), '%H:%M:%S')
tee_time = tee_time.split(':')[0] + ':' + tee_time.split(':')[1][:2]
tee_time = datetime.strptime(tee_time, '%H:%M')
diff = dt - tee_time


# convert your datetime to a float value to perform math
times = str(diff).split(':')
h = int(times[0])
m = int(times[1]) / 60
total_time = h+m
rate = pace / 9


# find final valye after dividing by your rate of play and print how many holes
answer = total_time // rate
print('You will get in at least {0} holes in before sunset'.format(answer))

# determine the rate of time that it would take for each hole
# divide difference between tee and sunset time by the per hole rate