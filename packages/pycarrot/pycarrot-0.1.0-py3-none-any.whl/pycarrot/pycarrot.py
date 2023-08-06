import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter.scrolledtext as ts 
import tkinter.messagebox as mb
from PIL import Image, ImageTk


class Layout(tk.Tk):
    def __init__(self):

        super().__init__()

        self.__title = "carrot app"
        self.__icon = "carrot-icon.ico"
        self.__width = int(self.winfo_screenwidth())
        self.__height = int(self.winfo_screenheight())
        self.__close_message = "Kill carrot?"
        
        self.geometry(f"{self.__width}x{self.__height}")
        self.title(self.__title)
        self.attributes("-topmost", True) # Put the layout at the top of any window
        self.iconbitmap(self.__icon)

        # Layout protocols
        self.protocol("WM_DELETE_WINDOW", self.close_layout)

    def set_title(self, title):
        self.__title = title
        self.title(self.__title)

    def get_title(self):
        return self.__title

    def set_icon(self, icon):
        self.__icon = icon

    def get_icon(self):
        return self.__icon

    def set_dimensions(self, width, height):
        self.__width = width
        self.__height = height
        self.geometry(f"{self.__width}x{self.__height}")

    def get_dimensions(self):
        return self.__width, self.__height

    def close_layout(self):
        if mb.askokcancel(message=self.__close_message, title=self.__title):
            self.destroy()

    def put_it_all_together(self):
        self.mainloop()

class Carrot(tk.Canvas):
    def __init__(self, layout):

        self.__layout = layout
        self.__bkg = "default-bkg.png"
        self.__width, self.__height = layout.get_dimensions()
        self.__border_width = 1

        super().__init__(self.__layout, width = self.__width, height = self.__height)

        self.smallFont = tkFont.Font(family="Open Sans", size=8)
        self.mediumFont = tkFont.Font(family="Open Sans", size=12)
        self.bigFont = tkFont.Font(family="Open Sans Semibold", size=25)

        self.bkg = Image.open(self.__bkg)
        self.bkg = self.bkg.resize((self.__width, self.__height))
        self.img = ImageTk.PhotoImage(self.bkg)
        self.create_image(0, 0, anchor = tk.NW, image=self.img)
        self.spawn_carrot()
        

    def set_bkg(self, bkg):
        self.__bkg = bkg
        self.bkg = Image.open(self.__bkg)
        self.bkg = self.bkg.resize((self.__width, self.__height))
        self.img = ImageTk.PhotoImage(self.bkg)
        self.create_image(0, 0, anchor = tk.NW, image=self.img)

    
    def get_bkg(self):
        return self.__bkg

    def set_border_width(self, border_width):
        self.__border_width = border_width
        self.spawn_carrot()
    
    def get_border_width(self):
        return self.__border_width
    
    def add_widget(self, widget, x, y):
        self.create_window(x, y, anchor=tk.CENTER, window=widget)
        return widget
    
    def add_styled_button(self, text, anchor, bcolor, fcolor, w, h, bd, style, command, x, y):
        h = self.add_widget(tk.Button(self, 
                                text = text, 
                                anchor = anchor,
                                bg = bcolor,
                                foreground = fcolor,
                                width = w,
                                height = h,
                                bd = bd,
                                font = style,
                                command = command), x, y)
        
        self.spawn_carrot()

    def add_text(self, content, anchor, style, fcolor, x, y):
        self.create_text(x,y, fill=fcolor,
                                    text=content,
                                    justify = anchor,
                                    font = style)
        self.spawn_carrot()
    #def add_text_box(self, )

    def add_button(self, text, command, x, y):
        u = self.add_widget(ttk.Button(self,    text = text,
                                                command = command,
                                                takefocus=False), x, y)

    def go_page(self, new_page):
        self.forget()
        new_page.spawn_carrot()
        

    def spawn_carrot(self):
        self.pack()



