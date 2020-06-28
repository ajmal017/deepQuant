import pandas
import numpy
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import matplotlib.pyplot as plt

CONST_TRAINING_SEQUENCE_LENGTH = 60
CONST_TESTING_CASES = 5

def dataNormalization(data):
	return [(datum-data[0])/data[0] for datum in data]

def dataDeNormalization(data, base):
	return [(datum+1)*base for datum in data]

def getDeepLearningData(ticker, folder):
	# Load data
	# Read csv data into a DataFrame, the first row of the data will be keys
	# Note: do not add space between keys like 'high, low, close'
	# data = pandas.read_csv('../02. Data/01. IntradayUS/'+ticker+'.csv')['close'].tolist()
	path = folder + './'+ticker+'.csv'
	data = pandas.read_csv(path)['close'].tolist()

	# Build training data
	dataTraining = []
	# choose data using starting index between 0 to index len(data) - 300
	# for starting index i, data in range (i:i+61) will be selected as
	# a data segment, the segment size is 61
	# the first 60 elements will be used as X, the last one will be used as Y
	for i in range(len(data) - CONST_TESTING_CASES*CONST_TRAINING_SEQUENCE_LENGTH):
		dataSegment = data[i:i+CONST_TRAINING_SEQUENCE_LENGTH+1]
		dataTraining.append(dataNormalization(dataSegment))

	# dataTraining has 'len(data) - 300' arrays/rows
	# each array has size of 61
	dataTraining = numpy.array(dataTraining)
	# print((dataTraining))

	# shuffle the data to ensure randomness
	# better results will achieved after removing shuffling
	numpy.random.shuffle(dataTraining)

	# X_Training has has 'len(data) - 300' arrays/roww, each row size:60
	# X_Training has has 'len(data) - 300' arrays/roww, each row size:1
	X_Training = dataTraining[:,:-1]
	Y_Training = dataTraining[:,-1]

	# print(len(X_Training))
	# print(len(Y_Training))
	# print(X_Training[0])
	# print(Y_Training[0])

	# Build testing data
	X_Testing = []
	Y_Testing_Base = []
	# The rest 300 data will be used as testing data
	# Each data segment has size of 60
	# X_Testing has 5 arrays/rows, each row size is 60
	# First data element for each row will be used for normalization
	for i in range(CONST_TESTING_CASES, 0, -1):
		dataSegment = data[-(i+1)*CONST_TRAINING_SEQUENCE_LENGTH: -i*CONST_TRAINING_SEQUENCE_LENGTH]
		Y_Testing_Base.append(dataSegment[0])
		X_Testing.append(dataNormalization(dataSegment))

	# Y_Testing has size of 300
	# X: 60, 60, 60, 60, 60
	# Y: 60  60  60  60  60
	# So there will be 300 different precition runs
	# For each row in X, it will predict the next 60 stock price
	# You may think the prediction is like sliding a window over X,
	# and the window size is 60.
	Y_Testing = data[-CONST_TESTING_CASES*CONST_TRAINING_SEQUENCE_LENGTH:]

	X_Testing = numpy.array(X_Testing)
	Y_Testing = numpy.array(Y_Testing)

	# print(len(X_Testing[0]))
	# print(len(Y_Testing))

	# Reshape for deep learning
	X_Training = numpy.reshape(X_Training, (X_Training.shape[0], X_Training.shape[1], 1))
	X_Testing = numpy.reshape(X_Testing, (X_Testing.shape[0], X_Testing.shape[1], 1))

	return X_Training, Y_Training, X_Testing, Y_Testing, Y_Testing_Base


def predict(model, X):
	predictionsNormalized = []

	for i in range(len(X)):
		data = X[i]
		# if(i == 0):
		# 	print("data: ", data)
		# 	print("data len: ", len(data))
		result = []

		for j in range(CONST_TRAINING_SEQUENCE_LENGTH):
			input_data = data[numpy.newaxis, :, :]
			# print("input_data: ", input_data)
			# return
			predicted = model.predict(data[numpy.newaxis, :, :])[0, 0]
			result.append(predicted)
			data = data[1:]
			data = numpy.insert(data, [CONST_TRAINING_SEQUENCE_LENGTH-1], predicted, axis=0)

		predictionsNormalized.append(result)

	return predictionsNormalized


def plotResults(Y_Hat, Y):
	plt.plot(Y)

	for i in range(len(Y_Hat)):
		padding= [None for _ in range(i*CONST_TRAINING_SEQUENCE_LENGTH)]
		plt.plot(padding + Y_Hat[i])
		# plt.plot(Y_Hat[i])

	plt.show()

def predictLSTM(ticker):
	# Load data
	# getDeepLearningData(ticker)
	data_path = "../../data/intra_day_price/"
	(X_Training, Y_Training, X_Testing, 
	 Y_Testing, Y_Testing_Base) = getDeepLearningData(ticker, data_path)
	print(Y_Testing)

	# Build models
	model = Sequential()

	model.add(LSTM(input_dim=1,
		# output_dim=50,
		return_sequences=True,
		units=50,
		))
	model.add(Dropout(0.2))

	model.add(LSTM(200,
		return_sequences=False,
		))
	model.add(Dropout(0.2))

	model.add(Dense(units=1))
	model.add(Activation('linear'))

	model.compile(loss='mse', optimizer='rmsprop')

	# Train models
	model.fit(X_Training, Y_Training, 
		batch_size=512,
		epochs=5,
		validation_split=0.1
		)

	# Predict
	predictionNormalized = predict(model, X_Testing)

	print(predictionNormalized)

	# return

	# De-normalize
	predictions = []
	for i, row in enumerate(predictionNormalized):
		predictions.append(dataDeNormalization(row, Y_Testing_Base[i]))

	# Plot
	plotResults(predictions, Y_Testing)

predictLSTM('NVDA')