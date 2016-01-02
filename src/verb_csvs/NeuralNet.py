#!/usr/bin/env python
"""Chainer example: train a multi-layer perceptron on MNIST

This is a minimal example to write a feed-forward net. It requires scikit-learn
to load MNIST dataset.

"""
import argparse

import numpy as np
import six

import chainer
from chainer import computational_graph as c
from chainer import cuda
import chainer.functions as F
from chainer import optimizers


import sys



class NN:


	def __init_(self,unit_list):

		self.u1=unit_list[0]
		self.u2=unit_list[1]
		self.u3=unit_list[2]

	# Prepare multi-layer perceptron model
		self.model = chainer.FunctionSet(l1=F.Linear(self.u1,self.u2),
									l2=F.Linear(self.u2, self.u2),
									l3=F.Linear(self.u2, self.u3))

	# Setup optimizer
		optimizer = optimizers.Adam()
		optimizer.setup(self.model)



	def forward(self,x_data, y_data, train=True):
		# Neural net architecture
		x, t = chainer.Variable(x_data), chainer.Variable(y_data)
		h1 = F.dropout(F.relu(self.model.l1(x)),  train=train)
		h2 = F.dropout(F.relu(self.model.l2(h1)), train=train)
		print h2.data
		y = self.model.l3(h2)
		return F.softmax_cross_entropy(y,t), F.accuracy(y, t)




	# Learning loop
	def train(self,x_train,y_train,x_test,y_test,n_epoch=30,batchsize=30):
		xp=np
		for epoch in six.moves.range(1, n_epoch + 1):
			print('epoch', epoch)

			# training
			N=len(x_train)
			perm = np.random.permutation(N)
			sum_accuracy = 0
			sum_loss = 0
			for i in six.moves.range(0, N, batchsize):
				x_batch = xp.asarray(x_train[perm[i:i + batchsize]])
				y_batch = xp.asarray(y_train[perm[i:i + batchsize]])

				self.optimizer.zero_grads()
				loss, acc = self.forward(x_batch, y_batch)
				loss.backward()
				self.optimizer.update()
				"""
				if epoch == 1 and i == 0:
					with open("graph.dot", "w") as o:
						o.write(c.build_computational_graph((loss, )).dump())
					with open("graph.wo_split.dot", "w") as o:
						g = c.build_computational_graph((loss, ),
														remove_split=True)
						o.write(g.dump())
					print('graph generated')
				"""
				sum_loss += float(loss.data) * len(y_batch)
				sum_accuracy += float(acc.data) * len(y_batch)

			print('train mean loss={}, accuracy={}'.format(
				sum_loss / N, sum_accuracy / N))

			# evaluation
			sum_accuracy = 0
			sum_loss = 0
			N_test=len(x_test)
			for i in six.moves.range(0, N_test, batchsize):
				x_batch = xp.asarray(x_test[i:i + batchsize])
				y_batch = xp.asarray(y_test[i:i + batchsize])

				loss, acc = self.forward(x_batch, y_batch, train=False)

				sum_loss += float(loss.data) * len(y_batch)
				sum_accuracy += float(acc.data) * len(y_batch)

			print('test  mean loss={}, accuracy={}'.format(
				sum_loss / N_test, sum_accuracy / N_test))
