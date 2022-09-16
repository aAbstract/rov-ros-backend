import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_util
import lib.settings as settings_util


# module config
_NODE_NAME = 'example_output_raspi_node'

# module state
_temp_pub: rospy.Publisher = None
_settings_obj: dict = None


def ros_node_setup():
    global _temp_pub
    global _settings_obj

    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = settings_util.get_settings()

    topic_id = ros_util.create_topic_id('example_raspi_topic')
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _temp_pub = rospy.Publisher(
        topic_id, ros_std_msgs.String, queue_size=q_size)


def ros_node_loop():
    _temp_pub.publish('example raspi output')
