import random
from copy import deepcopy
from collections import deque

import numpy as np

from tensorflow.keras.activations import relu, tanh
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

class DQNAgent:

	def __init__(self, inputSize, outputSize):
		self.inputSize = inputSize
		self.outputSize = outputSize

		# What the agent did and what reward it got
		self.memory = deque(maxlen = 2000)

		# Discount factor on future values
		self.gamma = 0.99

		# Chance that it will take a random action
		self.epsilon = 1.0
		self.epsilonDecay = 0.995
		self.epsilonMinimum = 0.01

		# The amount that the weights in the neural network are updated by each time we train
		self.learningRate = 0.001

		# Create the neural network
		self.policyNetwork = self.createModel()
		self.targetNetwork = self.createModel()
		self.targetNetwork.set_weights(self.policyNetwork.get_weights())

	def createModel(self):
		"""
		Creates the model for the policy and target networks.

		Returns:
			Sequential: Compiled model.
		"""
		model = Sequential()
		model.add(Dense(32, input_dim = self.inputSize, activation = tanh))
		model.add(Dense(64, activation = tanh))
		model.add(Dense(32, activation = tanh))
		model.add(Dense(self.outputSize, activation = tanh))
		model.compile(loss = "mse", optimizer = Adam(lr = self.learningRate))
		return model

	def remember(self, state, nextState, action, reward, done):
		self.memory.append((state, nextState, action, reward, done))

	def act(self, state):
		"""
		Predicts or randomly selects an output based on output size.

		Arguments:
			state (np.array): State of the game (a.k.a. inputs).

		Returns:
			int: The agent's decision (output index).
		"""
		if random.random() <= self.epsilon:
			# Exploration of knowledge
			return random.randrange(self.outputSize)
		# Exploitation of existing knowledge
		return np.argmax(self.policyNetwork.predict(state)[0])

	def replay(self, batchSize):
		"""
		Train the neural network based on examples from the memory.

		Arguments:
			batchSize (int): How many random samples should be used.
		"""
		batch = random.sample(self.memory, batchSize)
		
		for state, nextState, action, reward, done in batch:
			target = reward
			if not done:
				target = (reward + self.gamma * np.amax(self.targetNetwork.predict(nextState)[0]))
			targetF = self.targetNetwork.predict(state)
			targetF[0][action] = target

			self.targetNetwork.fit(state, targetF, epochs = 1, verbose = 0)

		if self.epsilon > self.epsilonMinimum:
			self.epsilon *= self.epsilonDecay

	def load(self, name):
		"""
		Loads the model weights.
		Wrapper function for Tensorflow method.

		Arguments:
			name (str): File path of the model weights to be loaded.
		"""
		self.policyNetwork.load_weights(name)

	def save(self, name):
		"""
		Saves the model weights.
		Wrapper function for Tensorflow method.

		Arguments:
			name (str): File path where the model weights should be saved.
		"""
		self.policyNetwork.save_weights(name)