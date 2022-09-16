# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.log as log_util
import lib.settings as settings_util
# autopep8: on


MODULE_ID = 'upload_main_tcu_code'

settings_obj = settings_util.get_settings()
main_tcu_ip = settings_obj['networking']['main_tcu']


# check if raspi is online
log_util.print_log(MODULE_ID, 'DEBUG',
                   f"checking main TCU machine with ip: {main_tcu_ip}")
proc_exit_code = os.system(f"ping -4 -c 1 {main_tcu_ip}")

if proc_exit_code != 0:
    log_util.print_log(MODULE_ID, 'ERROR', f"main_tcu / ip:{main_tcu_ip} is offline")
    sys.exit()

log_util.print_log(MODULE_ID, 'DEBUG', f"main_tcu / ip:{main_tcu_ip} is online")

# upload ros codebase
log_util.print_log(MODULE_ID, 'DEBUG', "uploading ROS codebase")

main_tcu_ssh_username = settings_obj['security']['main_tcu']['username']
main_tcu_ssh_pass = settings_obj['security']['main_tcu']['password']

os.system(
    f'sshpass -p "{main_tcu_ssh_pass}" ssh {main_tcu_ssh_username}@{main_tcu_ip} "rm -r ~/rov/ros"')
os.system(
    f'sshpass -p "{main_tcu_ssh_pass}" rsync -a --progress ../ros {main_tcu_ssh_username}@{main_tcu_ip}:~/rov/')

log_util.print_log(MODULE_ID, 'DEBUG', "done uploading ROS codebase")
