from tkinter import Tk, Button, Label, Frame

class GUI(Tk):

    def __init__(self):
        super().__init__()

        #Frames
        left_container = Frame(self, width=50, height=50, bg="blue")
        left_container.place(x=15, y=30)
        
        #Window config
        self.geometry("600x400")
        self.title("BookWorm")


window = GUI()
window.mainloop()