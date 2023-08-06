# Imports
from pyniryo import *

# - Constants
workspace_name = "workspace_1"  # Robot's Workspace Name
robot_ip_address = "x.x.x.x"

# The pose from where the image processing happens
observation_pose = PoseObject(
    x=0.16, y=0.0, z=0.35,
    roll=0.0, pitch=1.57, yaw=0.0,
)
# Place pose
place_pose = PoseObject(
    x=0.0, y=-0.2, z=0.12,
    roll=0.0, pitch=1.57, yaw=-1.57
)

# - Initialization

# Connect to robot
robot = NiryoRobot(robot_ip_address)
# Calibrate robot if robot needs calibration
robot.calibrate_auto()
# Updating tool
robot.update_tool()

# Initializing variables
offset_size = 0.05
max_catch_count = 4
shape_expected = ObjectShape.CIRCLE
color_expected = ObjectColor.RED

conveyor_id = robot.set_conveyor()

catch_count = 0
while catch_count < max_catch_count:
    # Turning conveyor on
    robot.run_conveyor(conveyor_id)
    # Moving to observation pose
    robot.move_pose(observation_pose)
    # Check if object is in the workspace
    obj_found, pos_array, shape, color = robot.detect_object(workspace_name,
                                                             shape=shape_expected,
                                                             color=color_expected)
    if not obj_found:
        robot.wait(0.5)  # Wait to let the conveyor turn a bit
        continue
    # Stopping conveyor
    robot.stop_conveyor(conveyor_id)
    # Making a vision pick
    obj_found, shape, color = robot.vision_pick(workspace_name,
                                                shape=shape_expected,
                                                color=color_expected)
    if not obj_found:  # If visual pick did not work
        continue

    # Calculate place pose and going to place the object
    next_place_pose = place_pose.copy_with_offsets(x_offset=catch_count * offset_size)
    robot.place_from_pose(next_place_pose)

    catch_count += 1

# Stopping conveyor
robot.stop_conveyor(conveyor_id)

# Unset conveyor
robot.unset_conveyor(conveyor_id)

robot.go_to_sleep()

robot.close_connection()
