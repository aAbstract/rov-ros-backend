import os
import sys
import subprocess
import time
import re

import lib.log as log_util
import lib.settings as settings_util


MODULE_ID = 'ros_launch'

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

# start ros master node
log_util.print_log(MODULE_ID, 'INFO', 'starting ROS master node')
os.system('docker-compose up -d')
# wait until ros master boots up
time.sleep(2)
log_util.print_log(MODULE_ID, 'INFO', 'finished starting ROS master node')

# start slave ros nodes
log_util.print_log(MODULE_ID, 'INFO', 'starting slave ROS nodes')

ros_nodes_map: dict = settings_obj['ros']['nodes']
nodes_to_check: list[str] = ['/rosout']

for machine_name in ros_nodes_map.keys():
    # skip monitor TCU machine because it should start manually
    if machine_name == 'monitor_tcu':
        continue

    machine_ip = settings_obj['networking'][machine_name]
    machine_ssh_username = settings_obj['security'][machine_name]['username']
    machine_ssh_password = settings_obj['security'][machine_name]['password']

    for node_name in ros_nodes_map[machine_name]:
        log_util.print_log(
            MODULE_ID, 'INFO', f"starting nodes: ({machine_name}|{machine_ip}).{node_name}")

        nodes_to_check.append(f"/{node_name}")

        launch_cmd = f'sshpass -p "{machine_ssh_password}" ssh -f {machine_ssh_username}@{machine_ip} "cd ~/rov/ros && (python3 ./ros_nodes/{node_name}/bootstrap.py > /dev/null 2>&1 &) && exit"'
        os.system(launch_cmd)
        time.sleep(1)

log_util.print_log(MODULE_ID, 'INFO', 'done starting slave ROS nodes')

# ros launch validation
log_util.print_log(MODULE_ID, 'INFO', 'starting ROS validation routine')

main_tcu_ip = settings_obj['networking']['main_tcu']
main_tcu_ssh_username = settings_obj['security']['main_tcu']['username']
main_tcu_ssh_pass = settings_obj['security']['main_tcu']['password']
validation_cmd = f'sshpass -p "{main_tcu_ssh_pass}" ssh {main_tcu_ssh_username}@{main_tcu_ip} "docker exec rov_ros_1 /bin/bash -c \\"source /ros_entrypoint.sh && rosnode list\\""'

sub_process = subprocess.Popen(
    validation_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
stdout, _ = sub_process.communicate()
output = stdout.decode()
active_nodes_list = output.split()

# format active nodes
for i in range(len(active_nodes_list)):
    if active_nodes_list[i] == '/rosout':
        continue

    active_nodes_list[i] = re.findall(
        '\/[a-z_]+', active_nodes_list[i])[0][:-1]

if set(nodes_to_check) == set(active_nodes_list):
    log_util.print_log(MODULE_ID, 'INFO', 'ROS validation routine succeed')

else:
    log_util.print_log(MODULE_ID, 'ERROR', 'ROS validation routine faild')
    print('nodes_to_check:')
    print(nodes_to_check)
    print('active_nodes')
    print(active_nodes_list)
