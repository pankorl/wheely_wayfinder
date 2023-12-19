import cv2
from keras.models import load_model
from semSeg import perform_semantic_segmentation
from birdsEye import perform_birds_eye_transformation
from occGrid import create_occupancy_grid
import numpy as np
from keras_segmentation.models import all_models
import tensorflow as tf
import socket
import pickle
import struct
import cv2.aruco as aruco
from marker_handler import MarkerHandlers
import inspect
import zlib
from shared_queue import shared_aruco_queue, shared_obstacle_queue

def wheely_thread():

    stream_camera = False
    use_aruco = True
    use_obs_detect = True


    if use_obs_detect:
        model = all_models.model_from_name['vgg_unet'](n_classes=2, input_height=320, input_width=640)
        # Create a checkpoint object
        checkpoint = tf.train.Checkpoint(model=model)
        # Restore from a checkpoint

        # ch_path = r'C:\Users\simon\ikt213g23h\wheely\monocular\image-segmentation-keras\checkpoints\checkpoints_fixed_numEpochs4.4.index'
        # ch_path = r'C:\Users\simon\ikt213g23h\wheely\monocular\image-segmentation-keras\checkpoints.00005.index'
        ch_path = r'C:\Users\simon\ikt213g23h\wheely\monocular\image-segmentation-keras\checkpoints\checkpoints_binary_class.4.index'
        checkpoint.restore(ch_path).expect_partial()
        
        
        # Birds eye view and road crop for obstacle detection
        # Points in the source image
        # pts1 = np.float32([[130, 100], [190, 100], [0, 160], [320, 160]])
        pts1 = np.float32([[0, 0], [320, 0], [0, 160], [320, 160]])
        # Points in the destination image
        pts2 = np.float32([[0, 0], [320, 0], [0, 160], [320, 160]])

        # Compute the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        # Compute the inverse transformation matrix
        inverse_matrix = cv2.getPerspectiveTransform(pts2, pts1)

    if (not stream_camera):
        # Initialize webcam
        # webcam = cv2.VideoCapture(0)
        webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not webcam.isOpened():
            print("Could not open webcam")
            exit()

    else:
        # Video Client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.66.85', 8089))
        data = b""
        payload_size = struct.calcsize(">L")


    # Class of road pixels
    class_index = 0

    if (use_aruco):
        # Aruco
        # Get the predefined dictionary
        arucoDict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

        detector = aruco.ArucoDetector(arucoDict)

        #Load marker handlers:
        mh = MarkerHandlers()
        handlerFunctions = [func for name, func in inspect.getmembers(mh, inspect.ismethod)]
        current_id = 0


    def capture_frame():
        global data
        global payload_size
        global client_socket
        

        # Retrieve message size
        while len(data) < payload_size:
            data += client_socket.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)
        # frame = frame[:160, :320]
        return frame


    def aruco_func(frame):
        global current_id
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the markers in the image using the ArucoDetector object
        corners, ids, rejectedImgPoints = detector.detectMarkers(image=gray)

        # Check if markers are detected
        if ids is not None:
            # If markers are detected, overlay their ID and outline them in the frame
            aruco.drawDetectedMarkers(frame, corners, ids)
        #Checks if new id detected and executes corresponding handler function
        if ids is not None:
            id = ids[0][0]
            if id != current_id:
                handlerFunctions[id-1]()  
                shared_aruco_queue.put(id)  #Only CHANGE MADE. Use Shared_queue
                current_id = id
        else:
            #Set current_id to 0 current id is removed from frame
            current_id = 0

        return ids


    def is_obstacle_in_front(frame, orig_frame, obstacle_min_size):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

        crop_frame = thresh[10:-20, 30:-30]
        # crop_frame = thresh[: -20, 0:-1]
        # print(crop_frame.shape)

        contours, _ = cv2.findContours(crop_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        obs_pres = False
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Check if the obstacle is in the lower half of the image and meets the minimum size
            if y + h <= crop_frame.shape[0] and w * h >= obstacle_min_size:
            # if True:
                # rect_pts = np.float32([[x+30, y], [x+30 + w, y], [x+30, y + h], [x+30 + w, y + h]])
                rect_pts = np.float32([[x+30 + w, y], [x+30, y], [x+30, y + h], [x+30 + w, y + h]])
                transformed_pts = cv2.perspectiveTransform(np.array([rect_pts]), inverse_matrix)[0]
                cv2.polylines(orig_frame, [np.int32(2*transformed_pts)], True, (0, 0, 255), 2)
                
                obs_pres = True

        return obs_pres, orig_frame


    obs_count = 0
    obs_true_count = 0
    obs_scan_time = 10
    obs_threshold = 0.7
    obs_cooldown = 5
    obs_cooldown_count = 0

    def inc_obs_count(is_obstacle, obs_count, obs_true_count, obs_cooldown_count):
        # global obs_count
        # global obs_true_count
        # global obs_cooldown_count

        if obs_cooldown_count > 0:
            obs_cooldown_count -= 1
            return obs_count, obs_true_count, obs_cooldown_count
        if obs_count == 0:
            if is_obstacle:
                shared_obstacle_queue.put(1)
                print("Stop to check if obstacle")
                obs_true_count += 1
                obs_count += 1
        else:
            if is_obstacle:
                obs_true_count += 1
            obs_count += 1
        if obs_count >= obs_scan_time:
            if obs_true_count/obs_count >= obs_threshold:
                shared_obstacle_queue.put(2)
                print("Navigate obstacle!!!")
                obs_cooldown_count = obs_cooldown
            else:
                shared_obstacle_queue.put(0)
            obs_true_count = 0
            obs_count = 0
        return obs_count, obs_true_count, obs_cooldown_count


    while True:

        if not stream_camera:
            ret, frame = webcam.read()
            if not ret:
                print('Failed to grab frame')
                webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                continue
            frame = frame[-320:, -640:]

        else:
            frame = capture_frame()[-320:, :]

        if use_aruco:
            aruco_ids = aruco_func(frame)


        if aruco_ids is not None:
            obs_count = 0
            obs_true_count = 0
            shared_obstacle_queue.put(0)
        if use_obs_detect and aruco_ids is None:
            # Perform semantic segmentation
            free_space_map = perform_semantic_segmentation(frame, checkpoint.model, class_index)  
            free_space_map = np.reshape(free_space_map, (160, 320))

            free_space_map = free_space_map.astype(np.uint8) * 255
            free_space_map = cv2.cvtColor(free_space_map, cv2.COLOR_GRAY2BGR)

            kernel = np.ones((5,5), np.uint8)
            closed = cv2.morphologyEx(free_space_map, cv2.MORPH_CLOSE, kernel)
            closed_opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

            # cv2.imshow('free_space', free_space_map)
            # cv2.imshow('closed freespace', closed)
            cv2.imshow('closed freespace', closed_opened)

            # print(free_space_map.shape)
            # print(np.any(np.isnan(free_space_map)))
            # print(np.any(np.isinf(free_space_map)))

            # print("Model output shape:", free_space_map.shape)
            # print("Model output type:", type(free_space_map))


            pts1 = np.float32(pts1)
            pts2 = np.float32(pts2)

            # Perform bird's-eye view transformation
            # bird_eye_view = perform_birds_eye_transformation(free_space_map, pts1, pts2, 320, 160)
            bird_eye_view = perform_birds_eye_transformation(closed_opened, pts1, pts2, 320, 160)

            cv2.imshow("bird_eye", bird_eye_view)

            obs_pres, frame = is_obstacle_in_front(bird_eye_view, frame, 900)
            
            obs_count, obs_true_count, obs_cooldown_count = inc_obs_count(obs_pres, obs_count, obs_true_count, obs_cooldown_count)

            # if obs_pres:
            #     print("Obstacle!!")
        
        cv2.imshow('Webcam Feed', frame)

        # Create occupancy grid
        # occupancy_grid = create_occupancy_grid(bird_eye_view)

        # Display the webcam feed
        # cv2.imshow('Webcam Feed', frame)

        # Display the occupancy grid
        # cv2.imshow('Occupancy Grid', occupancy_grid)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if stream_camera:
        client_socket.close()
    else:
        webcam.release()
        
    cv2.destroyAllWindows()
