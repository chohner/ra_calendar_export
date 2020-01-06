# RA calendar export

Export your RA events to an .ics calendar, for public and private profiles.

## Usage
This project uses [poetry](https://python-poetry.org/) for dependency management.

```
poetry install --no-dev  # install dependencies
poetry run ics_export    # begin calendar export
```

## Development
```
poetry install   # install dependencies
poetry run lint  # apply black
poetry run test  # run tests
```

## Todo
- Add more locations to the timezone lookup
- Add nicer CLI
