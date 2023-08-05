import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers import Dense


class GlobalAttentionPooling1D(Layer):
    """
    An implementation of the encoder module presented by Geng et. al. in
    "Induction Networks for Few-Shot Text Classification" (2019). It is a block of layers that
    takes in a sequence of embeddings and uses self attention to embed them down into a single
    embedding, summarizing/pooling across the time steps of the sequence.

    Can be used in place of for example `tf.keras.layers.GlobalAveragePooling1D` but assumes
    that `data_format=="channels_last"`.
    """

    def __init__(self, units: int):
        super().__init__()
        self.units = units
        self.W1 = Dense(self.units)  # (units, seq_len)
        self.W2 = Dense(1)  # (1, units)

    def call(self, inputs, training):
        # `inputs` has dims: (batch_size, seq_len, hidden_size)

        # The attention weights. One weight for each element in the sequence.
        A = tf.nn.softmax(self.W2(tf.math.tanh(self.W1(inputs))), axis=-2)  # (batch_size, seq_len, 1)
        # Take a learned convex combination of the sequence's vectors, collapsing it into
        # a single learned embedding vector for the whole sequence.
        E = tf.math.reduce_sum(A * inputs, axis=-2)  # (batch_size, hidden_size)
        return E

    def get_config(self) -> dict:
        return {"units": self.units}
