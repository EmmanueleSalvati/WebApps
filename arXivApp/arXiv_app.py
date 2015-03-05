"""Run the arXiv app back-end"""

import flask
from sys import path
from pymongo import MongoClient
path.append('./static')
import arXiv_helper as helper


KEYWORDS = ['electron', 'photon', 'muon', 'higgs', 'tau', 'proton',
            'neutron', 'quark', 'top', 'strange', 'bottom', 'quark',
            'lepton', 'meson', 'jet', 'BaBar', 'ATLAS', 'CMS']

client = MongoClient()
hepex = client.arXivpapers.hepex
hepph = client.arXivpapers.hepph

cursor = helper.get_cursor()
abs_dict = helper.loop_events(cursor, KEYWORDS)
del cursor
abstract_json = flask.jsonify(abs_dict)

app = flask.Flask(__name__)


@app.route("/")
def viz_page():
    """Homepage to serve the visualization page"""

    with open('arXiv_slider.html') as viz_file:
        return viz_file.read()


@app.route("/postdir", methods=['POST'])
def dosomething():
    """When a POST request is made with some json data, read the
    sample from a json called sample, and return something.
    I have implemented the function date_range into the helper"""
    pass
