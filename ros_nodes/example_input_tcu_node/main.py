import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_util
import lib.settings as settings_util


# module config
_MODULE_ID = 'ros_nodes.example_input_tcu_node.main'
_NODE_NAME = 'example_input_tcu_node'

# module state
_settings_obj: dict = None


# ros msgs handlers
def _example_ros_msg_handler(msg: ros_std_msgs.String):
    func_id = f"{_MODULE_ID}._example_ros_msg_handler"
    print(f"example_raspi_topic: {msg.data}")
    ros_util.ros_log(func_id, 'DEBUG', f"example_raspi_topic: {msg.data}")


def ros_node_setup():
    global _settings_obj

    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = settings_util.get_settings()

    topic_id = ros_util.compute_topic_id(
        'example_output_raspi_node', 'example_raspi_topic')

    rospy.Subscriber(topic_id, ros_std_msgs.String, _example_ros_msg_handler)


def ros_node_loop():
    pass
