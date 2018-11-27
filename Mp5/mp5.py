# ----------------------------------------------------------
#
# THIS CODE IS INCOMPLETE! BUT MAY HELP WHEN GETTING STARTED
#
# ----------------------------------------------------------
import numpy as np
import numpy.linalg as la
import pandas as pd
import math

# Read in the data files
tumor_data_train = pd.io.parsers.read_csv("breast-cancer-train.dat", header=None, names=labels)
tumor_data_test = pd.io.parsers.read_csv("breast-cancer-validate.dat", header=None, names=labels)

# Construct your A matrices
train = np.ndarray(shape=(len(tumor_data_train.values), len(tumor_data_train.values[0]) - 2))
test = np.ndarray(shape=(len(tumor_data_test.values), len(tumor_data_test.values[0]) - 2))

for i in range(len(tumor_data_train)):
    temp = []
    for j in range(len(tumor_data_train.values[0]) - 2):
        temp.append(tumor_data_train.values[i][j + 2])
    train[i] = np.array(temp)

for i in range(len(tumor_data_test)):
    temp = []
    for j in range(len(tumor_data_test.values[0]) - 2):
        temp.append(tumor_data_test.values[i][j + 2])
    test[i] = np.array(temp)

dim1 = 2 * len(subset_labels + math.factorial(len(subset_labels) - 1))
A_quad_train = np.ndarray(shape=(len(tumor_data_train.values), dim1))
dim2 = 2 * len(subset_labels + math.factorial(len(subset_labels) - 1))
A_quad_test = np.ndarray(shape=(len(tumor_data_test.values), dim2))

count = 0
for x in tumor_data_train.columns:
    if x in subset_labels:
        temp = []
        for i in range(len(tumor_data_train)):
            temp.append(tumor_data_train[x][i])
        A_quad_train[:, count] = np.array(temp)
        count += 1

for i in range(len(tumor_data_train)):
    for j in range(len(subset_labels)):
        A_quad_train[i][j + len(subset_labels)] = A_quad_train[i][j] * A_quad_train[i][j]

count = 0
for primary in range(len(subset_labels) - 1):
    for offset in range(len(subset_labels) - primary - 1):
        for i in range(len(tumor_data_train)):
            A_quad_train[i][2 * len(subset_labels) + count] = np.multiply(A_quad_train[i][primary],
                                                                          A_quad_train[i][primary + offset + 1])
        count += 1

count = 0
for x in tumor_data_test.columns:
    if x in subset_labels:
        temp = []
        for i in range(len(tumor_data_test)):
            temp.append(tumor_data_test[x][i])
        A_quad_test[:, count] = np.array(temp)
        count += 1

for i in range(len(tumor_data_test)):
    for j in range(len(subset_labels)):
        A_quad_test[i][j + len(subset_labels)] = A_quad_test[i][j] * A_quad_test[i][j]

count = 0
for primary in range(len(subset_labels) - 1):
    for offset in range(len(subset_labels) - primary - 1):
        for i in range(len(tumor_data_test)):
            A_quad_test[i][2 * len(subset_labels) + count] = np.multiply(A_quad_test[i][primary],
                                                                         A_quad_test[i][primary + offset + 1])
        count += 1

# Construct your b's
b_train = np.zeros(shape=(len(tumor_data_train), 1))

for i in range(len(tumor_data_train)):
    if tumor_data_train.values[i][1] == 'M':
        b_train[i] = 1.0
    else:
        b_train[i] = -1.0

b_test = np.zeros(shape=(len(tumor_data_test), 1))

for i in range(len(tumor_data_test)):
    if tumor_data_test.values[i][1] == 'M':
        b_test[i] = 1.0
    else:
        b_test[i] = -1.0

# Solve the least squares problem
u, sigma, vt = np.linalg.svd(train, full_matrices=False)
u2, sigma2, vt2 = np.linalg.svd(A_quad_train, full_matrices=False)
sigma = np.diag(sigma)
sigma2 = np.diag(sigma2)

weights_linear = vt.T @ la.inv(sigma) @ np.transpose(u) @ b_train
weights_quad = vt2.T @ la.inv(sigma2) @ np.transpose(u2) @ b_train

fp_linear = 0
fn_linear = 0

new_b_lin = test @ weights_linear

# See how well your model (i.e. weights) does on the validate data set
for i in range(len(new_b_lin)):
    if new_b_lin[i] > 0:
        if b_test[i] == -1.0:
            fp_linear += 1
    elif new_b_lin[i] < 0:
        if b_test[i] == 1.0:
            fn_linear += 1

fp_quad = 0
fn_quad = 0
new_b_quad = A_quad_test @ weights_quad
for i in range(len(new_b_quad)):
    if new_b_quad[i] > 0:
        if b_test[i] == -1.0:
            fp_quad += 1
    elif new_b_quad[i] < 0:
        if b_test[i] == 1.0:
            fn_quad += 1

weights_linear = weights_linear.reshape((weights_linear.shape[0],))
weights_quad = weights_quad.reshape((weights_quad.shape[0],))

# Plot a bar graph of the false-positives and false-negatives
bar_graph(fp_linear, fn_linear, fp_quad, fn_quad)