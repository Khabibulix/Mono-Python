# Process Viz (current project)

ProcessViz is a high-performance monitoring tool that provides real-time visibility into running processes, DLLs, open files, signatures, and potential security risks.
Built with Quart (async Flask), psutil, WebSockets, and pefile, it delivers an interactive dashboard designed for developers, analysts, and security practitioners who need to understand what is happening on a machine — right now.


### Table of contents
- [V 1.0](#process-viz-v-10)
- [Expectations](#expectations-at-051025)
- [DevLog](#where-i-am-at-141025)
- [Improvements](#possible-improvements)
- [Learning Objectives](#what-i-want-to-learn)
- [What I learned](#what-i-learnedrelearned)
- [V 2.0](#process-viz-v-20)

## How to launch things
- ```git clone http://www.github.com/Khabibulix/Mono-Python```
- ```cd Mono-Python\2025\ProcessViz```
- ```python -m app.app``` for main web-app
- ```pytest``` to launch tests


## Process Viz v 1.0


## Expectations at 05/10/25

- Script that generate processes snapshots to stock on a server
- Fast and asynchronous
- FastAPI stack with SQLAlchemy and TDD method
- Feature to navigate in processes, a bit like a C&C

## Expectations at 08/10/25

- Process viewer in a basic web page
- Consulting a process via its PID
- View metrics for memory, CPU usage... etc

## Expectations at 06/11/25

- DLL static analysis in webpage
- Clear reading of what is going on


###  📅 14/10/25

Web app is styled with CSS, vanilla CSS and I'm using JS to grab a click event on a process and display it in a new Flask route. The web-app looks slow to load but is working as intended.
Next step is to analyze the process to display a _score of trust_, it will be the beginning of data visualisation.

###  📅  16/10/25

Full glow-up on all the web-app. Switching to Quart + asyncio speeds up the loading. However, i got a Lighthouse score of 55 in performances, which is pretty bad. The content is available after 21,4s and its size is 176KiB. After caching and Quart migration, content is available after 1,7s, and performance score is at 97.

###  📅  18/10/25

Working on DLL and opened files. It is now possible to check certain metrics about a process via its PID, if a file is signed, if the path is a standard one. All of that displays a _risk level_


###  📅  19/10/25

Adding loggings features and removing _asyncio_ noise, quick debug on process main page click events.
Optimizing _psutil_ with ```attrs[]```, calls are less frequent, then faster. Beginning of TDD for all processes classes.

### 📅 20/10/25
Resolved recurring issues with Async/Await, nasty bugs these ones! 🤯 Developed unit tests for the `ProcessAnalyzer` class using `unittest.mock` to simulate `psutil` behaviors and utility functions (`is_signed`, `is_invocating_scripts`, etc.). Adjusting mocks to precisely reflect real execution conditions, including normalization of suspicious executable paths with `.lower()`.

### 📅 21/10/25
Set up asynchronous testing environment with `pytest-asyncio`. Fixed errors related to unawaited coroutine objects by properly awaiting async fixtures.
Mocked various dependencies (`psutil`, `is_signed`, etc.) in tests to isolate the `ProcessAnalyzer` behavior.Achieved all tests passing successfully, writing tests for ProcessAnalyzer. ```Pytest-cov``` score is at 60% for ```process_manager.py```
_Auto Fetch()_, page reloads automatically without user intervention. Using full ```JS/AJAX```, not needing more. 
Broke LightHouse Score, currently at 40.

### 📅 22/10/25
Full glow-up for speed, removing some infos on the first page the user sees, adding a button to analyse and display more. 

Front-end is quicker still with full AJAX. 

Reaching 91% of test coverage for ```process_manager.py```

Fighting with CSS, currently the layout is like this:

![Layout](pics/loadout.png)

### 📅 23/10/25

_Plan for the day_: Transition from _polling AJAX_ to _WebSocket_ for ```/``` route to have a "live" view of the processes.
Organizing project with ```/app``` and others mains refactorisations

### 📅 24/10/25

Cleaning ```app.py``` for better structure.

### 📅 05/11/25

Implementation of WebSocket, linting/testing all project before each commit with ```black/pytest``` More styling for index page.

### 📅 06/11/25

Jinja Templates inheritance. Adding colored borders to see potentially suspicious processes on ```index``` page. PeFile infos for DLL view, really cryptic for now, but useful infos to see if DLL is packed or known. Preparing events alerts for strange new processes with ```Asyncio.Queue()``` Hunt for logic flaws in score, making easier maintainable function for score handling.


### Strange behaviour to fix

- ✅    Unclickable buttons (button element was not correctly placed)
- ✅    Broken route for /process/pid (Blueprint for DLL link was not correctly called in template)
- ✅    CSS not linked correctly for /process/<pid> route (Unorthodox use of {extends})


## Possible improvements that i will make

- ✅    Make it quicker
- ✅    Add a real logging file for easier debug
- ✅    Styling of _waiting web-page_
- ✅    Process Tree
- ✅    DLL & files opened
- ✅    Opening and inspecting DLL files on click
- ✅    Profile code
- ✅    Optimize _psutil_ with attrs
- ✅    Read files async style with _aiofiles_
- ✅    Pytest rapport to check tests coverage
- ✅    Auto fetch() without reloading page for standard access in /
- ✅    Lazy loading, load only x's first processes
- ✅    Full test coverage for classes
- ✅    WebSocket implementation
- ✅    Risk level in index page to view suspicious processes
- ✅    More DLL infos with pefile


## What i want to learn

- Basic API design
- Processes under the hood

## What i learned/relearned:

- Jinja templates, playing with Win32 APIs
- Review for dictionary/JSON
- Services
- Hashlib, Radon, Signtool, Psutil
- Project organisation and modularization
- Quart, Blueprint, Context processor
- Async/Await for Files(```aiofiles```) or Requests(```asyncio```)
- Py-Spy, Mocking with _unittest.mock_, _pytest_ TDD
- Black linter to format the code properly
- WebSocket replacing Ajax polling


## Process Viz v 2.0

## Expectations at 06/11/25
- Basic behavioral detection nore like an EDR
- Live-streamed alerts
- Real Web Dashboard
- Multimachine controller
- FastAPI stack