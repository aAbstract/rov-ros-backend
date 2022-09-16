# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.settings as settings_util
# autopep8: on


settings_obj = settings_util.get_settings()
main_tcu_ip = settings_obj['networking']['main_tcu']
main_tcu_ssh_username = settings_obj['security']['main_tcu']['username']
main_tcu_ssh_pass = settings_obj['security']['main_tcu']['password']

cmd = f'sshpass -p "{main_tcu_ssh_pass}" ssh -t {main_tcu_ssh_username}@{main_tcu_ip} "docker exec -it rov_ros_1 /bin/bash"'
os.system(cmd)
