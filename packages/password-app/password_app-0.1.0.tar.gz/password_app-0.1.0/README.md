# Passwords_app

Flask-ML application to predict password frequency

## Installation

First clone the repo locally.
~~~bash
- $ git clone https://gitlab.com/production-ml/password_app
- $ cd password_app
~~~

Install Pipenv and its dependencies.
~~~bash
- $ pip install pipenv
~~~

Activate the virtual environment.
~~~bash
- $ pipenv shell
- $ pipenv install --dev
~~~

For deploy you should use commands:
~~~bash
- $ pipenv shell
- $ pipenv install
~~~

Run the web application via
~~~bash
- $ python app.py
~~~

Deactivate the virtual environment.
~~~bash
- $ exit
~~~

## Jupyter enviromnet settings:

Activate the virtual environment.
~~~bash
- $ pipenv shell
- $ pipenv install --dev
~~~

~~~bash
- $ python -m ipykernel install --user --name=venv38
~~~

## Launch jupyter:
~~~bash
- $ jupyter notebook
- select kernel "venv38"
~~~

## Development

To commit changes, first run `pre-commit install`. If you have no pre-commit installed, you can do it following instructiosn at https://pre-commit.com
