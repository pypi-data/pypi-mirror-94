import tensorflow as tf
import numpy as np

from packages.abstractMLBaseModel import abstractMLBaseModel

class neuralNetworkModel(abstractMLBaseModel):
    
    def __init__(self):
        self.modelName = "Neural Network with 3 layers"
        self.epochs = 10;
        self.batch_size = 100;
        self.classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        self.W1 = tf.Variable(tf.random.normal([784, 300], stddev=0.03), name='W1');
        self.b1 = tf.Variable(tf.random.normal([300]), name='b1');
        
        self.W2 = tf.Variable(tf.random.normal([300, 10], stddev=0.03), name='W2');
        self.b2 = tf.Variable(tf.random.normal([10]), name='b2');
        self.optimizer = tf.keras.optimizers.Adam()
    
    def train(self, x_train, y_train, x_test, y_test):
        total_batch = int(len(y_train) / self.batch_size);
        for epoch in range(self.epochs):
            avg_loss = 0
            for i in range(total_batch):
                batch_x, batch_y = self.get_batch(x_train, y_train)
                # create tensors
                batch_x = tf.Variable(batch_x)
                batch_y = tf.Variable(batch_y)
                # create a one hot vector
                batch_y = tf.one_hot(batch_y, 10)
                with tf.GradientTape() as tape:
                    logits = self.predictInClass(batch_x)
                    loss = self.loss_fn(logits, batch_y)
                gradients = tape.gradient(loss, [self.W1, self.b1, self.W2, self.b2])
                self.optimizer.apply_gradients(zip(gradients, [self.W1, self.b1, self.W2, self.b2]))
                avg_loss += loss / total_batch
            test_logits = self.predictInClass(x_test)
            max_idxs = tf.argmax(test_logits, axis=1)
            test_acc = np.sum(max_idxs.numpy() == y_test) / len(y_test)
            print(f"Epoch: {epoch + 1}, loss={avg_loss:.3f}, test set      accuracy={test_acc*100:.3f}%")
        print("\nTraining complete!")
        
    def predict(self, x_input):
        # flatten the input image from 28 x 28 to 784
        x_input = tf.reshape(x_input, (x_input.shape[0], -1))
        x = tf.add(tf.matmul(tf.cast(x_input, tf.float32), self.W1), self.b1)
        x = tf.nn.relu(x)
        logits = tf.add(tf.matmul(x, self.W2), self.b2)
        max_idxs = tf.argmax(logits, axis=1)
        result = max_idxs.numpy()
        return result
    
    def predictInClass(self, x_input):
        # flatten the input image from 28 x 28 to 784
        x_input = tf.reshape(x_input, (x_input.shape[0], -1))
        x = tf.add(tf.matmul(tf.cast(x_input, tf.float32), self.W1), self.b1)
        x = tf.nn.relu(x)
        logits = tf.add(tf.matmul(x, self.W2), self.b2)
        return logits
        
    def get_batch(self, x_data, y_data):
        idxs = np.random.randint(0, len(y_data), self.batch_size)
        return x_data[idxs,:,:], y_data[idxs]
    
    def loss_fn(self, logits, labels):
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels,
                                                                                  logits=logits))
        return cross_entropy