# RA calendar export

Export your RA events to an .ics calendar, for public and private profiles.

## Usage
This project uses [poetry](https://python-poetry.org/) for dependency management.

```
poetry install --no-dev  # install dependencies
poetry run ics_export    # begin calendar export
```

### Note
The [ics.py](https://github.com/C4ptainCrunch/ics.py) library [converts all events to UTC time](https://github.com/C4ptainCrunch/ics.py/issues/188) before exporting to .ics file. Times should still show up correct though.

## Development
```
poetry install   # install dependencies
poetry run lint  # apply black
poetry run test  # run tests
```

## Todo
- Add timezones for all countries
- Add nicer CLI
