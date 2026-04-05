# STARstruck
semi-complete management solution for IntelliSTAR systems

## How to use
MAKE SURE YOU HAVE UV INSTALLED through `pip install uv`  
This should work well on Windows so if you want you can just host it directly on your i2.

1. Clone and cd into the repository
2. Run `uv venv` to get into a virtual environment
3. Run `uv sync` to install dependencies
4. Run `python manage.py migrate` to set up the database
5. Run `python manage.py createsuperuser` to create an admin account
6. Finally run `python manage.py runserver` to start the server

Note: You will need [the agent](https://github.com/fourteentrees/STARStruck-Agent) installed on an i2 and set up according to that guide. Make sure STARstruck is accessible from your i2!

## Features
- SpecialMessage support thru MSOs
- Azul promo text support
- Ad crawl and greeting management
- Mostly automated, you don't have to touch much
- More targeting capability than the actual IBOSS
- Cool admin interface

## Features in development
- CoolER admin interface
- Original IntelliSTAR support
- Fake alert generator