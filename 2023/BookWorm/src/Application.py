from tkinter import Tk, Button, Label, Frame, Entry

OUTPUT_FILE_CONTENT = open('output.txt', 'r').read()

TOTAL_WIDTH_OF_WINDOW = 800
TOTAL_HEIGHT_OF_WINDOW = 400
MARGIN_LEFT = 15
WIDTH_FOR_RIGHT_CONTAINER = 420
# WindowW - LeftContainerW - InitialPlacement * 4
X_POS_FOR_RIGHT_CONTAINER = TOTAL_WIDTH_OF_WINDOW - 320 - 120
BUTTON_WIDTH = 4
BUTTON_HEIGHT = 1

class Application(Tk):

    def __init__(self):
        super().__init__()

        #Frames
        left_container = Frame(self, width=320, height=350, borderwidth=2, relief="groove", bg="lightgray")
        left_container.place(x=MARGIN_LEFT, y=30)

        right_button_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=70, borderwidth=2, relief="groove", bg="gray")
        right_button_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=30)

        right_search_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=50, borderwidth=2, relief="groove", bg="lightblue")
        right_search_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=110)

        right_help_container = Frame(self, width=WIDTH_FOR_RIGHT_CONTAINER, height=210, borderwidth=2, relief="groove", bg="darkblue")
        right_help_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=170)

        #Entry for search_container
        search_bar = Entry(right_search_container, width=68)
        search_bar.insert(0," ")
        search_bar.pack()

        #Labels
        left_container_label = Label(left_container, text=OUTPUT_FILE_CONTENT, width=45, height=23)
        left_container_label.pack()

        #Buttons
        add_button = Button(right_button_container, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Add")
        delete_button = Button(right_button_container, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Delete")
        search_button = Button(right_button_container, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Search")
        update_button = Button(right_button_container, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Update")
        quit_button = Button(right_button_container, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text="Quit")
        buttons_list = [add_button, delete_button, search_button, update_button, quit_button]

        for button in buttons_list:
            button.pack()



        #Window config
        self.geometry(f"{TOTAL_WIDTH_OF_WINDOW}x{TOTAL_HEIGHT_OF_WINDOW}")
        self.title("BookWorm")


window = Application()
window.resizable(False, False)
window.mainloop()