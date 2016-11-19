# Secret Santa

A simple web app that allows people to enter names and email addresses, and it will send out emails to all users with a randomised pairing.

## First-time setup

Languages/applications needed
- Python 3.5 and PIP
- Postgres [postgres](https://www.postgresql.org)
- Heroku Toolbelt [heroku](https://toolbelt.heroku.com) (optional)


The app runs within a virtual environment. To [install virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html), run
```shell
    [sudo] pip install virtualenv
```

Install virtualenvwrapper
```shell
    [sudo] pip install virtualenvwrapper
```

Create a local environment.sh file containing the following:
```shell
echo "
export DJANGO_SETTINGS_MODULE='secret_santa.settings.dev'
export DATABASE_URL='postgres://localhost/santa'
export SECRET_KEY='REPLACE ME WITH AN ACTUAL SECRET KEY'
"> environment.sh
```

Make a virtual environment for this app:
```shell
    mkvirtualenv -p /usr/local/bin/python3.5 santa
```

Install dependencies
```shell
    ./scripts/bootstrap.sh
```

## Running the application

Running with django runserver:
```shell
    workon santa
    python manage.py runserver
```
Then visit [localhost:8000](http://localhost:8000)

Or through heroku:
```shell
    workon santa
    heroku local
```
Then visit [localhost:5000](http://localhost:5000)

## Running tests

Tests include a pep8 style check, django test script and coverage report.

```shell
    workon santa
    ./scripts/run_tests.sh
```
