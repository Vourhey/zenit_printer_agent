# Standart, System and Third Party
from tempfile import mkstemp

# ROS
import rospy

# Robonomics
from robonomics_msgs.msg import Offer, Demand
from ethereum_common.msg import Address, UInt256
from ipfs_common.msg import Multihash, Filepath
from ipfs_common.ipfs_rosbag import IpfsRosBag
from ipfs_common.srv import IpfsDownloadFile

from .octopi import OctoPi


class Trader:

    def __init__(self):
        rospy.init_node("trader_node")
        rospy.loginfo("Launching trader node...")

        rospy.wait_for_service("/eth/current_block")
        rospy.wait_for_service("/eth/accounts")
        self.accounts = rospy.ServiceProxy("/eth/accounts", Accounts)()
        rospy.loginfo(str(self.accounts))  # AIRA ethereum addresses

        self.MODEL = rospy.get_param("~model")
        self.TOKEN = rospy.get_param("~token")

        self.signing_offer = rospy.Publisher("/lighthouse/infochan/eth/signing/offer", Offer, queue_size=128)
        rospy.Subscriber('/liability/infochan/incoming/demand', Demand, self.on_incoming_demand)

        self.octopi = OctoPi(rospy.get_param("~octopi_url"),
                             rospy.get_param("~octopi_key"))

        rospy.loginfo("Trader node is launched!")

    def on_incoming_demand(self, demand: Demand):
        rospy.loginfo("Incoming demand: {}".format(demand))
        if demand.model.multihash == self.MODEL:
            price = self.calc_price(demand)
            if demand.cost < price:
                self.send_offer(demand, price)
        else:
            rospy.loginfo("The demand is not for me, skipping")

    def make_deadline(self) -> UInt256:
        lifetime = int(rospy.get_param('~order_lifetime'))
        deadline = rospy.ServiceProxy('/eth/current_block', BlockNumber)().number + lifetime
        return UInt256(str(deadline))

    def send_offer(self, demand: Demand, price: UInt256):
        offer = Offer()
        offer.model = Multihash(self.MODEL)
        offer.objective = demand.objective
        offer.token = Address(self.TOKEN)
        offer.cost = price
        offer.lighthouse = demand.lighthouse
        offer.validator = demand.validator
        offer.lighthouseFee = UInt256("0")
        offer.deadline = self.make_deadline()

        self.signing_offer.publish(offer)
        rospy.loginfo(offer)

    """
    Downloads a file by the given IPFS hash and returns the local path
    """
    def __ipfs_download(self, ipfs_hash: str) -> str:
        rospy.wait_for_service('/ipfs/get_file')
        download = rospy.ServiceProxy('/ipfs/get_file', IpfsDownloadFile)

        tmpfile = mkstemp()

        res = download(Multihash(ipfs_hash), Filepath(tmpfile[1]))
        if not res.success:
            raise Exception(res.error_msg)

        return tmpfile[1]

    """
    Let's assume 1 hour of printer usage costs $5
    And let's say we use a stable coin for now 1 Token = $1
    1 Token has 9 digits after decimal point, so technically 1_000_000_000 tk = $1
    est_time in seconds
    """
    def __calc_production_cost(self, est_time: int) -> int:
        hours = est_time / 60 / 60
        cost_usd = hours * 5
        tokens = int(cost_usd * 1_000_000_000)
        return tokens

    def calc_price(self, demand: Demand) -> UInt256:
        objective = IpfsRosBag(multihash=demand.objective)
        stl_address = objective.messages["/file"].data

        stl_path = self.__ipfs_download(stl_address)
        name = self.octopi.upload_file(stl_path)

        gcode_analysis = self.octopi.get_gcode_analysis(name)
        estimated_time = int(gcode_analysis["estimatedPrintTime"])

        production_cost = self.__calc_production_cost(estimated_time)
        material_cost = 0       # TODO

        total_cost_tokens = production_cost + material_cost
        return UInt256(str(total_cost_tokens))

    def spin(self):
        rospy.spin()

