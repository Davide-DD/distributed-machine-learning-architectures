from flask import Flask, request
from classes.data_lake import DataLake
from classes.model import Model
from classes.policy import Policy


correct = 0
wrong = 0

dl = DataLake()

model = Model()
model.train(dl.get_training_data())
model.test(dl.get_test_data())

policy = Policy()

app = Flask(__name__)


@app.route("/predict", methods=['POST'])
def predict():
	response = request.get_json()
	dict_data = {'TS1': response['TS1'], 'TS2': response['TS2'], 'TS3': response['TS3'], 'TS4': response['TS4'] }
	data = response['TS1'], response['TS2'], response['TS3'], response['TS4']
	outcome = response['outcome']
		
	dl.add_data(dict_data, outcome)
		
	prediction = model.predict(dl.transform(data))
	print("La predizione e' " + prediction + " e il valore reale e' " + outcome.split()[0])
	if (outcome.split()[0] == prediction):
		global correct
		correct += 1
	else:
		policy.update_status()

		if not policy.is_respected():
			dl.load_data()
			model.train(dl.get_training_data())
	
		global wrong
		wrong += 1
	
	print("Corretti: " + str(correct))
	print("Sbagliati: " + str(wrong))
	
	return prediction


app.run(host='0.0.0.0')