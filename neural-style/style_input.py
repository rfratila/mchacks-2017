
import tensorflow as tf
from os import path, listdir


def read_jpg(filename_queue):
    reader = tf.WholeFileReader(name='file_reader')
    key, record_string = reader.read(filename_queue)
    example = tf.image.decode_jpeg(record_string, name='decode_jpeg')

    # Cast and reshape (This assumes the images are 224 * 224 * 3).
    example = tf.cast(tf.reshape(example, shape=(224, 224, 3)),
                      dtype=tf.float32, name='image_input')
    label = tf.constant(0, dtype=tf.uint8)
    return example, label


def style_input(train_image_dir, batch_size, min_after_dequeue=5, read_threads=1, num_epochs=None):
    train_filenames = [path.join(train_image_dir, f) for f in listdir(train_image_dir)]
    train_filenames = tf.constant(train_filenames, name='filenames')

    train_queue = tf.train.string_input_producer(train_filenames,
                                                 shuffle=True)
    train_example = read_jpg(train_queue)

    capacity = min_after_dequeue + 3 * batch_size

    train_batch = tf.train.shuffle_batch(train_example, batch_size=batch_size,
                                         capacity=capacity, num_threads=read_threads, min_after_dequeue=min_after_dequeue)

    return train_batch