from tkinter import *
from tkinter import filedialog, messagebox
from kinopoisk_api import KP
import os.path
import os
import pytils.translit
import threading


class Searcher:
    '''Class working with KinopoiskAPI.
    '''

    def btn_get_path(self, tkinter):
        '''Button "choose directory" logic.'''
        direction_main_path = filedialog.askdirectory()            
        
        tkinter.entry.delete(0, END)
        tkinter.entry.insert(0, direction_main_path)

    def message_search(self, tkinter):
        '''Message for button "ПОИСК."'''
        self.top = Toplevel(tkinter, height=80, width=200)
        self.top.eval('tk::PlaceWindow . center')
        self.m = Message(self.top, text='Подождите. Выполняется поиск...')
        # self.m.place(x=60, y=13)
        # self.m.pack()
        # self.m.eval('tk::PlaceWindow . center')

    def check_thread(self, tkinter, thread):
        '''Return buttons "ПОИСК", "Выбрать путь" to NORMAL state.'''
        if thread.is_alive():
            tkinter.after(100, lambda: self.check_thread(tkinter, thread))
        else:
            tkinter.button_search.config(state=NORMAL)
            tkinter.button_path.config(state=NORMAL)

    def btn_search(self, tkinter):
        '''Button 'ПОИСК' logic.'''
        # get path from entry
        entry_path = tkinter.entry.get()

        try:
            dir_generator = os.walk(entry_path)
            # get list of files in generator
            film_list_not_ready = next(dir_generator)

            # fill with films
            self.film_list_ready = []
            # len > 2 is that root directory have subfolders and files 
            if len(film_list_not_ready) > 2:
                for file in film_list_not_ready[1]:
                    self.film_list_ready.append(file)
                for file in film_list_not_ready[2]:
                    # checkout for video formats
                    if '.mkv' in file or '.avi' in file or '.mp4' in file or '.mpg' in file or '.mov' in file or '.mpeg4' in file or '.flv' in file or '.vob' in file or '.wmv' in file:
                        self.film_list_ready.append(file)

            # len < 2 is that root directory have only files
            else:
                for file in film_list_not_ready:
                    # checkout for video formats
                    if '.mkv' in file or '.avi' in file or '.mp4' in file or '.mpg' in file or '.mov' in file or '.mpeg4' in file or '.flv' in file or '.vob' in file or '.wmv' in file:
                        self.film_list_ready.append(file)

        except FileNotFoundError:
            messagebox.showwarning('Warning', 'Выберите путь')
            self.btn_get_path(tkinter)

        # disable buttons "ПОИСК", "Выбрать путь" for searching operations
        tkinter.button_search.config(state=DISABLED)
        tkinter.button_path.config(state=DISABLED)

        # starting function "logic" in other thread
        thread = threading.Thread(target=lambda: self.logic(tkinter))
        print(threading.main_thread().name)
        print(thread.name)
        thread.start()
        self.check_thread(tkinter, thread)

        
    def logic(self, tkinter):
        '''Search logic.'''
        # call message
        self.message_search(tkinter)

        # return films in format: filmname_year
        def text_reader(text):
            text_string = ''
            num_string = ''
            for i in text:    
                if i.isnumeric() == True:
                    # variable for counting digits in string
                    num_string += i
                    text_string += i
                    # when num_str == 4 it is a year of a film, breaking cycle
                    if len(num_string) == 4 and num_string.startswith('20') or len(num_string) == 4 and num_string.startswith('19'):
                        break
                # means that digits before not a year
                elif i.isnumeric() == False and len(num_string) > 0:
                    num_string = ''
                    text_string += i

                else:
                    text_string += i
            # replace unnessesary symbols
            formated_string = text_string.replace('.', ' ').replace('(', '').replace(')', '').replace('_', ' ').replace('[', '').replace(']', '')
            return formated_string

        
        self.film_list_ready_formated = []
        # filling film_list_ready_formated with films
        for string in self.film_list_ready:
            self.film_list_ready_formated.append(text_reader(string))

        # create dictionary of films with None values
        self.films_dict = {}
        for film in self.film_list_ready_formated:
            self.films_dict[film] = None

        def detranslify(text):
            '''Detranslify text.'''
            detrans_text = pytils.translit.detranslify(text)
            return detrans_text

        # TOKEN
        kinopoisk = KP(token='34c5c2a6-5e2e-4005-aba5-575c848fe1a7')

        def searchKP(film):
            '''Working with KinopoiskAPI.'''
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
                    # return 'Нет результата поиска'
                    self.films_dict[film] = 'Нет результата поиска'
                else:
                    # return string_search_formated_2
                    self.films_dict[film] = string_search_formated_2
            else:
                # return string_search_formated_1
                self.films_dict[film] = string_search_formated_1


        # list of threads for searchKP
        threads = []
        
        # call searchKP in multythreads mode
        for film in self.films_dict:
            threads.append(threading.Thread(target=lambda x=film: searchKP(x)))
            threads[-1].start()

        # waiting for threads are gone
        for thread in threads:
            thread.join()

        # turn on function than create buttons from self.films_dict
        tkinter.make_film_btns()

        # close message automatically
        self.top.destroy()
        messagebox.showinfo('Info', 'Поиск выполнен!')
        

    def btn_films(self, tkinter, key):
        '''Film buttons operations.'''

        text_for_area = self.films_dict[key]

        # put the text to text_area
        tkinter.text_area.delete('1.0', END)
        tkinter.text_area.insert('1.0', text_for_area)

        # reset bg color of buttons to default
        btn_index = self.film_list_ready_formated.index(key)
        
        for button in (tkinter.buttons[:btn_index] + tkinter.buttons[btn_index:]):
            button.config(bg='SystemButtonFace')
        
        # set bg color to clicked button
        tkinter.buttons[btn_index].config(bg='#C0C0C0')
        