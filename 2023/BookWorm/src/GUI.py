from tkinter import Tk, Button, Label, Frame

TOTAL_WIDTH_OF_WINDOW = 800
TOTAL_HEIGHT_OF_WINDOW = 400
MARGIN_LEFT = 15
# WindowW - LeftContainerW - InitialPlacement * 4
X_POS_FOR_RIGHT_CONTAINER = TOTAL_WIDTH_OF_WINDOW - 320 - 120

class GUI(Tk):

    def __init__(self):
        super().__init__()

        #Frames
        left_container = Frame(self, width=320, height=350, borderwidth=2, relief="groove", bg="lightgray")
        left_container.place(x=MARGIN_LEFT, y=30)

        right_button_container = Frame(self, width=420, height=70, borderwidth=2, relief="groove", bg="gray")
        right_button_container.place(x=X_POS_FOR_RIGHT_CONTAINER, y=30)

        #Window config
        self.geometry(f"{TOTAL_WIDTH_OF_WINDOW}x{TOTAL_HEIGHT_OF_WINDOW}")
        self.title("BookWorm")


window = GUI()
window.resizable(False, False)
window.mainloop()