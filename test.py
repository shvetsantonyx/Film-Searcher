import requests
import json

# url = 'https://kinopoiskapiunofficial.tech/documentation/api/#/films/get_api_v2_1_films_search_by_keyword'

# params = {
#     'keyword': 'матрица',
#     'pagesCount': 1,
#     'searchFilmsCountResult': 1,
#     'films': ''
# }

# r = requests.get(url, params=params)
# print(r.status_code)

# a = r.text
from kinopoisk_api import KP

kinopoisk = KP(token='34c5c2a6-5e2e-4005-aba5-575c848fe1a7')

search = kinopoisk.search('Delicieux 2021')
#print(search)
string_search = ''

films = ['Green Mile', 'Терминатор']


for item in search:
    # print(item.ru_name, item.year, item.kp_rate)
    # print(", ".join(item.genres))
    # print()

    string_search = str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n'
    print(string_search)
if len(string_search) < 5:
    print('none')
else:
    print('ok')
    # print(", ".join(item.countries))


