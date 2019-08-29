import tensorflow as tf

# swish activation


class Swish(tf.keras.layers.Activation):

    def __init__(self, activation, **kwargs):
        super(Swish, self).__init__(activation, **kwargs)
        self.__name__ = 'swish'


def swish(x):
    return (tf.keras.backend.sigmoid(x) * x)

# mean iou as a metric


def mean_iou(y_true, y_pred):
    y_pred = tf.round(y_pred)
    intersect = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(
        y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    smooth = tf.ones(tf.shape(intersect))
    return tf.reduce_mean((intersect + smooth) / (union - intersect + smooth))


# define model
def create_network(input_size, channels, n_blocks=2, depth=4):
    # input
    inputs = tf.keras.Input(shape=(input_size, input_size, 1))
    x = tf.keras.layers.Conv2D(
        channels, 3, padding='same', use_bias=False)(inputs)
    # residual blocks
    for d in range(depth):
        channels = channels * 2
        x = create_downsample(channels, x)
        for b in range(n_blocks):
            x = create_resblock(channels, x)
    # output
    x = tf.keras.layers.BatchNormalization(momentum=0.9)(x)
    x = tf.keras.layers.Activation('swish')(x)
    x = tf.keras.layers.Conv2D(1, 1, activation='sigmoid')(x)
    outputs = tf.keras.layers.UpSampling2D(2**depth)(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def create_downsample(channels, inputs):
    x = tf.keras.layers.BatchNormalization(momentum=0.9)(inputs)
    x = tf.keras.layers.Activation('swish')(x)
    x = tf.keras.layers.Conv2D(channels, 1, padding='same', use_bias=False)(x)
    x = tf.keras.layers.MaxPool2D(2)(x)
    return x


def create_resblock(channels, inputs):
    x = tf.keras.layers.BatchNormalization(momentum=0.9)(inputs)
    x = tf.keras.layers.Activation('swish')(x)
    x = tf.keras.layers.Conv2D(channels, 3, padding='same', use_bias=False)(x)
    x = tf.keras.layers.BatchNormalization(momentum=0.9)(x)
    x = tf.keras.layers.Activation('swish')(x)
    x = tf.keras.layers.Conv2D(channels, 3, padding='same', use_bias=False)(x)
    return tf.keras.layers.add([x, inputs])
