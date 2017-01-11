# Setup local developer copy

## Install prerequisites

* node.js
* Python 3.5
* Postgres 9.5+

## Clone project

```
git clone git@github.com:funrun/funrun.git
cd funrun
```

## Create PostgreSQL database

```
createdb funrun
```

## Prepare Python virtual environment

[Install pyenv](https://github.com/yyuu/pyenv-installer#github-way-recommended), then:

```
pyenv install 3.5.2
pyenv virtualenv 3.5.2 funrun
pyenv local funrun
```

## Install pip-tools

```
pip install pip-tools
```

## Setup local config

```
cp conf/local.sample.py conf/local.py
```

## Update local project dependencies

```
pip-sync
```

This will need to be re-run every time a new dependency is added.

## Update database schema

```
src/manage.py migrate
```

This will need to be re-run every time a new schema migration is added.

## Create local admin user

```
src/manage.py createsuperuser
```

This only needs to run once.

## Run local server

```
src/manage.py runserver
```

The project is now accessible at <http://localhost:8000>.
