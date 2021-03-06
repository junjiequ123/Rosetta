import os
import csv
import tensorflow as tf
import numpy as np
from util import read_dataset
import argparse

np.set_printoptions(suppress=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

np.random.seed(0)


# ################################################## Args
parser = argparse.ArgumentParser(description="Rosetta Linear Regression")
parser.add_argument('--dims', type=int, help="dims", default=5)
parser.add_argument('--epochs', type=int, help="epochs", default=10)
args, unparsed = parser.parse_known_args()
# ##################################################
EPOCHES = args.epochs
DIM_NUM = args.dims

learning_rate = 0.0002
BATCH_SIZE = 5
DIS_STEP = 5

# real data
# ######################################## difference from mpc
prefix = '../playground/datasets/'
file_name_prefix = prefix + str(DIM_NUM) + "D/" + str(DIM_NUM) + "d"
real_X = read_dataset(file_name_prefix + "_attr_plain.csv")
real_Y = read_dataset(file_name_prefix + "_label_plain.csv")
# ######################################## difference from mpc

X = tf.Variable(real_X, dtype=tf.float64)
Y = tf.Variable(real_Y, dtype=tf.float64)
print(X)
print(Y)

# initialize W & b
W = tf.Variable(tf.zeros([DIM_NUM, 1], dtype=tf.float64))
b = tf.Variable(tf.zeros([1], dtype=tf.float64))
print(W)
print(b)

# predict
pred_Y = tf.matmul(X, W) + b
print(pred_Y)

# loss
loss = tf.reduce_mean(tf.square(Y - pred_Y))
print(loss)

# optimizer
train = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
print(train)

# save
# dtype=double
saver = tf.train.Saver(var_list=None, max_to_keep=5, name='v2')
os.makedirs("./log/ckpt", exist_ok=True)

init = tf.global_variables_initializer()
print(init)


# restore mpc's model and predict
with tf.Session() as sess:
    sess.run(init)
    if os.path.exists("./log/ckpt/checkpoint"):
        saver.restore(sess, './log/ckpt/model')

    # predict
    Y_pred = sess.run(pred_Y)
    print("Y_pred:", Y_pred)
