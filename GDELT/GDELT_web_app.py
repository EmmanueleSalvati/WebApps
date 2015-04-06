"""Run the arXiv app back-end"""

import flask
import json
from sys import path
path.append('./static')


app = flask.Flask(__name__)


@app.route("/")
def viz_page():
    """Homepage to serve the visualization page"""

    with open('index.html') as viz_file:
        return viz_file.read()


app.debug = False
app.run(host='0.0.0.0', port=8800)
