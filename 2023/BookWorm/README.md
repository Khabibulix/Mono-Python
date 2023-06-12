# BookWorm

<p>I want to make one project to rule them all.
  The goal here is to make an app that will help me to manage my forever growing library</p>
  
My plan at the 31/05/2023: <br>
<pre>
  - [x] Make a really simple console app
  - [x] Make a I/O working app
  - [] Make a GUI to make it easier, perhaps with Tkinter, as i already know that
  - [] Connect it to a database using an API
  - [] Adding backend to share library
  - [] Go cloud?
</pre>

I don't know yet how I will do it, but i'm on my way. I'll be using Python for this project, don't know if that's possible but i'll make my best.

![DeKs](https://github.com/Khabibulix/Mono-Python/assets/80721211/3cc37802-19f1-4880-9696-8f7b0d1bcdf8)

## Step 1: Console application

### 31/05/2023:
That's how i see my project, please don't mind the austerity of the schema.

![Bookworm](https://github.com/Khabibulix/Mono-Python/assets/80721211/56f55f8c-27c2-4460-9110-51f7d163a0cb)

I want to store my books in a text file, i could have done it in an array, but i want my changes to be persistent. Moreover, an array is a nasty idea for this type of project. I'll need libraries to play with files for this project, i don't think i'll need more for the first step which is a console application.

### 01/06/2023:

Code is on its way. Today i made the implementation for consulting the list. The data structure for the list is now a dictionnary, to be ultra specific, it will be an OrderedDict because i'll need the index of each book later. I d'ont know yet that data structure but i'll make play with it tomorrow. I have another task to do: make a nicer print for all books, i don't like the style of the one i'm currently using.

![Sans titre](https://github.com/Khabibulix/Mono-Python/assets/80721211/42a7e1b2-0083-4dbe-8e1b-44bf78c8ab8a)

### 02/06/2023

I quitted the OrderedDict, a nested list is doing the job, I don't need to track the order of the books for now. I want it to be sorted by alphabetical order, i can practice my algo next, when the project will be more advanced.

The pretty print function is complete: <br>
![Sans titre](https://github.com/Khabibulix/Mono-Python/assets/80721211/45f2018b-ea32-4499-b378-0a919f61de90)

 I added structure to my code using functions to make it more readable, for me and for others. The next step will be to try/catch all inputs, because users are malicious. My code will be more more safe, maybe i'll need to explain how the console app works too. Because i'm the only user yet and i know how it works. Some documentation will be necessary, i'll add it to my todo. I don't think it will be too difficult.
 
 ### 03/06/2023
 
 A quick update about input validation, i think i'll be using Regex to assure my input are correct. I'll need a quick recap about try/except before.

### 04/06/2023

More config than code today. I wanted  to make TDD for this project, using pytest. But i forgot that i need to mock my inputs for that. I'm struggling with unittest.mock for now and my tests aren't detected, which is disappointing. I think i'll need to focus on that for today, i'll move on tomorrow.
Let's be honest here, TDD is not necessary here, but i'll learn pytest aside. I'll drop try/except, i think that my code can treat just enough exceptions like this and I'll move on to the last functionnality of this step: the search for a book, by title or by author.

![Sans titre](https://github.com/Khabibulix/Mono-Python/assets/80721211/41e6b096-c9de-48ce-85b4-0db5765f34e2)

This is NOT the optimal solution, and NOT the most performant, but it's good enough for now. And working.

Next step is to move on into a setup with input/output, an array is not an option anymore. I want a text file stocking all of my data.

### 05/06/2023

Currently working on I/O. I am encountering some problems because i close my file quite brutally and i can't add or delete some stuff. Code is not working yet, don't know if i need to put all my code into a try/finally block to avoid errors. I'll debug tomorrow, i think it is a big step for today.

### 06/06/2023

I made some tests, it didn't seem to work until i found a logical bug. I was displaying the list and not the file. Now i'm working on the output itself and it seems to work. However, the file is making some strange writing, i'll need to figure out why.

![Sans titre](https://github.com/Khabibulix/Mono-Python/assets/80721211/494a35b6-372e-4bea-88b7-37463ad1aec4)

The consulting function is almost complete, i'll just need to pretty print all of this, without the "[]", it shall not be a problem.

### 07/06/2023

Deleted all references to the original list, which is no longer needed. Working on the suppression function, the app is now able to select correctly the book which will be deleted later. Just wondering if my multi loops setup will be efficient later when the app will get bigger... 

Almost all core functions are now complete and functionnal. I'll need to secure my code before moving on.

### 08/06/2023

Deletion function is now functional and a little more secure with error handling. The next step is to continue with the searching function. I want to make my all code POO friendly. The more simple it is, the less time i will spent on maintenance.

### 09/06/2023

All my app is now working and have all CRUD options, including update that i added today. The next step is to make it working while using the POO before making it into a GUI. I have a Library class, where we can add, update, delete or search, each Library will have an owner later on. This will make me gain some time.

### 10/06/2023

POO is complete, files are now separated as i like it. I'll write some tests for my Library class using mocking, i want to be sure that it will works whatever the context will be.

### 12/06/2023

Currently working on testing my application using pytest mocking. I raised a strange behaviour while testing. My adding_book function does not add to my output file, at least not when i'm testing it, which is strange. Maybe my first bug? I'll need to search about it while moving on.
