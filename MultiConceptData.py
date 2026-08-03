import numpy as np
import argparse

def default_args(**kwargs):
	parser = argparse.ArgumentParser()
	parser.add_argument("--number-of-examples", default=5000, type=int)
	parser.add_argument("--number-of-copies", default=1, type=int)
	parser.add_argument("--number-of-elements", default=2, type=int)
	parser.add_argument("--noise", default=0.0, type=float)
	args = parser.parse_args()
	for key, value in kwargs.items():
		if key in args.__dict__:
			setattr(args, key, value)
	return args

args = default_args()
 
features = args.number_of_elements*2 # Two concepts represented separately with different elements

X_train = np.zeros((args.number_of_examples, features*args.number_of_copies), dtype=np.uint32)
Y_train = np.zeros(args.number_of_examples, dtype=np.uint32)
for i in range(args.number_of_examples):
	x = np.random.randint(args.number_of_elements, size=(2))

	for j in range(args.number_of_copies):
		X_train[i, j*features + x[0]] = 1
		X_train[i, j*features + args.number_of_elements + x[1]] = 1

	Y_train[i] = np.logical_xor(x[0] % 2, x[1] % 2)

Y_train = np.where(np.random.rand(args.number_of_examples) <= args.noise, 1 - Y_train, Y_train)  # Adds noise

np.savetxt("MultiConceptTrainingData.txt", np.append(X_train, Y_train.reshape((number_of_examples, 1)), axis=1), fmt='%d')

X_test = np.zeros((args.number_of_examples, features*args.number_of_copies), dtype=np.uint32)
Y_test = np.zeros(args.number_of_examples, dtype=np.uint32)
for i in range(args.number_of_examples):
	x = np.random.randint(args.number_of_elements, size=(2))

	for j in range(args.number_of_copies):
		X_test[i, j*features + x[0]] = 1
		X_test[i, j*features + args.number_of_elements + x[1]] = 1

	Y_test[i] = np.logical_xor(x[0] % 2, x[1] % 2)

np.savetxt("MultiConceptTestingData.txt", np.append(X_test, Y_test.reshape((number_of_examples, 1)), axis=1), fmt='%d')

