import flask
from flask import request
import sys
application = flask.Flask(__name__)
 
@application.route("/")
def index():
    return flask.render_template('index.html')

@application.route("/result", methods=['POST'])
def get_bet_value():
    result = request.form['text']
    return flask.render_template('result.html', result = result)

 
if __name__ == "__main__":
    application.run(debug = True)

