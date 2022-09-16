import os
import rospy
from datetime import datetime

import lib.settings as settings_util
import lib.log as log_util


# module state
_node_name = ''
_settings_obj = {}
_module_id = 'lib.ros'


# utils
def _get_node_machine_name():
    search_result = ''

    for mahine_name in _settings_obj['ros']['nodes']:
        if _node_name in _settings_obj['ros']['nodes'][mahine_name]:
            search_result = mahine_name

    return search_result


def create_topic_id(topic_name: str):
    ''' this function is used to generate topic ids when publishing to the topic '''

    return f"/{_node_name}/{topic_name}"


def compute_topic_id(node_name: str, topic_name: str):
    ''' this function is used to generate topic ids when subscribing to the topic '''

    return f"/{node_name}/{topic_name}"


def ros_log(mod_id: str, level: str, desc: str):
    allowed_logs_levels: list[str] = _settings_obj['system']['allowed_log_levels']

    if level in allowed_logs_levels:
        
        temp_log_obj = log_util.log(
            date=datetime.now(),
            level=level,
            mod_id=mod_id,
            description=desc
        )

        formated_log = log_util.format_log(temp_log_obj)

        # publish ros log
        rospy.loginfo(formated_log)


def init_node(node_name: str) -> bool:
    global _node_name
    global _settings_obj
    global _module_id

    _module_id = f"{node_name}.{_module_id}"
    _node_name = node_name

    func_id = f"{_module_id}.init_node"

    _settings_obj = settings_util.get_settings()

    machine_name = _get_node_machine_name()

    if machine_name == '':
        log_util.print_log(func_id, 'ERROR',
                           f"attempt to initialize a non configured ROS node: {node_name}")
        return False

    log_util.print_log(func_id, 'INFO', f"initializing ROS node: {node_name}")

    # setup ROS master URI
    os.environ['ROS_MASTER_URI'] = f"http://{_settings_obj['networking']['main_tcu']}:11311/"
    os.environ['ROS_IP'] = _settings_obj['networking'][machine_name]

    # init ros node
    try:
        rospy.init_node(node_name, anonymous=True)
        log_util.print_log(
            func_id, 'INFO', f"done initializing ROS node: {node_name}")
        ros_log(func_id, 'INFO', f"done initializing ROS node: {node_name}")
        return True

    except Exception as err:
        err_msg = f"error initializing ROS node: {node_name}: {err}"
        log_util.print_log(func_id, 'ERROR', err_msg)
        return False
