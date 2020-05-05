## How to run this app if it is the first time cloning this repo:
1) clone git repo
1) `cd exercisesproject`
1) Run the following code in your terminal to create a virtual environment

    Mac Users:
    ```
    python -m venv exercisesenv
    source ./exercisesenv/bin/activate
    pip install django
    pip freeze > requirements.txt
    ```

    Windows users:
    ```
    python -m venv exercisesenv
    source ./exercisesenv/Scripts/activate
    pip install django
    pip freeze > requirements.txt
    ```
1) Run application in virtual environment: 
    ```
    python manage.py runserver
    ```

## How to run this app if you've previously cloned this repo (and have already created a virtual environment):
1) `cd exercisesproject` (verify that this is the directory that contains `manage.py`)
1) Enter the virtual environment

    Mac Users:
    ```
    source ./exercisesenv/bin/activate
    ```
    Windows Users:
    ```
    source ./exercisesenv/Scripts/activate
    ```
1) Run application in virtual environment:          
    ```
    python manage.py runserver
    ```
