"""Run the arXiv app back-end"""

import flask
import json
import numpy as np
import socket
from collections import Counter
from sys import path
from pymongo import MongoClient
path.append('./static')
import arXiv_helper as helper


KEYWORDS = ['electron', 'photon', 'muon', 'higgs', 'tau', 'proton',
            'neutron', 'quark', 'top', 'strange', 'bottom', 'quark',
            'lepton', 'meson', 'jet', 'BaBar', 'ATLAS', 'CMS']

# if socket.gethostname() == 'mcnulty-emmanuele':
#     client = MongoClient()
# else:
#     URI = 'mongodb://104.236.120.21'
#     client = MongoClient(host=URI)

# hepex = client.arXivpapers.hepex
# # hepph = client.arXivpapers.hepph

# cursor = helper.get_cursor(client)
# abs_dict = helper.loop_events(cursor, KEYWORDS)

# import pickle as pkl
# with open("abstract_with_str.pkl", 'r') as pklfile:
#     abs_dict = pkl.load(pklfile)

print 'Loop ended, you can view the page now'
# del cursor
# # abstract_json = flask.jsonify(abs_dict)
# abstract_json = json.dumps(abs_dict)

app = flask.Flask(__name__)


# @app.route("/data")
# def abstracts():
#     """Puts the dictionary of abstracts into the data route"""

#     return flask.jsonify(**abs_dict)


@app.route("/")
def viz_page():
    """Homepage to serve the visualization page"""

    with open('stacked_papers.html') as viz_file:
        return viz_file.read()


@app.route("/postdir", methods=['POST'])
def postdir():
    """When a POST request is made with some json data, read the
    sample from a json called sample, and return something.
    I have implemented the function date_range into the helper"""

    data = flask.request.json
    x = data['sample']
    the_counter = helper.date_range(abs_dict, x[0], x[1])

    return flask.jsonify(the_counter)


app.debug = False
app.run(host='0.0.0.0', port=8888)
