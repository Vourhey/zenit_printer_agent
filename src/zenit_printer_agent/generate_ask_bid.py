import rospy
from robonomics_lighthouse.msg import Ask, Bid
from zenit_printer_agent.srv import *
from web3 import Web3, HTTPProvider

class Generate_ask_bid:
    
    model     = 'QmWboFP8XeBtFMbNYK3Ne8Z3gKFBSR5iQzkKgeNgQz3dZP'
    token     = '0xdEA33F21294399c675C8F1D6C4a1F39b0719BCBf' 
    #objective = 'QmaFhGQjwHkhkxwyGsLfGkyF2hjB3xQxN1AWNFrH71ADqB'
    cost      = 1

    def __init__(self):
        rospy.init_node('generate_ask_bid_node')

        self.web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
        self.signing_bid = rospy.Publisher('lighthouse/infochan/signing/bid', Bid, queue_size=128)
        self.signing_ask = rospy.Publisher('lighthouse/infochan/signing/ask', Ask, queue_size=128)

        def make_bid(m):
            rospy.loginfo("Got an ask, let's make a bid")

            block = self.web3.eth.getBlock('latest')
            deadline = block.number + 10000 # should be enough for a day

            msg             = Bid()
            msg.model       = self.model
            msg.objective   = m.objective
            msg.token       = self.token
            msg.cost        = m.cost
            msg.lighthouseFee = 0
            msg.deadline    = deadline
            self.signing_bid.publish(msg)
        rospy.Subscriber('lighthouse/infochan/incoming/ask', Ask, make_bid)

        def make_ask(req):
            rospy.loginfo("Creating an ask")
            rospy.loginfo()

            block = self.web3.eth.getBlock('latest')
            deadline = block.number + 10000 # should be enough for a day

            msg             = Ask()
            msg.model       = self.model
            msg.objective   = req.objective
            msg.token       = self.token
            msg.cost        = self.cost
            msg.validator   = '0x0000000000000000000000000000000000000000'
            msg.validatorFee = 0
            msg.deadline    = deadline

            self.signing_ask.publish(msg)
            return ObjectiveResponse('ok')
        rospy.Service('make_ask', Objective, make_ask)

    def spin(self):
        rospy.spin()
