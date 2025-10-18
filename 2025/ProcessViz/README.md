# Process Viz (current project)

## Expectations at 05/10/25

- Script that generate processes snapshots to stock on a server
- Fast and asynchronous
- FastAPI stack with SQLAlchemy and TDD method
- Feature to navigate in processes, a bit like a C&C

## Expectations at 08/10/25

- Process viewer in a basic web page
- Consulting a process via its PID
- View metrics for memory, CPU usage... etc

### Where I am at 14/10/25

Web app is styled with CSS, vanilla CSS and I'm using JS to grab a click event on a process and display it in a new Flask route. The web-app looks slow to load but is working as intended.
Next step is to analyze the process to display a _score of trust_, it will be the beginning of data visualisation.

### Where I am at 16/10/25

Full glow-up on all the web-app. Switching to Quart + asyncio speeds up the loading. However, i got a Lighthouse score of 55 in performances, which is pretty bad. The content is available after 21,4s and its size is 176KiB. After caching and Quart migration, content is available after 1,7s, and performance score is at 97.


## Possible improvements

- ~~Make it quicker~~
- Add a real logging file for easier debug
- Styling of _waiting web-page_
- ~~Process Tree~~
- ~~DLL & files opened~~
- Opening and inspecting DLL files on click, see _Bugs 1_
- Geolocation of opened connections
- DB conn

## Bugs
 - 1 "Certains objets retournés par psutil.Process().memory_maps() n’ont pas d’attribut .path, ni .addr, ou le retour est vide — mais la ligne échoue au moment du getattr(m, 'path', None)"

## What i want to learn

- Basic API design
- Processes under the hood

## What i learned/relearned:

- Jinja templates, playing with Win32 APIs
- Review for dictionary/JSON
- Hashlib, Radon, Signtool
- Quart