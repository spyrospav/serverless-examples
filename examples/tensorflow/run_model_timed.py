"""
Small script to run the regression model as a standalone code for training and testing purposes
"""
import time
IMPORT_START_TIME = time.time()
import ConfigParser
import os
import numpy
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
class TensorFlowRegressionModel:

    def __init__(self, config, is_training=True):
        # store the model variables into a class object
        self.vars = self.set_vars()
        self.model = self.build_model(self.vars)
        # if it is not training, restore the model and store the session in the class
        if not is_training:
            self.sess = self.restore_model(config.get('model', 'LOCAL_MODEL_FOLDER'))

        return

    def set_vars(self):
        """
        Define the linear regression model through the variables
        """
        return {
            # placeholders
            'X': tf.placeholder("float"),
            'Y': tf.placeholder("float"),
            # model weight and bias
            'W': tf.Variable(numpy.random.randn(), name="weight"),
            'b': tf.Variable(numpy.random.randn(), name="bias")
        }

    def build_model(self, vars):
        """
        Define the linear regression model through the variables
        """
        return tf.add(tf.mul(vars['X'], vars['W']), vars['b'])

    def restore_model(self, model_dir):
        sess = tf.Session()
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state(model_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

        return sess

    def train(self, train_X, train_Y, learning_rate, training_epochs, model_output_dir=None):
        n_samples = train_X.shape[0]
        # Mean squared error
        cost = tf.reduce_sum(tf.pow(self.model - self.vars['Y'], 2)) / (2 * n_samples)
        # Gradient descent
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
        # Launch the graph
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver(tf.global_variables())
            # Fit all training data
            for epoch in range(training_epochs):
                for x, y in zip(train_X, train_Y):
                    sess.run(optimizer, feed_dict={self.vars['X']: x, self.vars['Y']: y})
            # Save model locally
            saver.save(sess, model_output_dir + 'model.ckpt')

        return

    def predict(self, x_val):
        return self.sess.run(self.vars['W']) * x_val + self.sess.run(self.vars['b'])


# get config file
HERE = os.path.dirname(os.path.realpath(__file__))
Config = ConfigParser.ConfigParser()
Config.read(HERE + '/settings.ini')
# settings for the training
MODEL_DIR = Config.get('model', 'LOCAL_MODEL_FOLDER')
LEARNING_RATE = float(Config.get('model', 'LEARNING_RATE'))
TRAINING_EPOCHS = int(Config.get('model', 'TRAINING_EPOCHS'))


def main():
    # training data
    train_X = numpy.asarray([3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167,
                             7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1])
    train_Y = numpy.asarray([1.7, 2.76, 2.09, 3.19, 1.694, 1.573, 3.366, 2.596, 2.53, 1.221,
                             2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3])
    # Uncomment here for training again the model
    # r = TensorFlowRegressionModel(Config)
    # r.train(train_X, train_Y, LEARNING_RATE, TRAINING_EPOCHS, MODEL_DIR)
    # make some predictions with the stored model
    test_val = 6.83
    r = TensorFlowRegressionModel(Config, is_training=False)
    y_pred = r.predict(test_val)
    print(y_pred)
    assert y_pred > 2.48 and y_pred < 2.52

    return


if __name__ == "__main__":
    main()