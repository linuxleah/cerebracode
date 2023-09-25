import os
import logging
from flask import Flask, request
import yaml
from waitress import serve
from OpenSSL import SSL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    return '''
    <html>
        <head>
            <title>Simple Web App</title>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script>
                $(document).ready(function(){
                    $("#btn").click(function(){
                        $.ajax({
                            url: "/data",
                            type: "get",
                            success: function(response){
                                $("#result").html(response);
                            }
                        });
                    });
                });
            </script>
        </head>
        <body>
            <button id="btn">Get Data</button>
            <div id="result"></div>
        </body>
    </html>
    '''

@app.route("/data")
def data():
    return "This is data from the server!"

def create_ssl_context(certfile, keyfile):
    logger.info("Creating SSL context.")
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file(keyfile)
    context.use_certificate_file(certfile)
    return context

def load_config():
    config = {'HTTPS_PORT': 443}
    logger.info("Loading configuration.")
    try:
        with open('server-settings.yaml', 'r') as f:
            loaded_config = yaml.safe_load(f)
        config.update(loaded_config)
    except FileNotFoundError:
        logger.warning("settings.yaml not found, using default settings.")

    certfile = config.get('SSL_CERTFILE')
    keyfile = config.get('SSL_KEYFILE')

    if certfile and keyfile:
        logger.info("SSL_CERTFILE and SSL_KEYFILE are provided.")
        if certfile and keyfile:
            if not os.path.exists(certfile):
                raise FileNotFoundError(f"SSL_CERTFILE {certfile} not found.")
            if not os.path.exists(keyfile):
                raise FileNotFoundError(f"SSL_KEYFILE {keyfile} not found.")
        config['ssl_context'] = create_ssl_context(certfile, keyfile)
    elif certfile or keyfile:
        raise ValueError("Both SSL_CERTFILE and SSL_KEYFILE must be set.")
    return config

if __name__ == "__main__":
    logger.info("Starting the application.")
    config = load_config()
    port = config['HTTPS_PORT']
    ssl_context = config.get('ssl_context')
    logger.info(f"Running server on port {port}")
    try:
        if ssl_context: # SSL via Waitress.
            serve(app, host='0.0.0.0', port=port, _ssl_context=ssl_context)
        else: # Ad-hoc SSL via Flask's built-in ad-hoc context.
            logger.warning("Server will use ad-hoc SSL context. THIS IS NOT RECOMMENDED FOR PRODUCTION USAGE. If this server is intended for production usage, please provide an SSL certfile and keyfile and set SSL_CERTFILE and SSL_KEYFILE in server-settings.yaml. This will make the server use the Waitress WSGI server, which is intended for production usage.")
            app.run(host='0.0.0.0', port=port, ssl_context='adhoc', debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")


