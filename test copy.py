#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
import json
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import Pose

client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
pose = [ {"x":0.45,"y":-1.9,"type":"pass_point"},
        {"x":0.45,"y":1,"type":"pass_point"},{"x":0.45,"y":1.9,"type":"pass_point"}]


waypoint_pose = []
chargepoint_pose = []

isStop = True
isStoppoint = False 
isPasspoint = False
isChargepoint = False
index = 0


def callback_robot_pose(data):
    global pose , index ,isPasspoint
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
            # rospy.loginfo("TRUE   NA"+str(index))
            isPasspoint = True
        else:
            # rospy.loginfo("FALSE   NA"+str(index))
            isPasspoint = False

    # rospy.loginfo("Robot position (x, y, z): %f, %f, %f", data.position.x, data.position.y, data.position.z)

def callback_test(data):
    global pose ,index ,isStoppoint,isPasspoint,isStop,client

    mes =  data.data
    json_data = json.loads(mes)
    rospy.loginfo('-'*30)
    rospy.loginfo(json_data)
    

    if json_data['mode'] == "set":
        waypoint_pose = json_data['waypoint']
        charge_pose = json_data['chargepoint']

        pose = waypoint_pose
        index = 0
        rospy.loginfo("SET data")
        rospy.loginfo(waypoint_pose)
        rospy.loginfo(pose)

    elif json_data['mode'] == "run":
        manage_move()
    elif json_data['mode'] == "pause":
        client.cancel_goal()
        isStop = True
    elif json_data['mode'] == "sw":
        isStoppoint = True


def manage_move():
    global pose , index,isStop,isStoppoint,isPasspoint,isStop
    isStop = False
    isPasspoint = False
    isStoppoint = False
    if ( index >= len(pose) ):
        rospy.loginfo("DONE ALL POSE")
        isStop = True
    else:
        if pose[index]['type'] == "stop_point":
            isDone = False
            result = move_waypoint(pose,index)
            if result:
                # for i in range(10):rospy.loginfo("DONE"+str(index))
                while True:
                    rospy.loginfo("SAY HI")
                    if isStop == True:break
                    if isStoppoint == True:
                        isDone = True
                        break
            if isDone:
                index+=1
                manage_move()
        elif pose[index]['type'] == "pass_point":
            move_passpoint(pose,index)
            isDone = False
            while True:
                    if isStop == True:break
                    if isPasspoint == True:
                        isDone = True
                        break
            if isDone:
                index+=1
                manage_move()


def move_waypoint(pose,index):
    global client
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = pose[index]['pose']['position']['x']
    goal.target_pose.pose.position.y = pose[index]['pose']['position']['y']
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
    
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
    global data,index
    pub = rospy.Publisher('/roboAC/nav_node/public', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo("INDEX : "+str(index))
        rate.sleep()
    

if __name__ == '__main__':
    
    
    rospy.init_node('movebase_client_py')
    rospy.Subscriber("/roboAC/nav_node", String, callback_test)
    rospy.Subscriber("/robot_pose", Pose, callback_robot_pose)
    talker()
    
    


