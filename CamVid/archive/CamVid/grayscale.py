import cv2
import numpy as np
import pandas as pd
import os

# Load the class_dict.csv
class_dict = pd.read_csv('C:\\Users\\simon\\ikt213g23h\\wheely\\CamVid\\archive\\CamVid\\class_dict.csv')

# Create a mapping from RGB to class index
rgb_to_index = {}
for i, row in class_dict.iterrows():
    rgb_to_index[tuple(row[['r', 'g', 'b']])] = i


# Path to the folder containing label images
label_folder = 'C:/Users/simon/ikt213g23h/wheely/CamVid/archive/CamVid/val_labels'

# Path to the folder to save converted label images
output_folder = 'C:\\Users\\simon\\ikt213g23h\\wheely\\CamVid\\archive\\CamVid\\val_labels_new'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each label image
for filename in os.listdir(label_folder):
    if filename.endswith('.png'):
        img_path = os.path.join(label_folder, filename)
        img = cv2.imread(img_path)
        
        # Create an empty array to store class indices
        h, w, _ = img.shape
        class_idx_img = np.zeros((h, w), dtype=np.uint8)
        
        # Convert RGB to class index
        for i in range(h):
            for j in range(w):
                rgb = tuple(img[i, j])
                class_idx_img[i, j] = rgb_to_index.get(rgb, 0)  # Default to 0 if RGB not found
        
        # Save the converted image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, class_idx_img)

print('Label conversion completed.')