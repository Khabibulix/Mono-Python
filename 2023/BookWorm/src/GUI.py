from tkinter import Tk, Button, Label, Frame

TOTAL_WIDTH_OF_WINDOW = 800
TOTAL_HEIGHT_OF_WINDOW = 400
TOTAL_HEIGHT_OF_TOP_MENU = 15

class GUI(Tk):

    def __init__(self):
        super().__init__()

        #Frames
        left_container = Frame(self, width=320, height=350, relief="raised", bg="lightgray")
        left_container.place(x=TOTAL_HEIGHT_OF_TOP_MENU, y=30)

        #Window config
        self.geometry(f"{TOTAL_WIDTH_OF_WINDOW}x{TOTAL_HEIGHT_OF_WINDOW}")
        self.title("BookWorm")


window = GUI()
window.resizable(False, False)
window.mainloop()