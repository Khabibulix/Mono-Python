from tkinter import Tk, Button, Label, Frame, Entry
from help import *
from Library import *

library = Library()

OUTPUT_FILE_CONTENT = open('output.txt', 'r').read()
TOTAL_WIDTH_OF_WINDOW = 800
TOTAL_HEIGHT_OF_WINDOW = 400
MARGIN_LEFT = 15
WIDTH_FOR_RIGHT_CONTAINER = 420
# WindowW - LeftContainerW - InitialPlacement * 4
X_POS_FOR_RIGHT_CONTAINER = TOTAL_WIDTH_OF_WINDOW - 320 - 110
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1

class Application(Tk):

    def __init__(self):
        super().__init__()

        #Frames
        left_container = Frame(self, width=320, height=350, borderwidth=2, relief="groove")
        left_container.place(x=MARGIN_LEFT, y=30)

        right_button_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=70, borderwidth=2, relief="groove")
        right_button_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=30)

        right_search_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=50, borderwidth=2, relief="groove")
        right_search_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=70)

        right_help_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=210, borderwidth=2, relief="groove")
        right_help_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=100)

        #Entry for search_container
        search_bar = Entry(right_search_container, width=66)
        search_bar.insert(0,"")
        search_bar.pack()

        #Labels
        left_container_label = Label(left_container, text=OUTPUT_FILE_CONTENT, width=45, height=23)
        left_container_label.pack()
        right_container_label = Label(right_help_container, text=MAIN_HELP_MESSAGE, width=56, height=18, padx=2, pady=2)
        right_container_label.pack()


        #Buttons
        add_button = Button(right_button_container,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text="Add")
        delete_button = Button(right_button_container,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text="Delete")
        search_button = Button(right_button_container,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text="Search")
        update_button = Button(right_button_container,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text="Update")
        quit_button = Button(right_button_container,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text="Quit")

        buttons_list = [add_button, delete_button, search_button, update_button, quit_button]

        for index, button in enumerate(buttons_list):
            button.padx = 1
            button.grid(row=0, column=index)

        #Functions for keybinding
        def click_on_adding_button(self):
            if len(search_bar.get()) == 0:
                right_container_label.config(text=EMPTY_INPUT_BOX_MESSAGE)
            else:
                right_container_label.config(text=ADDING_HELP_MESSAGE)
                library.adding_book(search_bar.get())

        # Keybinding
        add_button.bind('<Button-1>', click_on_adding_button)


            # STEP 1: CHECK INPUT FOR ENTRY -> IF EMPTY CHANGE HELP MESSAGE
            # STEP 2: UPDATE HELP MESSAGE ELSE
            # STEP 3: ADD BOOK
            # STEP 4: UPDATE DISPLAY


        #Window config
        self.geometry(f"{TOTAL_WIDTH_OF_WINDOW}x{TOTAL_HEIGHT_OF_WINDOW}")
        self.title("BookWorm")



window = Application()
window.resizable(False, False)
window.mainloop()