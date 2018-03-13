#API for making predictions

import numpy as np 
import pandas as pd
import pickle
from flask import Flask, jsonify, request

myModel = pickle.load(open('finalizedmodel.sav', 'rb'))

app = Flask(__name__)

@app.route('/api', methods = ['POST'])

def make_predict():

	cols = pd.read_csv('trainingCases.csv', nrows=1).columns.tolist()

	del cols[0]
	cols.remove('timeToAdoption')

	data = request.get_json(force = True)

	predict_request = [[data[i] for i in cols]]
	predict_request = np.array(predict_request)

	y_hat = myModel.predict(predict_request)
	output = [y_hat[0]]

	return jsonify(predictions = output)


if __name__ == '__main__':
	app.run(port = 9000, debug = False)