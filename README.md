# cerebracode
A learning AI system designed for building code.

## Authors

   LinuxLeah and GPT-4.

## Installation

1: Install prerequisites:
* Flask: `pip install Flask` or `pip3 install Flask`.
* PyYAML: `pip install PyYAML` or `pip3 install PyYAML`
* Waitress: `pip install waitress` or `pip3 install waitress`
* pyOpenSSL: `pip install pyOpenSSL` or `pip3 install pyOpenSSL`
* If you'll be using ad-hoc HTTPS certificates (RECOMMENDED ONLY FOR TESTING/DEV!):
** Cryptography: `pip install Cryptography` or `pip3 install Cryptography`

2: Edit server-settings.yaml to taste.

3: Run server.py: `python3 server.py`

## Troubleshooting

* Getting 'Permission denied' when running the server? If server-settings.yaml does not exist, or if server-settings.yaml sets HTTPS_PORT to 443, the server would be trying to bind to the port 443, which non-root users cannot bind to. Set HTTPS_PORT to a port 1024 or greater in server-settings.yaml, or run the server as root or another superuser.
