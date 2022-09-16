# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

import ros_nodes.logging_node.main as logging_node
# autopep8: on


# module config
_NODE_DELAY = 0.01  # 10ms delay / operation frequency 100Hz


if __name__ == '__main__':
    logging_node.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            logging_node.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
