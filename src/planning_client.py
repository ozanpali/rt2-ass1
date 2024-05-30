#! /usr/bin/env python

import rospy

# Brings in the SimpleActionClient
import actionlib
import assignment_2_2023.msg
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from monitoring_package.msg import poseVelocity

poseVelocityPublisher = None
poseVelocitySubscriber = None
def planning_client():
    """
	This function is responsible to send goal pose to the action server. 
    """
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)
    print("planning_client waiting for server")
    client.wait_for_server()
    rospy.loginfo("server ready. publishing goal")
    pose = PoseStamped()
    pose.pose.position.x = 7
    pose.pose.position.y = 7

    goal = assignment_2_2023.msg.PlanningGoal(target_pose=pose)

    client.send_goal(goal)

def publishPoseAndVelocity(msg):
    """
        Handler for the subscriber for /odom. This function receives odom.message and publishes pose and velocity from it on the topic current_pose_velocity_publisher.
    """
    poseVelocityMsg = poseVelocity()
    poseVelocityMsg.x = msg.pose.pose.position.x
    poseVelocityMsg.y = msg.pose.pose.position.y
    poseVelocityMsg.vel_x = msg.twist.twist.linear.x
    poseVelocityMsg.vel_y = msg.twist.twist.linear.y
    poseVelocityPublisher.publish(poseVelocityMsg)

def initialize_publisher_subscriber():
    """
        initializes the publishr and subscriber and stores them in a global variable.
    """
    global poseVelocityPublisher, poseVelocitySubscriber
    poseVelocityPublisher = rospy.Publisher('current_pose_velocity_publisher', poseVelocity)
    poseVelocitySubscriber = rospy.Subscriber('/odom', Odometry, publishPoseAndVelocity)

def main():
# Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
    rospy.init_node('planning_client', log_level=rospy.DEBUG)
    planning_client()
    initialize_publisher_subscriber()
    rospy.spin()

if __name__ == "__main__":

    main()
