# SOMCAS CLIENTS

Web clients to simulate diferent applications to test som-cas application 

# Instalation

```bash
$> pipenv --python 3 install
```

# Run the client
Actually there are three projects, `8hours`, `black-ligth` and `cas-api`.

`8hours` and `black-ligth`are two sample webapplications. To lunch it enter in each folder and run:
```bash
$> pipenv run python main.py
```
`cas-api` is an intent to authenticate apis in cas. It is a work in progress and not is working.

# Configurate clients
When clients are up und running, then you have to add two entries in your `/etc/hosts` to simulate that they are two diferent applications. A possible configuration could be:
```
127.0.0.1       blacklight.somenergia.coop 8hours.somenergia.local
```

Now you can especify in som-settings this two services in the setting `mama_cas_services` that is in the file conf.yaml.



