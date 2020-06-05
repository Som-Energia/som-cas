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
### 0.3.0
* Added census registration for especfic site
* Improved translations

## Contact
If you want to contact with us, feel free to send an email to <info@somenergia.coop>.

## Licence
This project uses the following license: [GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE).
