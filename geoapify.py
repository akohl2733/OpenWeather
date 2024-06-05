import requests
from requests.structures import CaseInsensitiveDict

def coordinates():
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

    return longitude, latitude

print(coordinates())