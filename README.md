# dynamic_form application

## Setup

The first thing to do is to clone the repository:


Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd dynamic_form
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
```
And navigate to `http://127.0.0.1:8000/api/users/login/`.

To create form 
Navigate to `http://127.0.0.1:8000/api/forms/`.
