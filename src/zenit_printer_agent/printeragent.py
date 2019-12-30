# Standart, System and Third Party

# ROS
import rospy

# Robonomics
from robonomics_liability.msg import Liability
from robonomics_liability.srv import StartLiability, StartLiabilityRequest
from robonomics_liability.srv import FinishLiability, FinishLiabilityRequest


class PrinterAgent:
    def __init__(self):
        rospy.init_node('printagent_node')
        rospy.loginfo("Launching PrinterAgent node...")

        rospy.Subscriber('/liability/ready', Liability, self.on_new_liability)

        rospy.wait_for_service('liability/finish')
        self.liability_proxy = namedtuple('liability_srvs_proxy', ['start', 'finish'])(
                                          rospy.ServiceProxy('liability/start', StartLiability),
                                          rospy.ServiceProxy('liability/finish', FinishLiability))

        rospy.loginfo("PrinterAgent node is launched!")

    def on_new_liability(self, liability: Liability):
        pass

    def spin(self):
        rospy.spin();
