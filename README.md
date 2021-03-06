# Optimus Wind Turbine Design Software
This software is for the design of a wind turbine.

# Requirements
- pipenv
- python 3

# How to start
This software is written in Python with the Django framework. A virtual environment is required. Go to the directory with the 'Pipfile' in it and run
```python
pipenv shell
pipenv install
```
This should start the virtual environment and install Django in it. To switch the view of the Readme, press 'ctrl' + 'shift' + 'v'.


For starting the server, go into the directory with 'manage.py' in it and then type
```python
python manage.py runserver
```
For the first use, the database needs to be synced with the project. For this purpose, type
```python
python manage.py migrate
```
followed by
```python
python manage.py makemigrations
```
and then migrate again.

# Admin panel
For the admin panel you need to create a super user. Type
```python
python manage.py createsuperuser
```
and follow the instructions. After successfully creating a super user, you can run the server and go to http://127.0.0.1:8000/admin. To manipulate values of the models in the admin panel, register them in 'admin.py'.
For registering a model, firstly import it and then register it with admin.site.register(<model name>)

# Building models
Django is designed to use models. In 'models.py' in the app directory ('Windturbine') you can create models for the different parts of the turbine. To work in the shell, type
```python
python manage.py shell
```
and import the models with 'from WindTurbine import <model name>'


# Changing code
For changing code, it is good practice to use different branches and not directly push it to the master code.