from urllib.parse import urlparse, parse_qsl, urlencode, parse_qs
from requests.exceptions import HTTPError

import cas
import requests
from flask import Flask


app = Flask(__name__)

CAS_URL_LOGIN = 'http://cas.somenergia.coop:8000/login'

CAS_SERVER_URL = 'http://cas.somenergia.coop:8000/'

SERVICE_NAME = 'http://api.somenergia.coop'

CAS_CLIENT = cas.CASClientV3(
    server_url=CAS_SERVER_URL,
    service_url=SERVICE_NAME,
    extra_login_params=False,
    renew=False
)


def _get_ticket(response):
    response_info = response.raw.info().get('Location', '')
    if response_info:
        return parse_qs(urlparse(response_info).query)['ticket'][0]

    raise HTTPError()


def cas_login(username, password):
    resp = requests.get(CAS_URL_LOGIN)

    headers = {
        'X-CSRFToken': resp.cookies.get('csrftoken'),
        'Origin': 'https://cas.somenergia.coop',
        'Referer': 'https://cas.somenergia.coop/login'
    }
    params = {'service': 'http://api.somenergia.coop'}
    payload = {'username': username, 'password': password}

    resp_post = requests.post(
        url=CAS_URL_LOGIN,
        data=payload,
        params=params, headers=headers, cookies=resp.cookies,
        allow_redirects=False
    )
    resp_post.raise_for_status()

    ticket = _get_ticket(resp_post)

    params.update(
        parse_qsl(urlparse(resp_post.raw.info()['Location']).query)
    )

    return CAS_CLIENT.verify_ticket(ticket)


if __name__ == '__main__':
    try:
        app.run(
            host='localhost',
            debug=True
        )
    except KeyboardInterrupt:
        shutdown = requests.environ.get('werkzeug.server.shutdown')
        if shutdown is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown()
