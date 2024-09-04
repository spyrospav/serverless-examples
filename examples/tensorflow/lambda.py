import os
import sys
import json
import ConfigParser

"""
This is needed so that the script running on AWS will pick up the pre-compiled dependencies
from the vendored folder
"""
HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "vendored"))

"""
Now that the script knows where to look, we can safely import our objects
"""
# refactored from the examples at https://github.com/aymericdamien/TensorFlow-Examples
import tensorflow as tf
import numpy

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

"""
Declare here global objects living across requests
"""
# use Pythonic ConfigParser to handle settings
Config = ConfigParser.ConfigParser()
Config.read(HERE + '/settings.ini')
# instantiate the tf_model in "prediction mode"
tf_model = TensorFlowRegressionModel(Config, is_training=False)
# just print a message so we can verify in AWS the loading of dependencies was correct
print("loading done!")


def validate_input(input_val):
    """
    Helper function to check if the input is indeed a float

    :param input_val: the value to check
    :return: the floating point number if the input is of the right type, None if it cannot be converted
    """
    try:
        float_input = float(input_val)
        return float_input
    except ValueError:
        return None


def get_param_from_url(event, param_name):
    """
    Helper function to retrieve query parameters from a Lambda call. Parameters are passed through the
    event object as a dictionary.

    :param event: the event as input in the Lambda function
    :param param_name: the name of the parameter in the query string
    :return: the parameter value
    """
    params = event['queryStringParameters']
    return params[param_name]


def return_lambda_gateway_response(code, body):
    """
    This function wraps around the endpoint responses in a uniform and Lambda-friendly way

    :param code: HTTP response code (200 for OK), must be an int
    :param body: the actual content of the response
    """
    return {"statusCode": code, "body": json.dumps(body)}


def lambda_handler(event, context):
    """
    This is the function called by AWS Lambda, passing the standard parameters "event" and "context"
    When deployed, you can try it out pointing your browser to

    {LambdaURL}/{stage}/predict?x=2.7

    where {LambdaURL} is Lambda URL as returned by serveless installation and {stage} is set in the
    serverless.yml file.

    """
    try:
        param = get_param_from_url(event, 'x')
        x_val = validate_input(param)
        if x_val:
            value = tf_model.predict(x_val)
        else:
            raise "Input parameter has invalid type: float expected"
    except Exception as ex:
        error_response = {
            'error_message': "Unexpected error",
            'stack_trace': str(ex)
        }
        return return_lambda_gateway_response(503, error_response)

    return return_lambda_gateway_response(200, {'value': value})