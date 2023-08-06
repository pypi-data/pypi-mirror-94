import tensorflow as tf
import numpy as np
from PIL import Image
from keras.utils import get_file


model_input_shape = (224, 224)
model = tf.keras.Sequential([
        tf.keras.applications.DenseNet201(weights=None, include_top=False, input_shape=[*model_input_shape, 3]),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(104, activation='softmax')
    ])
model_url = "https://github.com/Bhanuchander210/keras_flower/raw/master/keras_flower_weights.h5"
labels_url = "https://github.com/Bhanuchander210/keras_flower/raw/master/keras_flower_labels.txt"
model_dir = "keras_flower"
model.load_weights(get_file("keras_flower_weights.h5", model_url, cache_subdir=model_dir))
labels = np.loadtxt(get_file("keras_flower_labels.txt", labels_url, cache_subdir=model_dir), dtype='str', delimiter="\n")


def predict(image):
    image = np.array(image)
    image = image / 255.0
    results = model.predict(np.expand_dims(image, axis=0))[0]
    return results


def predict_by_path(act_path):
    img = Image.open(act_path).resize(model_input_shape)
    return predict(img)


def get_label_score(results, top):
    return sorted(zip(labels, results), key=lambda x: x[1], reverse=True)[:top]


def predict_name(image_array, top=1):
    results = predict(image_array)
    return get_label_score(results, top)


def predict_name_by_path(act_path, top=1):
    results = predict_by_path(act_path)
    return get_label_score(results, top)
