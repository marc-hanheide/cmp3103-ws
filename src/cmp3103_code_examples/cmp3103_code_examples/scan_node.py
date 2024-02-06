#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ScanNode(Node):
    """ a simple "ScanNode" that publishes String messages on a topic.


    """

    def __init__(self):
        """ Initialise the Node. """
        # calling the constructor of the super class with the name of the node
        super().__init__('ScanNode')  

        # creating a ROS2 Subscriber, for type "String" and topic name "/msgs"
        # the forth argument is the length of the queue, i.e., only the last message is queued here
        self.create_subscription(LaserScan, '/scan', self.callback, 1)
        self.publisher = self.create_publisher(String, '/timestamp', 1)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 1)


    def callback(self, msg):
        """ the main callback, triggered when a message is received.

            The `msg` field contains the actual ROS2 message object received.
        """
        
        # simply print the received message on the screen:
        print("I received this message: timestamp is %s" % msg.header.stamp.sec)
        s = String()
        s.data = str(msg.header.stamp.sec)
        self.publisher.publish(s)

        cmd_vel = Twist()
        if msg.header.stamp.sec % 2 == 0:
            cmd_vel.angular.z = 0.5 
        else:
            cmd_vel.angular.z = -0.5 
        #print(cmd_vel)
        self.cmd_pub.publish(cmd_vel)


def main(args=None):
    # always run "init()" first
    rclpy.init()

    # let's catch some exceptions should they happen
    try:
        # create the ScanNode object
        node = ScanNode()

        # tell ROS to run this node until stopped (by [ctrl-c])
        rclpy.spin(node)

        # once stopped, tidy up
        node.destroy_node()
        rclpy.shutdown()

    except KeyboardInterrupt:
        print('Node interrupted')

    finally:
        # always print when the node has terminated
        print("Node terminated")


if __name__ == '__main__':
    main()