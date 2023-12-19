# Main project folder

## Folders
- image-segmentation-keras
  - empty

## Files
- main.py
  - **run this file to run the demo project**
  - starts the threads for wheely.py and pygame_demo.py

- wheely.py
  - contains everything to do with image processing
  - **initialisation:**
    - loads weights
    - initialises values for cropping/stretching the "road" (currently set to not stretch at all)
    - initialises camera input, either for streaming from a JetBot, or for using a webcam
    - initialises aruco detection
  - **helper functions:**
    - capture_frame()
      - captures frame from the client socket when camera feed is being streamed from JetBot
    - aruco_func()
      - uses aruco detector to see if any known aruco markers are present in the input image
    - is_obstacle_in_front()
      - finds contours of every connected black pixels in closed image
      - filters the contours based on a minimum size
      - draws rectangles around contours that are big enough onto the original input image (this is where inverse_matrix for stretching is used, so it "un-stretches" the rectangles when stretching is used)
    - inc_obs_count()
      - counts frames where obstacle is present in image, to see if it is present for 7/10 frames or not. if it is, it is counted as an obstacle and not a false positive
      - keeps track of cooldown so the same obstacle isn't immediately recognised again (necessary for the demo)
  - **main loop:**
    - captures a frame
    - checks for aruco markers
    - does semantic segmentation
      - runs input image through model
      - closing
      - opening
      - stretching
      - runs is_obstacle_in_front()
      - runs inc_obs_count()
- webcamtest.py used for testing webcam
- videoClient.py used for testing streamed videofeed
- trash.py used for pasting code
- shared_queue.py used by pygame_demo.py to use the same queue in wheely.py
- semSeg.py contains function to run semantic segmentation with our weights, used in wheely.py
- **pygame_demo.py**
  - pygame simulation script
  - **run this script to play with simulation without camera and with keyboard input**
    - keyboard input:
      - 2, 3, 4, 5 for different movement commands
      - o for triggering potential obstacle
        - y for confirming obstacle
        - n for cancelling obstacle
- occGrid.py is obsolete, was going to be used to make a black/white grid, but it already is with the binary classifier
- marker_handler.py was supposed to be handler functions for the different aruco markers to be sent to JetBot
- mainnb.ipynb is obsolete, was used to potentially run the demo in a notebook for efficiency and not having to spend time on loading weights under demo, but it ended up being quick anyways
- load_test.py/load_test_2.py/load_stuff.py was used to figure out how to load model weights
- gstream_thing.py was an attempt at using gstreamer to stream camera feed from JetBot, but we ended up just using a web socket and the pickle library
- classes.txt contains some info about the different classes in the original CamVid dataset
- birdsEye.py contains function for stretching our closed image