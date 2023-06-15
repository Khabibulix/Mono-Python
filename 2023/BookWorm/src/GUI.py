from tkinter import Tk, Button, Label

class GUI(Tk):

    def __init__(self):
        super().__init__()

        label = Label(self, text="Manage your library with BookWorm")
        label.pack()

        button = Button(self, text="Push me!", command=self.clicking)
        button.pack()

        self.geometry("300x200")

        self.title("BookWorm")

    def clicking(self):
        print("Button clicked")

window = GUI()
window.mainloop()