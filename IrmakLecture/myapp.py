import flask


from sklearn.linear_model import LogisticRegression
import numpy as np


X = np.linspace(1, 1000, 50).reshape(-1, 1)
Y = np.zeros(50,)
Y[25:] = np.ones(25,)

# print X
# print Y

PREDICTOR = LogisticRegression().fit(X, Y)

# print PREDICTOR.predict([200])

# __name__ is the name of the current file
app = flask.Flask(__name__)


@app.route("/")
def hello():
    return "It's alive!!!!"


@app.route("/predict", methods=['POST'])
def predict():
    data = flask.request.json
    x = np.array(data["example"]).reshape(-1, 1)

    # Classify
    y_pred = PREDICTOR.predict(x)
    y_pred = list(y_pred)
    results = {"predicted": y_pred}
    return flask.jsonify(results)


app.debug = True

app.run(host='0.0.0.0', port=8888)
