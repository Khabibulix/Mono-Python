# Contact Manager

First finished project of 2025

### What i learned

I _re-learned_ about POO, project organisation and basic Python, and I learned about CSV outputting.

### How to launch

You can launch main.py using ```python main.py```, the other files will not display anything.

### How my project is structured

```helpers.py``` --> Contains functions to sanitize user input 

```Contact.py``` --> Main class of the app, basic CRUD and saving. Basically, a ContactList contains a dictionary of contacts including names and phone numbers

```main.py``` --> Main part of the input, the user interacts here via a CLI only interface with a minimum interaction

### First launch

After entering the app, you will need to add your first contact. To do it you will need to enter ```1 + Enter```. The numbers on the left are the commands, if you do not use them the application will loop. It that happens, please press ```Ctrl + C``` to exit or ```7 + Enter```.

### How the input works

You will read _full name_. Let me show you some examples.

_Albert_ is not a full name, but _Albert Dawson_ is. The space **is** important, without, you will encounter problem.

Concerning phone numbers, it must have ten digits, international notation is not provided.

_0623546576_ works, not _+33623546576_, but I can work on it if needed.

I hope you like this very basic application, reach out to me for feedback or bugs.