# djangoldp_energiepartagee
How to install the project locally

1- create virtual environement
`py -m venv venv`

2- activate venv
`venv\Scripts\activate.bat`

3- update pip & wheel
`py -m pip install -U pip wheel`

4- install sib-manager
`py -m pip install -U sib-manager`

5- launch the startproject command
`sib startproject energiepartagee_server`

6- install server
  => go into energiepartagee_server folder
`sib install server`

7- create superuser
`py manage.py createsuperuser`

8- add virtual link with the djangoldp_energiepartagee package : 
`mklink /D [LINK] [TARGET]`
`mklink /D [...]\energiepartage_server\djangoldp_energiepartagee [...]\djangoldp_energiepartagee\djangoldp_energiepartagee`
=><!> [LINK] : Link to the "folder" where the target will be found

9- add the package in the package.yml file

10- run migration and migrate
`py manage.py makemigrations djangoldp_energiepartagee` (for the first time, then `py manage.py makemigrations` will be enough in case ogf modifications of the package)
`py manage.py migrate`

11- runserver
`py manage.py runserver`
