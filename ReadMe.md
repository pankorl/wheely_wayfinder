# Root directory

## Files
**all of the python files in this directory are obsolete, 
they were used in the early stages of the project when we were figuring out our approach.**

- aruco_marker.png
  - image used in pygame simulation

- mock_RPi.py/RPi.py
  - mock library to simulate using GPiO-pins before we had access to the JetBot

- model2_c_1_UNUSED.h5
  - attempt at reformatting our weights before we had our training script properly set up

- movement_logic.py/movement_test.py
  - script we originally planned to use for movement commands on the JetBot

- slam.py
  - attempt at using SLAM before we knew it wouldn't work


## Folders
- aruco
  - empty

- CamVid
  - Contains the dataset we used for our model
    - all subsets used needed to be converted to grayscale with intensity values of the pixels representing the class index
  - class_dict.csv describes the rgb values of every class index (which we then converted)
  - grayscale.py did the conversion
  - make_binary.py combined all classes except 17 (the road) into one class to make it a binary classification
  - make_01.py made the pixel values either 0 or 1 instead of 0 or 255

- myenv
  - contains the scripts/dependencies used in this project

- **monocular**
  - this contains all the main scripts we ended up using in the end
  - contains separate ReadMe.md