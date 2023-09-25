import os
from flask import Flask, request
import yaml

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

def load_config():
    config = {'HTTPS_PORT': 443}
    try:
        with open('server-settings.yaml', 'r') as f:
            loaded_config = yaml.safe_load(f)
        config.update(loaded_config)
    except FileNotFoundError:
        print("settings.yaml not found, using default settings.")

    certfile = config.get('SSL_CERTFILE')
    keyfile = config.get('SSL_KEYFILE')

    if certfile and keyfile:
        if certfile and keyfile:
            if not os.path.exists(certfile):
                raise FileNotFoundError(f"SSL_CERTFILE {certfile} not found.")
            if not os.path.exists(keyfile):
                raise FileNotFoundError(f"SSL_KEYFILE {keyfile} not found.")

        if not os.path.exists(certfile) or not os.path.exists(keyfile):
            raise FileNotFoundError("SSL_CERTFILE or SSL_KEYFILE not found.")
        config['ssl_context'] = (certfile, keyfile)
    elif certfile or keyfile:
        raise ValueError("Both SSL_CERTFILE and SSL_KEYFILE must be set.")
    else:
        config['ssl_context'] = 'adhoc'
    return config

if __name__ == "__main__":
    config = load_config()
    app.run(ssl_context=config['ssl_context'], port=config['HTTPS_PORT'])

