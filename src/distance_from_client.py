#! /usr/bin/env python

import rospy
from monitoring_package.srv import pose
from monitoring_package.msg import poseVelocity
from monitoring_package.srv import distanceAndAverageVelocity, distanceAndAverageVelocityResponse

current_pose_subscriber = None
v_avg_x = None
v_avg_y = None
dist = None

def getGoal(x_current, y_current, v_current_x, v_current_y):
    """
         Calculates and returns the following:
             1. the distance between pose_current and pose_target. 
             2. average velocity of the robot 
    """

    global v_avg_x, v_avg_y
    rospy.wait_for_service('/get_last_target')
    
    getGoalHandle = rospy.ServiceProxy('/get_last_target', pose)
    goal = getGoalHandle()
    distance = ((goal.x-x_current)**2 + (goal.y-y_current)**2)**0.5
    if(v_avg_x==None):
        v_avg_x = abs(v_current_x)
    else:
        v_avg_x = (v_avg_x+abs(v_current_x))/2
    if(v_avg_y==None):
        v_avg_y = abs(v_current_y)
    else:
        v_avg_y = (v_avg_y+abs(v_current_y))/2

    return distance, v_avg_x, v_avg_y

def currentPoseHandler(data):
    """
        Handler to the subscriber current_pose_velocity_publisher. It receives current pose and velocity of robot and uses GetGoal function to update distance, v_average global variables
    """
    global v_avg_x, v_avg_y, dist
    x_current = data.x
    y_current = data.y
    vel_x = data.vel_x
    vel_y = data.vel_y
    dist, v_avg_x, v_avg_y = getGoal(x_current, y_current, vel_x, vel_y)

def getDistanceAndAvgVelocity(request):
    """
        triggers when a call to the service is made. returns global variables which store average velocity and distance to target.
    """
    global v_avg_x, v_avg_y, dist
    return distanceAndAverageVelocityResponse(dist, v_avg_x, v_avg_y)

def main():
    global current_pose_subscriber
    rospy.init_node('get_distance_and_avg_velocity_service', log_level=rospy.DEBUG)
    s = rospy.Service('get_distance_and_avg_velocity', distanceAndAverageVelocity, getDistanceAndAvgVelocity)
    current_pose_subscriber = rospy.Subscriber('current_pose_velocity_publisher', poseVelocity, currentPoseHandler)
    rospy.spin()

if __name__ == "__main__":
    main()

