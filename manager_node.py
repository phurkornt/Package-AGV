#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess
import signal
import json

# data: '{ \"topic\":\"test\" , \"script\":\"roslaunch test.launch\" , \"mode\":\"start\"   }'
# {"topic": "hi", "params": "11"}
# json_object = json.loads(employee_string)
# print(json_object , type(json_object))

pooling = []

class manager:

    def __init__(self, topic , script , mode):
        self.topic = topic
        self.script = script.split()
        self.mode = mode
        self.process = ""

    def set_value(self , mode):
        self.mode = mode

    def get_status():
        return  0
    def control(self):
        if self.mode == "start" or self.mode == "once" :
            self.start()
        elif self.mode == "stop":
            self.stop()
            self.topic = ''

    def start(self):
        self.process = subprocess.Popen(self.script)

    def stop(self):
        self.process.terminate()
        


def callback(data):
    mes =  data.data
    json_data = json.loads(mes)
    # rospy.loginfo(json_data)
    # rospy.loginfo(json_data['script'].split())
    if json_data['mode'] == 'once':
        manage = manager(json_data['topic'] , json_data['script'], json_data['mode'])
        manage.control()
    else:
        n = 0
        for i in range(len(pooling)):
            if json_data['topic'] == pooling[i].topic:
                pooling[i].set_value(json_data['mode'])
                pooling[i].control()
                if json_data['mode'] == 'stop':
                    pooling.remove(pooling[i])
                break
            else:
                n+=1
        if n >= len(pooling):
            manage = manager(json_data['topic'] , json_data['script'], json_data['mode'])
            manage.control()
            pooling.append( manage )


    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    


    
def listener():
    rospy.init_node('manager_node', anonymous=True)
    rospy.Subscriber("roboAC/manager_node", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()



