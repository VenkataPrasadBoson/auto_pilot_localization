#!/usr/bin/env python3
import rospy
from autopilot_utils.pose_helper import get_yaw
from nav_msgs.msg import Odometry
from zed_interfaces.srv import set_pose

set_pose_done = False
def callback(data):
    global set_pose_done
    print("cb called")
    
    yaw = get_yaw(data.pose.pose.orientation)
    if not set_pose_done:
        rospy.wait_for_service('/zed2i/zed_node/set_pose')
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y
        z = data.pose.pose.position.z
        try:
            set_pose1 = rospy.ServiceProxy('/zed2i/zed_node/set_pose', set_pose)
            resp1 = set_pose1(x, y, z, 0 , 0 , yaw)
            set_pose_done = True
            return resp1
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
        # set_pose_done
    else:
        print("Set pose done")


if __name__ == "__main__":
    print("dhbf")
    rospy.init_node("service_client_zed_init_pose")
    rospy.Subscriber("/mavros/global_position/local", Odometry, callback)
    rospy.spin()



