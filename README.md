# Mono-Python

Here is my mono-repository for the Python language, i learn it since april 2022 and from time to time, the code inside the folders are not from the same period of time, that's why the code's quality may vary. The first project i made which is inside this repo is <em> Calculator </em> and the last <em> Sudokus </em> if you want to compare.

I'll list and explain all this projects by alphabetical order, the two biggest are <em>Sudokus</em> and <em>Pong</em>

## Backdoor

![Sans titre](https://user-images.githubusercontent.com/80721211/193559392-74867b4f-3a39-4ae0-95d2-66f90d4b1832.png)

The main goal here was to emulate a backdoor, i made this project while i was self-studying cybersecurity to prove that a security breach could be used with Python.

We have two files there, one client and one server, in a reality scenario we will send the client file to our target and hide it, using for example, steganography. 
With our machine, we will run the server file and a tunnel will be created between the host and the server. <br> <br>
The connection is made using <em>sockets</em> --> https://docs.python.org/fr/3/howto/sockets.html

<br>I also added a functionnality to change path inside the backdoor like a normal command prompt with the <em>cd</em> command.

![Sans titre](https://user-images.githubusercontent.com/80721211/193560202-0b194f82-8e2e-402b-ae62-671d44b9cef8.png)

### How it could be improved

We could remove the ASCII encoding into the command prompt which make it really ugly, or we could add others functionnalities.

## Book_gen or Book Generator

![Sans titre](https://user-images.githubusercontent.com/80721211/193561988-fdc00a8d-d822-4e44-b7f2-1eeba68b5c14.png)

The main goal here was to randomize the next book that i'll read using a array data structure , the built-in modules and Tkinter to make a nice GUI.

We have five files there:
<ul>
<li>data.py, which contains the book list</li>
<li>main.py, which is self-explanatory</li>
<li>Book_chooser.py, which contains a class for each book and the stand-alone code to make it work without a GUI.</li>
<li>Application.py, which contains all the code for Tkinter and by extension, for the GUI</li>
<li>And, last, the test file for book_chooser.py</li>
</ul>

The functionning is simple, each book has an author and a title. We choose one, we display the title and the author inside a textbox. We "save" the choice
and we make a request using the <em>requests</em> module to display its price on the site https://www.chasse-aux-livres.fr/, which is a Skyscanner for books.
Then we display the URL for this specific book in another textbox.

### How it could be improved

There is a visible buffer overflow inside the title of the book tetxtbox, and the window of the application is ridiculously small.

## Calculator

![Sans titre](https://user-images.githubusercontent.com/80721211/193564442-c901213d-b2da-4564-9afe-fd0eed046080.png)

First Python project, it's a console-based calculator, really not much to say here.

### How it could be improved

Converting into int instead of float will be prettier, and i could also add a GUI or more operations.

## Forensic_tool

