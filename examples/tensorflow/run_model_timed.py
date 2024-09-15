"""
Small script to run the regression model as a standalone code for training and testing purposes
"""

import time
IMPORT_START_TIME = time.time()
import configparser
import os
import sys
import numpy

# ask AWS to pick up pre-compiled dependencies from the vendored folder ?
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))

# shutup tensorflow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


import tensorflow as tf  # noqa: E402
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
rng = numpy.random


class TensorFlowRegressionModel:
    def __init__(self, config: configparser.ConfigParser, is_training=True):
        self.W = tf.Variable(rng.randn(), name="weight")
        self.b = tf.Variable(rng.randn(), name="bias")

        self.optimizer = tf.optimizers.SGD(float(config.get("model", "LEARNING_RATE")))
        self.checkpoint = tf.train.Checkpoint(W=self.W, b=self.b)

        if not is_training:
            self.restore_model(config.get("model", "LOCAL_MODEL_FOLDER"))

    def linear_regression(self, x):
        return self.W * x + self.b

    def mean_square(self, y_pred, y_true):
        return tf.reduce_mean(tf.square(y_pred - y_true))

    def restore_model(self, model_dir):
        latest_checkpoint = tf.train.latest_checkpoint(model_dir)
        if latest_checkpoint:
            self.checkpoint.restore(latest_checkpoint).assert_consumed()

    def train(
        self, train_X, train_Y, learning_rate, training_epochs, model_output_dir=""
    ):
        saver = tf.train.CheckpointManager(
            self.checkpoint, model_output_dir, max_to_keep=3
        )
        for epoch in range(training_epochs):
            with tf.GradientTape() as g:
                pred = self.linear_regression(train_X)
                loss = self.mean_square(pred, train_Y)

            # Compute gradients.
            gradients = g.gradient(loss, [self.W, self.b])

            # Update W and b following gradients.
            self.optimizer.apply_gradients(zip(gradients, [self.W, self.b]))

            saver.save()

    def predict(self, x_val):
        return float(self.linear_regression(x_val).numpy())


# get config file
HERE = os.path.dirname(os.path.realpath(__file__))
Config = configparser.ConfigParser()
Config.read(HERE + "/settings.ini")
# settings for the training
MODEL_DIR = Config.get("model", "LOCAL_MODEL_FOLDER")
LEARNING_RATE = float(Config.get("model", "LEARNING_RATE"))
TRAINING_EPOCHS = int(Config.get("model", "TRAINING_EPOCHS"))


def main():
    # training data
    train_X = numpy.asarray(
        [
            3.3,
            4.4,
            5.5,
            6.71,
            6.93,
            4.168,
            9.779,
            6.182,
            7.59,
            2.167,
            7.042,
            10.791,
            5.313,
            7.997,
            5.654,
            9.27,
            3.1,
        ]
    )
    train_Y = numpy.asarray(
        [
            1.7,
            2.76,
            2.09,
            3.19,
            1.694,
            1.573,
            3.366,
            2.596,
            2.53,
            1.221,
            2.827,
            3.465,
            1.65,
            2.904,
            2.42,
            2.94,
            1.3,
        ]
    )
    # Uncomment here for training again the model
    r = TensorFlowRegressionModel(Config)
    r.train(train_X, train_Y, LEARNING_RATE, TRAINING_EPOCHS, MODEL_DIR)
    # make some predictions with the stored model
    test_val = 6.83
    r = TensorFlowRegressionModel(Config, is_training=False)
    y_pred = r.predict(test_val)
    print(y_pred)
    assert y_pred > 2.48 and y_pred < 2.52, f"got {y_pred}"

    return


if __name__ == "__main__":
    main()
