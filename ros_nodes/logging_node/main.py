import rospy
import rosgraph_msgs.msg as ros_graph_msgs
import sys

import lib.ros as ros_util


# module config
_NODE_NAME = 'logging_node'


# ros msgs handlers
def _log_read_handler(log: ros_graph_msgs.Log):
    print(f"ROSOUT: {log.msg}")


def ros_node_setup():
    is_init = ros_util.init_node(_NODE_NAME)
    
    if not is_init:
        sys.exit()

    rospy.Subscriber('/rosout', ros_graph_msgs.Log, _log_read_handler)


def ros_node_loop():
    pass
