import sys
from io import BytesIO

import requests
from PIL import Image

apikey = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
map_api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
search_api_server = 'https://search-maps.yandex.ru/v1/'

# geocoder
toponym_to_find = " ".join(sys.argv[1:])
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print(response.status_code, response.reason)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coordinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")

# search
address_ll = f"{toponym_longitude},{toponym_lattitude}"

search_params = {
    "apikey": apikey,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print(response.status_code, response.reason)
    quit()
js = response.json()
points = []
for i in range(10):
    org = js['features'][i]
    p = f"{org['geometry']['coordinates'][0]},{org['geometry']['coordinates'][1]},"
    if 'круглосуточно' in org['properties']['CompanyMetaData']['Hours']['text']:
        p += f"pm2gnm{i + 1}"
    elif '–' in org['properties']['CompanyMetaData']['Hours']['text']:
        p += f'pm2lbm{i + 1}'
    else:
        p += f'pm2grm{i + 1}'
    points.append(p)
# map
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "l": "map",
    "pt": f'{toponym_longitude},{toponym_lattitude},comma~{"~".join(points)}'
}
response = requests.get(map_api_server, params=map_params)
Image.open(
    BytesIO(response.content)
).show()
