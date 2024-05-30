#! /usr/bin/env python

import rospy
from monitoring_package.srv import pose, poseResponse
lastTarget = None

def getLastTarget(request):
    """
        Fetches target pose from the parameter server and returns when service is called.
    """
    global lastTarget
    xGoal = rospy.get_param('des_pos_x')
    yGoal = rospy.get_param('des_pos_y')
    return poseResponse(xGoal, yGoal)



def main():
    rospy.init_node('get_last_target_service', log_level=rospy.DEBUG)
    s = rospy.Service('get_last_target', pose, getLastTarget)
    rospy.spin()

if __name__ == "__main__":
    main()

