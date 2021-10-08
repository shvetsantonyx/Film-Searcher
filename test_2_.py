from kinopoisk_api import KP
import time
from datetime import timedelta


start_time = time.monotonic()

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
        # print(threading.current_thread())
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

for film in films:
    search(film)

print(films_dict)

end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))