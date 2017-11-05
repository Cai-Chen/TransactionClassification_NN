import tensorflow as tf
import inputData
import json

import os
# Log level
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def main(testData):
    # parameters
    learning_rate = 0.01
    training_epochs = 56
    testing_epochs = 1
    batch_size = 100
    display_step = 1

    # Network Parameters
    n_hidden_1 = 100      # 1st layer number of features
    n_hidden_2 = 100       # 2nd layer number of features

    n_classes = 23         # Categories

    # Get vocabulary and training data
    # Vocabulary list
    # Create a json file containing the description
    with open('./test.json', 'w', encoding='utf-8') as dump_f:
        json.dump([{'title' : testData}], dump_f)

    vocabDir = ['./trainingData.json', './test.json']
    input_data = inputData.InputData('./trainingData.json', './test.json', vocabDir, './category.json')
    input_data.getTrainDataAndLabel()

    n_input = len(input_data.vocab.vocab)  # Words in vocab

    # Get testing data
    input_data.getTestData()

    input_tensor = tf.placeholder(tf.float32,[None, n_input], name="input")
    output_tensor = tf.placeholder(tf.float32,[None, n_classes], name="output")

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
    }

    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }

    # dropout probability
    keep_prob = tf.placeholder(tf.float32)

    def multilayer_perceptron(input_tensor, weights, biases):
        layer_1_multiplication = tf.matmul(input_tensor, weights['h1'])
        layer_1_addition = tf.add(layer_1_multiplication, biases['b1'])
        layer_1 = tf.nn.relu(layer_1_addition)

        # Hidden layer with RELU activation
        layer_2_multiplication = tf.matmul(layer_1, weights['h2'])
        layer_2_addition = tf.add(layer_2_multiplication, biases['b2'])
        layer_2 = tf.nn.relu(layer_2_addition)

        # dropout
        layer_2_drop = tf.nn.dropout(layer_2, keep_prob)

        # Output layer
        out_layer_multiplication = tf.matmul(layer_2_drop, weights['out'])
        out_layer_addition = out_layer_multiplication + biases['out']

        return out_layer_addition

    # Construct model
    prediction = multilayer_perceptron(input_tensor, weights, biases)

    # Define loss and optimizer
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=output_tensor))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # Train
    for epoch in range(training_epochs):
        batch_xs, batch_ys = input_data.get_train_batch(batch_size)
        sess.run(optimizer, feed_dict={input_tensor: batch_xs, output_tensor: batch_ys, keep_prob: 1})

    # Test (Currently use the training data)
    correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(output_tensor, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(sess.run(accuracy, feed_dict={input_tensor: batch_xs, output_tensor: batch_ys, keep_prob: 1}))

    # Test
    batch_xs = input_data.get_test_batch(1)
    test_prediction = tf.argmax(prediction, 1)
    category_id = sess.run(test_prediction, feed_dict={input_tensor : batch_xs, keep_prob: 1})[0]
    print (input_data.get_category_byID(category_id))
    return input_data.get_category_byID(category_id)

if __name__ == '__main__':
    main('Better Pharmacy')
