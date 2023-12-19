#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import time
from movement_logic import *

# Your existing movement functions here

# Callback for RTAB-Map's pose estimates
def pose_callback(msg):
    # Extract pose information
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    # Navigation logic based on pose
    # E.g., call drive_forward() or rotate()

# Callback for camera feed
def image_callback(msg):
    # This can be left empty if you're using RTAB-Map for SLAM,
    # as RTAB-Map will handle SLAM internally.
    pass

def main():
    rospy.init_node('wheely_wayfinder')

    # Subscribe to RTAB-Map's pose topic
    print(30)
    pose_sub = rospy.Subscriber('/rtabmap/odom', Odometry, pose_callback)

    # Subscribe to camera feed if needed
    image_sub = rospy.Subscriber('/camera/image_raw', Image, image_callback)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Your periodic code here, if any
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
