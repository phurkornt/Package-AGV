#!/usr/bin/env python

from __future__ import print_function

import rospy

from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import *

from std_msgs.msg import String
from geometry_msgs import msg
import json

server = ''

init_pose_global = {'position':{},'orientation':{}}

def processFeedback2(feedback):
    p = feedback.pose
    # server.setPose('1',p)
    # server.applyChanges()
    
def callback_robot_pose(feedback):
    """
        set robot pose real time 
    """
    server.setPose('robot_pose',feedback)
    server.applyChanges()
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", feedback)


def processFeedback(feedback):
    """
        determine value for set init pose
    """
    global init_pose_global

    p = feedback.pose

    init_pose_global["position"]["x"] = p.position.x
    init_pose_global["position"]["y"] = p.position.y

    init_pose_global["orientation"]["x"] = p.orientation.x
    init_pose_global["orientation"]["y"] = p.orientation.y
    init_pose_global["orientation"]["z"] = p.orientation.z
    init_pose_global["orientation"]["w"] = p.orientation.w

    #print(str(p),type(p))

    # print(feedback.marker_name + " is now at " + str(p.x) + ", " + str(p.y) + ", " + str(p.z))



def make_marker(name , colors , type_name , position , orientation , zPose = 0.7 , scal = 0.5):
        """Creates a new interactive marker.
        Args:
            name: The name of the marker.
            pose: The geometry_msgs/Pose of the marker.
        """
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = 'map'
        int_marker.name = name
        int_marker.description = type_name
        
        int_marker.pose.position.x = position['x']
        int_marker.pose.position.y = position['y']
        int_marker.pose.position.z = 0.01

        int_marker.scale = 0.5

        # int_marker.pose = pose

        arrow_marker = Marker()
        arrow_marker.type = Marker.ARROW

        arrow_marker.pose.orientation.w = orientation['w']
        arrow_marker.pose.orientation.x = orientation['x']
        arrow_marker.pose.orientation.y = orientation['y']
        arrow_marker.pose.orientation.z = orientation['z']

        arrow_marker.scale.x = int_marker.scale / 2
        arrow_marker.scale.y = 0.05
        arrow_marker.scale.z = 0.05
        arrow_marker.color.r = colors[0]
        arrow_marker.color.g = colors[1]
        arrow_marker.color.b = colors[2]
        arrow_marker.color.a = 1.0

        text_marker = Marker()
        text_marker.type = Marker.TEXT_VIEW_FACING
        text_marker.pose.orientation.w = 1
        text_marker.pose.position.z = zPose
        text_marker.scale.x = 0.2
        text_marker.scale.y = 0.2
        text_marker.scale.z = 0.2
        text_marker.color.r = colors[0]
        text_marker.color.g = colors[1]
        text_marker.color.b = colors[2]
        text_marker.color.a = 1
        text_marker.text = name

        arrow_control = InteractiveMarkerControl()
        arrow_control.orientation.w = 1
        arrow_control.orientation.y = 1
        arrow_control.interaction_mode = InteractiveMarkerControl.MOVE_PLANE
        arrow_control.markers.append(arrow_marker)
        arrow_control.markers.append(text_marker)
        arrow_control.always_visible = True
        int_marker.controls.append(arrow_control)



        control = InteractiveMarkerControl()
        control.orientation.w = 1
        control.orientation.y = 1
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
      
        int_marker.controls.append(control)

        return int_marker

def init_get_data_type():
    """
        Create data type msg.PoseWithCovarianceStamped
    """
    initpose = msg.PoseWithCovarianceStamped()
    # initpose.header.stamp = rospy.get_rostime()
    initpose.header.frame_id = "map"
    
    initpose.pose.pose.position.x = init_pose_global["position"]["x"]
    initpose.pose.pose.position.y = init_pose_global["position"]["y"]
    initpose.pose.pose.orientation.w = init_pose_global["orientation"]["w"]
    initpose.pose.pose.orientation.x = init_pose_global["orientation"]["x"]
    initpose.pose.pose.orientation.y = init_pose_global["orientation"]["y"]
    initpose.pose.pose.orientation.z = init_pose_global["orientation"]["z"] 
    return initpose
def callback_manage(data):
    mes =  data.data
    rospy.loginfo(mes)
    json_data = json.loads(mes)
    # rospy.loginfo(json_data)

    
    if json_data['mode'] == "insert":
        
        name = json_data['name']
        type_name  = json_data['type']
        colors = [0,0,0]

        if json_data['type'] == "stop_point":
            colors=[0,0.75,0]
        elif json_data['type'] == "pass_point":
            colors=[0.75,0.5,0]
        elif json_data['type'] == "charge":
            colors=[0.75,0,0]
        
        position = {"x":0,"y":0,"z":0.01}
        orientation = {"x":0,"y":0,"z":0,"w":1}

        if 'pose' in json_data:
            pose = json_data['pose']
            position = pose['position']
            orientation = pose['orientation']

        server.insert(make_marker(name , colors , type_name , position , orientation) , processFeedback)
        server.applyChanges()

    elif json_data['mode'] == "delete":
        name = json_data['name']
        server.erase(name)
        server.applyChanges()
    elif json_data['mode'] == "clear":
        server.applyChanges()
    elif json_data['mode'] == "init_pose":

        position = {"x":0,"y":0,"z":0.01}
        orientation = {"x":0,"y":0,"z":0,"w":1}
        colors=[0,0,0]

        server.insert(make_marker( "init_pose" , colors , "init_pose" , position , orientation) , processFeedback)
        server.applyChanges()

    elif json_data['mode'] == "init_pose_confirm":
        pub = rospy.Publisher('/initialpose', msg.PoseWithCovarianceStamped, queue_size=10)
        topic_msg = init_get_data_type()
        rospy.loginfo(topic_msg)
        pub.publish(topic_msg)

    elif json_data['mode'] == "display_robot":
        position = {"x":0,"y":0,"z":0.01}
        orientation = {"x":0,"y":0,"z":0,"w":1}
        colors=[0,0,0]
        server.insert(make_marker( "robot_pose" , colors , "robot_pose" , position , orientation , zPose=1) , processFeedback2)
        server.applyChanges()
    
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    


if __name__=="__main__":
    
    


    rospy.init_node("simple_marker")
    # create an interactive marker server on the topic namespace simple_marker
    server = InteractiveMarkerServer("simple_marker")

   

    rospy.Subscriber("roboAC/marker_node", String, callback_manage)
    rospy.Subscriber("/robot_pose", msg.Pose ,callback_robot_pose)
    # server.insert(make_marker("wow"), processFeedback)
    # server.applyChanges()


    rospy.spin()

