import rospy
import json
import urllib2
from std_srvs.srv import Empty
from robonomics_liability.msg import Liability

class PrintAgent:
    def __init__(self):
        rospy.init_node('printagent_node')

        rospy.Subscriber('/path_to_gcode', String, self.print)

    def print(data):
        req = urllib2.Request('http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]/api/files/local/' + data.data)
        req.add_header('Content-Type', 'application/json')
        req.add_header('X-API-KEY', '80434B5D99384AFC836C90C236AC2652')

        data = {
            "command": "select",
            "print": True
        }

        response = urllib2.urlopen(req, json.dumps(data))

        rospy.wait_for_service("liability/finish")
        fin = rospy.ServiceProxy("liability/finish", Empty)
        rospy.loginfo("finishing...")
        fin()

    def spin(self):
        rospy.spin();
