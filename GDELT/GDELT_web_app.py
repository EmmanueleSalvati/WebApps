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


# @app.route("/postdir", methods=['POST'])
# def postdir():
#     """When a POST request is made with some json data, read the
#     sample from a json called sample, and return something.
#     I have implemented the function date_range into the helper"""

#     data = flask.request.json
#     x = data['sample']
#     the_counter = helper.date_range(abs_dict, x[0], x[1])

#     return flask.jsonify(the_counter)


app.debug = False
app.run(host='0.0.0.0', port=8800)
