#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
import json
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import Pose

# pose = [ {"x":0.45,"y":-1.9,"type":"pass_point"},
#         {"x":0.45,"y":1,"type":"pass_point"},{"x":0.45,"y":1.9,"type":"pass_point"}]

# --------------- GLOBAL VARIABLE ---------------
client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
pose = []
index = 0

waypoint_pose = []
chargepoint_pose = []

selece_mode = ''

trick_run = False
isStop = True
isRun = False

waitStep = {
    "isStoppoint":False,
    "isPasspoint":False,
    "isChargepoint":False
}

# --------------- GLOBAL VARIABLE ---------------



def callback_robot_pose(data):
    global pose , index ,waitStep
    if  isStop == False:
        scaleX = 0.5
        scaleY = 0.5
        recXmin = pose[index]['pose']['position']['x'] - scaleX
        recXmax = pose[index]['pose']['position']['x'] + scaleX
        recYmin = pose[index]['pose']['position']['y'] - scaleY
        recYmax = pose[index]['pose']['position']['y'] + scaleY
        conX = data.position.x > recXmin and data.position.x < recXmax 
        conY = data.position.y > recYmin and data.position.y < recYmax 
        if conX and conY:
            waitStep['isPasspoint'] = True
        else:
            waitStep['isPasspoint'] = False


def callback_test(data):
    global pose ,index ,isStop,client ,waypoint_pose,charge_pose ,waitStep
    mes =  data.data
    json_data = json.loads(mes)
    rospy.loginfo(json_data)
    
    if json_data['mode'] == "set":
        waypoint_pose = json_data['waypoint']
        charge_pose = json_data['chargepoint']
        pose = waypoint_pose
        index = 0
        rospy.loginfo(pose)
    elif json_data['mode'] == "run":
        manage_move()
    elif json_data['mode'] == "pause":
        client.cancel_goal()
        isStop = True
    elif json_data['mode'] == "sw":
        waitStep['isStoppoint'] = True
        #wait for sw



def manage_move():
    global pose ,index,isStop,isStop ,selece_mode,waitStep
    isStop = False
    waitStep = {
        "isStoppoint":False,
        "isPasspoint":False,
        "isChargepoint":False
    }
    if ( index >= len(pose) ):
        rospy.loginfo("DONE ALL POSE")
        isStop = True
    else:
        if pose[index]['type'] == "stop_point":
            move_waypoint(pose,index)
            selece_mode ="stop_point"
        elif pose[index]['type'] == "pass_point":
            move_passpoint(pose,index)
            selece_mode ="pass_point"
        elif pose[index]['type'] == "charge_point":
            move_passpoint(pose,index)
            selece_mode ="charge_point"


def move_waypoint(pose,index):
    global client
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = pose[index]['pose']['position']['x']
    goal.target_pose.pose.position.y = pose[index]['pose']['position']['y']
    goal.target_pose.pose.orientation.x = pose[index]['pose']['orientation']['x']
    goal.target_pose.pose.orientation.y = pose[index]['pose']['orientation']['y']
    goal.target_pose.pose.orientation.z = pose[index]['pose']['orientation']['z']
    goal.target_pose.pose.orientation.w = pose[index]['pose']['orientation']['w']
    client.send_goal(goal)
def move_passpoint(pose,index):
    global client
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = pose[index]['pose']['position']['x']
    goal.target_pose.pose.position.y = pose[index]['pose']['position']['y']
    goal.target_pose.pose.orientation.w = 1.0
    client.send_goal(goal)


def talker():
    global index,isStop ,selece_mode,client,trick_run,waitStep
    
    pub = rospy.Publisher('/roboAC/nav_node/public', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        if trick_run == True:
            manage_move()
            trick_run=False
        if selece_mode == "stop_point" :
            if client.get_goal_status_text() == "Goal reached.":
                if isStop == True:selece_mode=''
                if waitStep['isStoppoint'] == True:
                    index+=1
                    selece_mode=''
                    trick_run = True
        elif selece_mode == "pass_point" :
            if isStop == True:selece_mode=''
            if waitStep['isPasspoint'] == True:
                index+=1
                selece_mode=''
                trick_run = True
        elif selece_mode == "charge_point" :
            if isStop == True:selece_mode=''
            if waitStep['isChargepoint'] == True:
                index+=1
                selece_mode=''
                trick_run = True

        rospy.loginfo(client.get_goal_status_text())
        rospy.loginfo("INDEX : "+str(index))
        rate.sleep()
    

if __name__ == '__main__':
    
    
    rospy.init_node('movebase_client_py')
    rospy.Subscriber("/roboAC/nav_node", String, callback_test)
    rospy.Subscriber("/robot_pose", Pose, callback_robot_pose)
    talker()
    
    


