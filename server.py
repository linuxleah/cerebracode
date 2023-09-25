from flask import Flask, request
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

if __name__ == "__main__":
    app.run(ssl_context='adhoc', port=443)

