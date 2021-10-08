import os
import pytils.translit
from kinopoisk_api import KP


kinopoisk = KP(token='34c5c2a6-5e2e-4005-aba5-575c848fe1a7')


dir_list = os.listdir(r'C:\Users\SAI\Python_Scr\Film-Searcher\test_4')
dir_dir = os.walk(r'C:\Users\SAI\Python_Scr\Film-Searcher\test_4')
print(type(dir_dir))

for i in dir_dir:
    # print(i)
    film_list_not_ready = i
    break

print(film_list_not_ready)

print(len(film_list_not_ready))
# print()
# print(dir_list)
film_list_ready = []

if len(film_list_not_ready) > 2:
    for i in film_list_not_ready[1]:
        film_list_ready.append(i)
    for i in film_list_not_ready[2]:
        film_list_ready.append(i)
else:
    for i in film_list_not_ready:
        film_list_ready.append(i)

print(film_list_ready)