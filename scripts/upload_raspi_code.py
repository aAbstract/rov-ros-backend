# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.log as log_util
import lib.settings as settings_util
# autopep8: on


MODULE_ID = 'upload_raspi_code'

settings_obj = settings_util.get_settings()
raspi_ip = settings_obj['networking']['raspi']


# check if raspi is online
log_util.print_log(MODULE_ID, 'DEBUG',
                   f"checking raspi machine with ip: {raspi_ip}")
proc_exit_code = os.system(f"ping -4 -c 1 {raspi_ip}")

if proc_exit_code != 0:
    log_util.print_log(MODULE_ID, 'ERROR', f"raspi / ip:{raspi_ip} is offline")
    sys.exit()

log_util.print_log(MODULE_ID, 'DEBUG', f"raspi / ip:{raspi_ip} is online")

# upload ros codebase
log_util.print_log(MODULE_ID, 'DEBUG', "uploading ROS codebase")

raspi_ssh_username = settings_obj['security']['raspi']['username']
raspi_ssh_pass = settings_obj['security']['raspi']['password']

os.system(
    f'sshpass -p "{raspi_ssh_pass}" ssh {raspi_ssh_username}@{raspi_ip} "rm -r ~/rov/ros"')
os.system(
    f'sshpass -p "{raspi_ssh_pass}" rsync -a --progress ../ros {raspi_ssh_username}@{raspi_ip}:~/rov/')

log_util.print_log(MODULE_ID, 'DEBUG', "done uploading ROS codebase")
