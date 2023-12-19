import tensorflow as tf
import numpy as np
import cv2
from keras_segmentation.pretrained import pspnet_50_ADE_20K

def perform_semantic_segmentation(frame, model, class_index):
    # Load a pre-trained semantic segmentation model
    # model = pspnet_50_ADE_20K()
    # model = tf.keras.models.load_model(model_path)

    # Read the image
    # image = cv2.imread(image_path)

    # Preprocess the image
    input_image = cv2.resize(frame, (640, 320))
    input_image = np.expand_dims(input_image, axis=0)

    # Perform semantic segmentation
    # output = model.predict_segmentation(input_image, out_fname="out.png")
    output = model.predict(input_image) 
    

    # Post-process the output to get the class with the highest probability for each pixel
    class_map = np.argmax(output[0], axis=-1)
    class_map = class_map.reshape((160, 320))

    normalized_class_map = cv2.normalize(class_map, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Show the image
    # cv2.imshow('Class Map', normalized_class_map*8)
    # Identify free space (assuming class index for 'Road' is 0)
    free_space_map = (class_map == class_index)
    free_space_map = free_space_map.reshape((160, 320))


    return free_space_map