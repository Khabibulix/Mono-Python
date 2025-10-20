# Process Viz (current project)


Process Viz is a fast and asynchronous web application designed to capture and visualize process snapshots on a server. Built initially with FastAPI and evolving towards Quart with asyncio, it allows users to browse and analyze system processes in real-time through a clean web interface.

### Table of contents

- [Expectations](#expectations-at-051025)
- [DevLog](#where-i-am-at-141025)
- [Improvements?](#possible-improvements)
- [Learning Objectives](#what-i-want-to-learn)
- [What I learned](#what-i-learnedrelearned)

## How to launch things

- ```python app.py``` for main app
- ```python -m unittest discover -s tests``` for unittest tests



## Expectations at 05/10/25

- Script that generate processes snapshots to stock on a server
- Fast and asynchronous
- FastAPI stack with SQLAlchemy and TDD method
- Feature to navigate in processes, a bit like a C&C

## Expectations at 08/10/25

- Process viewer in a basic web page
- Consulting a process via its PID
- View metrics for memory, CPU usage... etc

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


## Possible improvements

- ✅    Make it quicker
- ✅    Add a real logging file for easier debug
- ✅    Styling of _waiting web-page_
- ✅    Process Tree
- ✅    DLL & files opened
- ✅    Opening and inspecting DLL files on click
- ✅    Profile code
- ✅    Optimize _psutil_ with attrs
- Test coverage for classes
- Dynamic dashboard Event-Driven with Asyncio.Queue
- Optimize search in CONFIG

- Visual profiling
- Lazy loading, load only x's first processes then frontend JS
- Auto fetch() without reloading page for standard access in / and /tree
- Hashing files in _WebAssembly_ to free the back-end, _Pyodide_, then _Rust-WASM_

- Geolocation of opened connections
- DB conn
- More DLL infos with pefile
- Read files async style with _aiofiles_
- _Hierplane_ for displaying tree
- Optimize fetching of services with _WMI Watcher_ or _psutil_
- Workers _Dask_
- Plugin System and _REPL_ for modifying system while running



## What i want to learn

- Basic API design
- Processes under the hood

## What i learned/relearned:

- Jinja templates, playing with Win32 APIs
- Review for dictionary/JSON
- Services
- Hashlib, Radon, Signtool, Psutil
- Quart, Context processor
- Py-Spy, Mocking with _unittest.mock_