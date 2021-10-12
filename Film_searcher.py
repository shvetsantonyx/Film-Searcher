from tkinter import *
from searcher_logic import Searcher
import os
import sys


class VerticalScrollingFrame(Frame):
    """Tkinter scrollable frame"""
    
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscroll = Scrollbar(self, orient=VERTICAL)
        vscroll.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscroll.set, height=600)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscroll.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class App(Tk):
    ''' Main application
    '''

    def __init__(self):

        self.searcher_obj = Searcher()

        Tk.__init__(self)

        self.title('Film Searcher')
        self.geometry('930x650+10+10')
        self.iconbitmap(default=self.resource_path('searching.ico'))

        # starting window graphics
        self.set_ui()

    # path for icon into App
    def resource_path(self, relative_path):    
        try:       
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # create window graphics   
    def set_ui(self):

        self.entry = Entry(self, width=60)
        self.entry.grid(row=1, column=1, padx=10)

        self.button_path = Button(self, bg='#DCDCDC', text='Выбрать папку', command=lambda: self.searcher_obj.btn_get_path(self))
        self.button_path.grid(row=1, column=0, padx=10, pady=3)

        self.button_search = Button(self, bg='#87CEEB', text='ПОИСК', width=20, command= lambda: self.searcher_obj.btn_search(self))
        self.button_search.grid(row=1, column=2, sticky=W, padx=3, pady=3)

        self.text_frame = Frame(self, width=50, height=37)
        self.text_frame.grid(row=3, column=2, rowspan=25, columnspan=3, padx=2, pady=3)

        self.text_area = Text(self.text_frame, width=58, height=37, font='Tahoma 10')
        self.text_area.pack(fill=BOTH, expand=1, side=LEFT)

        self.scroll_text = Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scroll_text.pack(side=RIGHT, fill=Y)
        self.text_area.config(yscrollcommand=self.scroll_text.set)
       

    # this func calls after button 'ПОИСК' is clicked
    def make_film_btns(self):

        self.frame = VerticalScrollingFrame(self)
        self.frame.place(x=8, y=35)

        self.buttons = []
        
        for key in self.searcher_obj.films_dict:
            button = Button(self.frame.interior, text=key, width=55, command=lambda x=key: self.searcher_obj.btn_films(self, x))
            self.buttons.append(button)
            button.pack(fill=X)     
          

if __name__ == '__main__':
    root = App()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
