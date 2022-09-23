# import libaries
from flask import Flask,render_template,url_for,request,flash,session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index',methods=['POST', 'GET'])
def predict():
	if request.method == 'POST':
		msg =''
		# collect factors
		seating = request.form['seating']
		feeding = request.form['feeding']
		prowess = request.form['prowess']
		contamination = request.form['contamination']
		temperature = request.form['temperature']
		water = request.form['water']
		age = request.form['age']
		# check if empty symptoms are submitted
		if seating == '' or feeding == '' or prowess == '' or contamination == '' or temperature == '' or water == '' or age == '':
			msg = 'Please select all factors'
			return render_template('index.html', message = msg)
		else:
			# load dataset
			data = pd.read_csv("factors.csv")
			X = data.drop(columns = ['result'])
			y = data['result']
			# split into testing and training: 20% testing, 80% training
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
			# load model
			model = DecisionTreeClassifier()
			# fit model
			model.fit(X_train,y_train)
			# predict
			predictions =model.predict([[seating, feeding, prowess, contamination, temperature, water, age]])
			
			return render_template('index.html', message =msg, result = predictions)
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True)