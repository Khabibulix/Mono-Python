from tkinter import Tk, Button, Label, Frame, Text
from Book_Chooser import Book_Chooser

bc = Book_Chooser()
bc.choosing_from_list()

class Application(Tk):
    def __init__(self):
        super().__init__()

        #Bottom frame
        bottom_container = Frame(self, width=900, height=100, borderwidth=5, relief="groove")
        bottom_container.place(x=0, y=140)

        text_for_result = Text(bottom_container, height=1, width=86)
        text_for_result.pack(expand=True)
        text_for_result.config(state='normal')


        text_box_for_url = Text(bottom_container, height=1, width=86)
        text_box_for_url.pack(expand=True)
        text_box_for_url.config(state='normal')

        # Top Frame
        top_container = Frame(self, width=700, height=100, borderwidth=5, relief="groove")
        top_container.place(x=0, y=0)

        label = Label(top_container, text="Let's randomize the next book I'll read -->")
        label.place(x=80, y=25)

        button = Button(top_container, text="Generate!",fg="black", bg="lightblue")
        button.place(x=320, y=23)

        button_delete = Button(top_container, text="Delete!", fg="black", bg="lightblue")
        button_delete.place(x=500, y=23)

        #Function Keybinding

        def delete_all():
            text_for_result.delete("1.0", "end")
            text_box_for_url.delete("1.0", "end")


        #Keybindings

        button.bind('<Button-1>', lambda event:
        text_for_result.insert("end", bc.choosing_book_and_preparing_for_output(),
        text_box_for_url.insert("end", bc.printing_price_informations_about_book()))
                    )

        button_delete.bind('<Button-1>', lambda event:delete_all())

        self.geometry("500x200")
        self.title("Book Randomizer")
        self.resizable(False,False)