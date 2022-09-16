# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.log as log_util
import lib.settings as settings_util
# autopep8: on


MODULE_ID = 'ros_down'

settings_obj = settings_util.get_settings()

# validate network configs
network_config: dict[str, str] = settings_obj['networking']

log_util.print_log(MODULE_ID, 'INFO', 'checking network configs')

for machine_name, machine_ip in network_config.items():
    if machine_ip in ['', '127.0.0.1']:
        continue

    log_util.print_log(MODULE_ID, 'DEBUG',
                       f"checking host {machine_name} with IP {machine_ip}")

    proc_exit_code = os.system(f"ping -4 -c 1 {machine_ip}")

    if proc_exit_code != 0:
        log_util.print_log(
            MODULE_ID, 'ERROR', f"host {machine_name} with IP {machine_ip} is offline")
        sys.exit()

log_util.print_log(MODULE_ID, 'INFO',
                   'finished scanning machines, all machines are online')

# stop slave ros nodes
log_util.print_log(MODULE_ID, 'INFO', 'stopping slave ROS nodes')

ros_nodes_map: dict = settings_obj['ros']['nodes']
nodes_to_check: list[str] = []

for machine_name in ros_nodes_map.keys():
    # skip monitor TCU machine because it should start manually
    if machine_name == 'monitor_tcu':
        continue

    machine_ip = settings_obj['networking'][machine_name]
    machine_ssh_username = settings_obj['security'][machine_name]['username']
    machine_ssh_password = settings_obj['security'][machine_name]['password']

    for node_name in ros_nodes_map[machine_name]:
        nodes_to_check.append(node_name)

        down_cmd = f'sshpass -p "{machine_ssh_password}" ssh {machine_ssh_username}@{machine_ip} "pkill -9 -f ./ros_nodes/.*/bootstrap.py"'
        os.system(down_cmd)

log_util.print_log(MODULE_ID, 'INFO', 'slave ROS nodes stopped')

log_util.print_log(MODULE_ID, 'INFO', 'shutting down ROS master')
os.system('docker-compose down')
log_util.print_log(MODULE_ID, 'INFO', 'finished shutting down ROS master')
