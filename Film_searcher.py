from tkinter import *
from searcher_logic import Searcher
from vertical_scrolling_frame import VerticalScrollingFrame
import os
import sys


class App(Tk):
    ''' Main application.'''

    def __init__(self):

        self.searcher_obj = Searcher()

        Tk.__init__(self)

        self.title('Film Searcher')
        self.geometry('1000x640+300+500')
        self.resizable(False, False)
        self.iconbitmap(default=self.resource_path('searching.ico'))

        # start window graphics
        self.set_ui()


    def resource_path(self, relative_path):
        '''Path for icon into App'''    
        try:       
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

  
    def set_ui(self):
        '''Create main window graphics.'''

        self.entry = Entry(self, width=60)
        self.entry.grid(row=1, column=1, padx=10)

        self.button_path = Button(
            self, bg='#DCDCDC', text='Выбрать папку',
            command=lambda: self.searcher_obj.btn_get_path(self)
            )
        self.button_path.grid(row=1, column=0, padx=10, pady=3)

        self.button_search = Button(
            self, bg='#87CEEB', text='ПОИСК',width=20,
            command= lambda: self.searcher_obj.btn_search(self)
            )
        self.button_search.grid(row=1, column=2, sticky=W, padx=3, pady=3)

        self.text_frame = Frame(self, width=60, height=37)
        self.text_frame.grid(row=3, column=2, rowspan=25, columnspan=3, padx=2, pady=3)

        self.text_area = Text(self.text_frame, width=68, height=37, font='Tahoma 10')
        self.text_area.pack(fill=BOTH, expand=1, side=LEFT)

        self.scroll_text = Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scroll_text.pack(side=RIGHT, fill=Y)
        self.text_area.config(yscrollcommand=self.scroll_text.set)


    # calls after button 'ПОИСК' is clicked
    def make_film_btns(self):
        '''Create films buttons after click on button "ПОИСК".'''

        self.frame = VerticalScrollingFrame(self)
        self.frame.place(x=9, y=35)

        self.buttons = []
        
        for key in self.searcher_obj.films_dict:
            self.buttons.append(Button(
                self.frame.interior, text=key, width=50,
                command=lambda x=key: self.searcher_obj.btn_films(self, x))
                )
            self.buttons[-1].pack(fill=X)   
          

if __name__ == '__main__':
    root = App()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
