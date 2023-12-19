import os
import numpy as np
from PIL import Image
from tqdm import tqdm

# Paths
source_folder = r'C:\Users\simon\ikt213g23h\wheely\CamVid\archive\CamVid\val_labels_new'
target_folder = r'C:\Users\simon\ikt213g23h\wheely\CamVid\archive\CamVid\val_labels_binary'

# Class index to isolate
specific_class_index = 17  # Replace with the index of the specific class you want to isolate

# Create target folder if it doesn't exist
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# Process each label image
for filename in tqdm(os.listdir(source_folder)):
    if filename.endswith('.png'):  # Assuming label images are in PNG format
        file_path = os.path.join(source_folder, filename)
        image = Image.open(file_path)
        image_array = np.array(image)

        # Create a binary mask
        binary_mask = (image_array == specific_class_index).astype(np.uint8) * 255

        # Save the binary mask
        Image.fromarray(binary_mask).save(os.path.join(target_folder, filename))