from tkinter import *
from tkinter import filedialog, messagebox
from kinopoisk_api import KP
import os.path
import os
import pytils.translit
import threading


class Searcher:
    '''Class working with KinopoiskAPI
    '''

    def __init__(self):
        # finnaly created for App (Film searcher)
        self.dict_films = {}

    # button "choose directory" logic
    def btn_get_path(self, tkinter):
        
        direction_main_path = filedialog.askdirectory()            
        
        tkinter.entry.delete(0, END)
        tkinter.entry.insert(0, direction_main_path)

    def message_search(self):
        self.top = Toplevel(height=80, width=200)
        self.m = Message(self.top, text='Подождите. Выполняется поиск...')
        self.m.place(x=60, y=13)
        # self.m.pack()

    def check_thread(self,tkinter, thread):
            if thread.is_alive():
                tkinter.after(100, lambda: self.check_thread(tkinter, thread))
            else:
                tkinter.button_search.config(state=NORMAL)

    # button 'ПОИСК' logic
    def btn_search(self, tkinter):
        # get path from entry
        entry_path = tkinter.entry.get()

        try:
            self.dir_list = os.listdir(entry_path)

        except FileNotFoundError:
            messagebox.showwarning('Warning', 'Выберите путь')
            self.btn_get_path(tkinter)


        tkinter.button_search.config(state=DISABLED)

        thread = threading.Thread(target=lambda: self.logic(tkinter))
        print(threading.main_thread().name)
        print(thread.name)
        thread.start()
        self.check_thread(tkinter, thread)

        

        # self.message_search()
    def logic(self, tkinter):
        
        film_list = []
        # sorting dir_list by video format extensions and filling film_list
        for file in self.dir_list:
            if '.mkv' in file or '.avi' in file or '.mp4' in file or '.mpg' in file or '.mov' in file or '.mpeg4' in file or '.flv' in file or '.vob' in file or '.wmv' in file:
                film_list.append(file)

        self.message_search()

        # return films in format: filmname_year
        def text_reader(text):
            string_1 = ''
            num_str = ''
            for i in text:    
                if i.isnumeric() == True:
                    # variable for counting digits in string
                    num_str += i
                    string_1 += i
                    # when num_str == 4 it is a year of a film, breaking cycle
                    if len(num_str) == 4 and num_str.startswith('20') or len(num_str) == 4 and num_str.startswith('19'):
                        break
                # means that digits before not a year
                elif i.isnumeric() == False and len(num_str) > 0:
                    num_str = ''
                    string_1 += i

                else:
                    string_1 += i

            formated_str = string_1.replace('.', ' ').replace('(', '').replace(')', '').replace('_', ' ').replace('[', '').replace(']', '')
            return formated_str

        

        self.film_list_form = []
        # filling film_list_form with films
        for string in film_list:
            self.film_list_form.append(text_reader(string))


        def detranslify(text):
            detrans_text = pytils.translit.detranslify(text)
            return detrans_text

        # TOKEN
        kinopoisk = KP(token='34c5c2a6-5e2e-4005-aba5-575c848fe1a7')

        # working with KinopoiskAPI
        # @task
        def searchKP(film):
            search = kinopoisk.search(film)
            string_search = ''
            # fill string_search
            for item in search:
                string_search += str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n' + '\n'
                string_search_formated_1 = string_search.replace('null', '0.0')
            
            # result < 5 is empty
            if len(string_search) < 5:
                # using detranslify text for another turn of request to KinopoiskAPI
                search = kinopoisk.search(detranslify(film)) 
                string_search_2 = ''
                for item in search:
                    string_search_2 += str(item.ru_name) + ' ' + str(item.year) + ' ' + str(item.kp_rate) + '\n' + ', '.join(item.genres) + '\n' + '\n'
                    string_search_formated_2 = string_search_2.replace('null', '0.0')
                # if normal and detranslify requests have no data
                if len(string_search) < 5:
                    return 'Нет результата поиска'
                else:
                    return string_search_formated_2
            else:
                return string_search_formated_1

        
        # self.m = Message(tkinter, text='111123', relief = RAISED)
        # self.m.place(x=100, y=20)

        # list of answers for films from KinopoiskAPI
        total_answer = []
        # call searchKP and fill total_answer
        for film in self.film_list_form:
            answer = searchKP(film)
            total_answer.append(answer)

        # create dictionary of films
        self.dict_films = dict(zip(self.film_list_form, total_answer))
        # turn on function than create buttons from self.dict_film
        tkinter.make_film_btns()
        self.top.destroy()
        messagebox.showinfo('Info', 'Поиск выполнен!')

    # film buttons operation
    def btn_films(self, tkinter, key):

        text_for_area = self.dict_films[key]

        tkinter.text_area.delete('1.0', END)
        tkinter.text_area.insert('1.0', text_for_area)

        # reset bg color of buttons to default
        btn_index = self.film_list_form.index(key)
        
        for button in (tkinter.buttons[:btn_index] + tkinter.buttons[btn_index:]):
            button.config(bg='SystemButtonFace')
        
        # set bg color to clicked button
        tkinter.buttons[btn_index].config(bg='#C0C0C0')
        