"""
Little Script which shows how to read a position from the TCP API
"""
# !/usr/bin/env python

from pyniryo import NiryoRobot

# Connecting to robot
niryo_robot = NiryoRobot(ip_address="192.168.1.15")

niryo_robot.calibrate_auto()

obj_pose = niryo_robot.get_target_pose_from_rel("workspace_1", height_offset=0.0,
                                                x_rel=0.2, y_rel=0.6, yaw_rel=1.57)

niryo_robot.move_pose(obj_pose)

# niryo_robot.set_learning_mode(True)

niryo_robot.close_connection()
