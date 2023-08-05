
import numpy as np
from tensorflow import tensordot, concat, sin, cos
from tensorflow.python import keras as k
from tensorflow.python.util.tf_export import keras_export
from tensorflow.python.keras import initializers
from tensorflow.python.keras.utils import tf_utils


@keras_export('keras.layers.FourierFeature')
class FourierFeature(k.layers.Layer):

    def __init__(self, w=10, **kwargs):
        super(FourierFeature, self).__init__(**kwargs)
        if isinstance(w, int):
            w = 2*np.pi/np.random.rand(w)
        else:
            assert isinstance(w, np.ndarray)
        self.frequencies = w.flatten()
        self.num_features = w.size

    @tf_utils.shape_type_conversion
    def build(self, input_shape):
        param_shape = list(input_shape[1:])
        assert param_shape == [1]
        w = self.frequencies.reshape(param_shape + [self.num_features])
        self.frequencies = k.backend.cast_to_floatx(w)
        self.built = True

    def call(self, inputs):
        xs = tensordot(inputs, self.frequencies, axes=1)
        return concat([sin(xs), cos(xs)], axis=-1)

    def get_config(self):
        config = {
            'frequencies': initializers.serialize(self.frequencies),
        }
        base_config = super(FourierFeature, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return [self.num_features]

