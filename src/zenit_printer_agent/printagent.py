import rospy
import json
import urllib3
from std_srvs.srv import Empty
from std_msgs.msg import String
from robonomics_liability.msg import Liability
from . import apikey

class PrintAgent:
    def __init__(self):
        rospy.init_node('printagent_node')

        self.output = open(rospy.get_param('~logfile'), 'w')

        rospy.Subscriber('/path_to_gcode', String, self.print_gcode)

    def print_gcode(self, data):
        rospy.loginfo('Got a task to print {}'.format(data.data))

        url = 'http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]/api/files/local/' + data.data
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': apikey.apikey()
        }
        data = {
            "command": "select",
            "print": True
        }
        encoded_data = json.dumps(data).encode('utf-8')

        pm = urllib3.PoolManager()
        r = pm.request('POST', url, body=encoded_data, headers=headers)

        if r.status != 204:
            rospy.loginfo("Printer is in bad state")

        url = 'http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]/api/job'
        headers = {
            'X-API-KEY': apikey.apikey()
        }

        while True:
            r = pm.request('GET', url, headers=headers)
            d = json.loads(r.data.decode('utf-8'))['progress']['completion']
            if d == 100.0:
                break
            rospy.loginfo('Completed {}%'.format(d ))
            self.output.write('Completed: {}%'.format(d))
            self.output.flush()
            rospy.sleep(1)
        
        '''
        pm = urllib3.PoolManager()
        req = pm.request('GET', 'http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]/api/files/local/ok?recursive=true', headers={'X-API-KEY': apikey.apikey()})
        
        rospy.loginfo(req.data)
        '''
        
        rospy.wait_for_service("liability/finish")
        fin = rospy.ServiceProxy("liability/finish", Empty)
        rospy.loginfo("finishing...")
        fin()

    def spin(self):
        rospy.spin();
