# CloudBolt Take-Home Coding Exercise

Congratulations, you passed the [CloudBolt Software](http://cloudbolt.io) hiring
screen. The next step is to demonstrate your coding and design chops at your own
pace, and show us what you’re capable of!

After getting the application installed and running, check out the
[INSTRUCTIONS.md](https://github.com/CloudBoltSoftware/coding-exercise/blob/master/INSTRUCTIONS.md)
document.

## Installation

### Requirements

* [Python >= 3.6](https://www.python.org/downloads/)
* [Poetry](https://github.com/python-poetry/poetry#installation)

It's recommended that you use the `make` commands provided in the Makefile. See
the Appendix for an explanation of what these commands do. If your development
environment doesn't support `make`, the you can copy-paste the commands into
your terminal that are listed in the "Non-Make Alternatives" column in the [Make
Commands](#make-commands) table below.

Additional packages can be installed using `poetry add <package-name>`.

> Note: Feel free to install any additional packages or tools to support your
> efforts!

## Getting Started

The following sections detail how to run the application and start developing.

If you’re unfamiliar with the structure of a Django application, check out the
[Django resources linked in the Appendix](#resources).

> Note: The message board application lives in `src/messageboard`.

### Initialize the Application

If you have any of the following environment variables set, you should unset
them:
* `DJANGO_SETTINGS_MODULE`

1. To initialize the application, run `make build`. This command creates a
   virtual environment using `pipenv` and installs the required Python packages.
   It also runs database migrations and seeds your database with fixtures (i.e.
   randomly-generated data).

### Start the Application

1. To start the application, run `make run`. This command starts the Django
   server on http://localhost:8080.

### Run Tests

1. With the application running, in a separate terminal, you can run automated
   tests using `make tests`.

### Run stats.py
1. To run the `stats.py` script, run `make stats`.

## Appendix

### Make Commands

We have provided a number of helpful commands via a Makefile to assist your
development experience.

| Command       | Description                                                                                         | Non-Make Alternative                                                                                                                                                 |
|---------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make build`  | Installs required packages to the virtual environment, managed by `pipenv`, and seeds your database | `poetry install && poetry run python src/manage.py makemigrations && poetry run python src/manage.py migrate && poetry run python src/manage.py seed_database`       |
| `make run`    | Runs the Django server at `http://localhost:8080`                                                   | `poetry run python src/manage.py runserver 0.0.0.0:8080`                                                                                                             |
| `make stats`  | Runs the `stats.py` script                                                                          | `poetry run python stats.py`                                                                                                                                         |
| `make shell`  | Opens an interactive terminal                                                                       | `poetry run python src/manage.py shell`                                                                                                                              |
| `make test`   | Runs unit tests                                                                                     | `poetry run python src/manage.py test messageboard.tests`                                                                                                            |
| `make format` | Formats the `src` folder using `black`                                                              | `poetry run black src && poetry run flake8 src`                                                                                                                      |
| `make wipe`   | Deletes and re-seeds the database                                                                   | `rm -f src/db.sqlite3 && poetry run python src/manage.py makemigrations && poetry run python src/manage.py migrate && poetry run python src/manage.py seed_database` |

### Resources

* [Django Quick Start](https://docs.djangoproject.com/en/2.2/intro/overview/)
* [DjangoGirls Tutorial](https://tutorial.djangogirls.org/en/)

### FAQ

#### 1. I don't have time to work on this, but I still want to apply to CloudBolt. What do I do?

If you have another project that you think would better exemplify your skills,
we'd love to see that instead! Regardless of the project, we will use the
[Evaluation Criteria](#evaluation-criteria).

If this is the case, please reach out to your hiring contact.

#### 2. I have other questions!

Please reach out to your hiring contact.
# cbolt
# cbolt
# cbolt
