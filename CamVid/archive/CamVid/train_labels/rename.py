import os

# Path to the directory containing the label files
label_dir = r'C:\Users\simon\ikt213g23h\wheely\CamVid\archive\CamVid\val_labels_new'

# Loop through each file in the directory
def rename_files():
    for filename in os.listdir(label_dir):
        if filename.endswith('_L.png'):
            new_filename = filename.replace('_L.png', '.png')
            os.rename(os.path.join(label_dir, filename), os.path.join(label_dir, new_filename))
            print(f'Renamed {filename} to {new_filename}')

# Run the function
rename_files()