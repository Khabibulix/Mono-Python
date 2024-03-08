from tkinter import *
from Blocker import Blocker, block_list, clear_host_file_as_if_not_touched

bk = Blocker("127.0.0.1")


class Application(Tk):
    def __init__(self):
        super().__init__()

        top_container = Frame(self, width=500, height=100, borderwidth=5, relief="groove")
        top_container.place(x=0, y=0)

        label = Label(top_container, text="Please enter the name or the IP of the site you want to block:")
        label.place(x=30, y=10)

        text_box_for_input = Text(top_container, height=1, width=40)
        text_box_for_input.place(x=30, y=30)
        text_box_for_input.config(state='normal')

        unblock_button = Button(top_container, text="➖", fg="black", bg="lightblue")
        unblock_button.place(x=30, y=60)

        block_button = Button(top_container, text="➕", fg="black", bg="lightblue")
        block_button.place(x=65, y=60)

        delete_input_button = Button(top_container, text="🗑", fg="black", bg="lightblue")
        delete_input_button.place(x=95, y=60)

        print_all_button = Button(top_container, text="Show all!", fg="black", bg="lightblue")
        print_all_button.place(x=150, y=60)

        delete_all_button = Button(top_container, text="Delete all!", fg="black", bg="lightblue")
        delete_all_button.place(x=220, y=60)

        retrieve_button = Button(top_container, text="Retrieve", fg="black", bg="lightblue")
        retrieve_button.place(x=300, y=60)

        bottom_container = Frame(self, width=500, height=400, borderwidth=5, relief="groove")
        bottom_container.place(x=0, y=100)

        text_box_for_output = Text(bottom_container, height=20, width=60)
        text_box_for_output.pack(expand=True)
        text_box_for_output.config(state='normal')


        #Keybinding

        block_button.bind('<Button-1>', lambda event:
            #Adding site to block-list then deleting input text
            bk.adding_site(text_box_for_input.get("1.0", END)))

        unblock_button.bind('<Button-1>', lambda event:
            # Removing site from block-list then deleting input text
            bk.deleting_site(text_box_for_input.get("1.0", END)))

        print_all_button.bind('<Button-1>', lambda event:
            text_box_for_output.insert("end", ("\n".join(block_list))))

        delete_input_button.bind('<Button-1>', lambda event:
            text_box_for_input.delete("1.0", "end"))

        delete_all_button.bind('<Button-1>', lambda event:
            text_box_for_output.delete("1.0", "end"))

        retrieve_button.bind('<Button-1>', lambda event:
        clear_host_file_as_if_not_touched())

        self.geometry("500x500")
        self.title("Website_Blocker")
        self.resizable(False, False)