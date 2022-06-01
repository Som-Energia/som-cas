# Som Energia CAS Authentication Service

This peace of software is used to authenticate users from different services against Som Energia client-space.

## Instalation

### Prerequisistes

Before you begin, ensure you have met the following requirements:
* You should have installed `pipenv`. Instructions here -> https://pipenv.readthedocs.io/en/latest/#install-pipenv-today
* You should have a `Linux/Mac` machine. Windows is not supported and we are not thinking in it.
* An `nginx` installation
* Optionally, an user with sudo permissions


### Configuration

#### Settings file
#### Configuration file

## Deployment


## Development

### Basic GitHub Checkout
We will assume that the folowing folder exists:

  * `PROJECTS_PATH` = `$HOME/projects`

Checkout the project:
```bash
user@host:> git clone git@github.com:Som-Energia/som-cas.git $PROJECTS_PATH/som-cas
```

Walk throw `$PROJECTS_PATH/som-cas` and install the requirements with `pipenv`
```bash
user@host:> cd $PROJECTS_PATH/som-cas
user@host:som-cas> pipenv install --dev
```

Copy `conf.yaml.example` to `config/conf.yaml` and adapat it to meet your needs.
If you want to place this file in other folder, set the environ variable `SOM_CAS_CONFIG` with the full path of the configuration file.

Run migrations, create an admin user and run the server to check that everything fit.
```bash
user@host:som-cas> pipenv run ./manage migrate
user@host:som-cas> pipenv run ./manage createsuperuser
user@host:som-cas> pipenv run ./manage runserver
```

And that's it. Now you can start to develop in a new branch. Please, when you are finished, make a pull request and asign one of us. We will check the pull request and if is every thing is ok, we will acept it :D

## Changes
### 0.7.0
* Adapted texts for 2022 general assembly
* In Django 2.2 pyscopg version must be <2.9

### 0.6.0
* Adapted texts for 2021 general assembly
* Improved admin site for better user experience

### 0.5.2
* Improved warning text when forthcoming assembly is inactive

### 0.5.1
* Fixed bug in service discover regex 

### 0.5.0
* Added local groups assemblyes registration 
* Tests improvemets

### 0.4.0
* Add new service: Education platform is now on CAS
* Add helper to login view

### 0.3.4
* Download census
* Improved translations 

### 0.3.3
* fixed concurrency problems when updating registration_email_sent attribute

### 0.3.2
* confirmation email is sent in background

### 0.3.1
* Fix confirmation email structure and legal texts

### 0.3.0
* Added census registration for especfic site
* Improved translations

## Contact
If you want to contact with us, feel free to send an email to <info@somenergia.coop>.

## Licence
This project uses the following license: [GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE).
