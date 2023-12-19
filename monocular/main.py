from wheely import wheely_thread
from pygame_demo import pygame_thread
import threading



opencv_thread = threading.Thread(target=wheely_thread)
pygame_thread = threading.Thread(target=pygame_thread)


opencv_thread.start()
pygame_thread.start()


opencv_thread.join()
pygame_thread.join()