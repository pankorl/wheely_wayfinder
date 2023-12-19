import cv2
import os
import numpy as np

input_folder = 'C:\\Users\\simon\\ikt213g23h\\wheely\\CamVid\\archive\\CamVid\\val_labels_binary'
output_folder = 'C:\\Users\\simon\\ikt213g23h\\wheely\\CamVid\\archive\\CamVid\\val_labels_binary_converted'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.png'):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Read the image in grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Convert pixel values: 255 -> 1, others remain 0
        image = (image == 255).astype(np.uint8)
        
        # Save the converted image
        cv2.imwrite(output_path, image)

print("Conversion completed.")
