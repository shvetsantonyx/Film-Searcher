import os
import pytils.translit
from kinopoisk_api import KP


kinopoisk = KP(token='34c5c2a6-5e2e-4005-aba5-575c848fe1a7')


dir_list = os.listdir(r'C:\Users\SAI\Python_Scr\Kinopoisk\KinoPoiskAPI\test')

print(dir_list)

film_list = []
# sorting dir_list and filling film_list
for file in dir_list:
    if '.mkv' in file or '.avi' in file or '.mp4' in file or '.mpg' in file or '.mov' in file or '.mpeg4' in file or '.flv' in file or '.vob' in file or '.wmv' in file:
    # if file in ('.mkv', '.avi', '.mp4', 'mpg', '.mov', 'mpeg4', '.flv', '.vob', '.wmv'):
        film_list.append(file)

print(film_list)



# return films in format: film_name_year
def text_reader(text):
    string_1 = ''
    num_str = ''
    for i in text:    
        if i.isnumeric() == True:
            num_str += i
            string_1 += i
            if len(num_str) == 4 and num_str.startswith('20') or len(num_str) == 4 and num_str.startswith('19'):
                break
        else:
            string_1 += i
    new_str = string_1.replace('.', ' ').replace('(', '')
    return new_str


film_list_form = []
# filling film_list_form with films
for string in film_list:
    film_list_form.append(text_reader(string))

print(film_list_form)


def detranslify(text):
    detrans_text = pytils.translit.detranslify(text)
    return detrans_text


# text_trans = []

# for i in film_list:
#     text_trans.append(detranslify(i))

# print(text_trans)

# search = kinopoisk.search('Малышка')

def searchKP(film):
    search = kinopoisk.search(film)
    string_search = ''
    for item in search:
        string_search += str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n' +'\n'
    
    if len(string_search) < 5:
        search = kinopoisk.search(detranslify(film))
        string_search = ''
        for item in search:
            string_search += str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n' +'\n'
        if len(string_search) < 5:
            return 'Нет результата поиска \n\n'
        else:
            return string_search
        # return 'Нет результата поиска \n\n'
    else:
        return string_search



# print(searchKP('Малышка'))

# for film in film_list:
#     search = kinopoisk.search(film)
#     for item in search:
#         string_search = str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n'

# answer = ''
total_answer = []

for film in film_list_form[3:5]:
    answer = searchKP(film)
    total_answer.append(answer)

# print(total_answer)

for i in total_answer:
    print(i)
