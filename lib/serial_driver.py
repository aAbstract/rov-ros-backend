# notes:
# this driver supports linux only
# this driver uses ';' as a stopping character

import re
import serial
import subprocess

import lib.log as log_man

# module config
_MODULE_ID = 'lib.serial_driver'
_BAUD_RATE = 9600

# module state
_serial_port = None


def _init_module():
    func_id = f"{_MODULE_ID}._init_module"

    global _serial_port

    log_man.publish_log(func_id, 'DEBUG', 'initializing serial driver')

    # exec system call to list all available serial ports
    sub_process = subprocess.Popen(
        'ls /dev/ttyUSB* /dev/ttyACM*', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, _ = sub_process.communicate()
    output = stdout.decode()
    port_list = re.findall('(/dev/ttyACM[0-9]+|/dev/ttyUSB[0-9]+)', output)

    if len(port_list) != 0:

        # choose serial port
        port_name = port_list[0]

        log_man.publish_log(func_id, 'DEBUG',
                        f"connecting to serial port {port_name}")

        _serial_port = serial.Serial(port_name, _BAUD_RATE)

        log_man.publish_log(func_id, 'INFO',
                        f"connected to serial port {port_name}")

        log_man.publish_log(func_id, 'DEBUG',
                        'finished initializing serial driver')

    else:
        err_msg = 'no serial port detected'
        log_man.publish_log(func_id, 'ERROR', err_msg)


def write_raw(msg: str):
    if _serial_port == None:
        return

    msg_to_write = f"{msg};"
    msg_buffer = msg_to_write.encode()

    if _serial_port != None:
        _serial_port.write(msg_buffer)


def read_raw():    
    out = ''

    if _serial_port == None:
        return out

    if not _serial_port.inWaiting():
        return out

    while True:
        if (_serial_port.inWaiting()):
            char = _serial_port.read(1)

            if char == b';':
                break

            if char != b'\n' and char != b'\r':
                out += char.decode()

    return out


_init_module()
