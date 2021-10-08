import requests
import json
import threading
import time
from datetime import timedelta


start_time = time.monotonic()


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

films = ['Green Mile', 'Терминатор', 'Робокоп', 'Snatch', 'Matrix']
films_dict = {}
for film in films:
    films_dict[film] = None
print(films_dict)



def search(film):
    search = kinopoisk.search(film)
    #print(search)
    # string_search = ''

    total_answ = ''


    for item in search:
        # print(item.ru_name, item.year, item.kp_rate)
        # print(", ".join(item.genres))
        # print()

        string_search = str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n'
        print(string_search)
        print(threading.current_thread())
        # print(threads[-1].name)
        total_answ +=string_search
    if len(string_search) < 5:
        print('none')
    else:
        print('ok')
    # print(", ".join(item.countries))
    # answers.append(string_search)
    # print(answers)
    films_dict[film] = total_answ
    # print(films_dict)
    # return string_search

threads = []
answers = []

for film in films:
    # thread = threading.Thread(target=lambda x=film: search(x))
    threads.append(threading.Thread(target=lambda x=film: search(x)))
    threads[-1].start()
    # answers.append(x)
    # print(threading.main_thread().name)
    # print(threading.current_thread())
    # print(threads[-1].name)
    # print(threading.active_count())
    
for i in threads:
    i.join()
    
print(threads)
print(films_dict)

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))
# print(threading.active_count())
# if threading.active_count == 1:
#     print(answers)



# def check_thread(thread):
#             if thread.is_alive():
#                 time.sleep(0.1)
#                 check_thread(thread)
#             else:
#                 pass
                
# for i in threads:
#     print(i.name)
#     i.start()


# films_in_thread = dict(zip(films, threads))
# print(films_in_thread)

# for key in films_in_thread:
#     films_in_thread[key].start()

