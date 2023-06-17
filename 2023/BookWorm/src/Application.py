from tkinter import Tk, Button, Label, Frame, Entry

TOTAL_WIDTH_OF_WINDOW = 800
TOTAL_HEIGHT_OF_WINDOW = 400
MARGIN_LEFT = 15
WIDTH_FOR_RIGHT_CONTAINER = 420
# WindowW - LeftContainerW - InitialPlacement * 4
X_POS_FOR_RIGHT_CONTAINER = TOTAL_WIDTH_OF_WINDOW - 320 - 120

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
        search_bar = Entry(right_search_container, width=100)
        search_bar.insert(0," ")
        search_bar.pack()

        #Window config
        self.geometry(f"{TOTAL_WIDTH_OF_WINDOW}x{TOTAL_HEIGHT_OF_WINDOW}")
        self.title("BookWorm")


window = Application()
window.resizable(False, False)
window.mainloop()