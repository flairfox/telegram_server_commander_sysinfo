import json
import logging
import os
import platform
import re
import socket
import uuid

import psutil
from flask import Flask

app = Flask(__name__)


def retrieve_system_info():
    try:
        info = {
            'platform': platform.system(),
            'platform-release': platform.release(),
            'platform-version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'ip-address': socket.gethostbyname(socket.gethostname()),
            'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'processor': platform.processor(),
            'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def retrieve_resource_utilization_info():
    try:
        info = {}

        cpu_utilization = {}
        if hasattr(psutil, 'sensors_temperatures'):
            cpu_utilization['cpu-temperature'] = psutil.sensors_temperatures()['coretemp'][0].current

        cpu_utilization['cpu-load-percent'] = psutil.cpu_percent()
        cpu_utilization['cpu-load-percent-per-core'] = psutil.cpu_percent(interval=None, percpu=True)
        info['cpu-utilization'] = cpu_utilization

        virtual_memory = psutil.virtual_memory()
        memory_utilization = {
            'total': virtual_memory.total,
            'used': virtual_memory.used,
            'free': virtual_memory.free,
            'percent': virtual_memory.percent}
        info['memory-utilization'] = memory_utilization

        swap_memory = psutil.swap_memory()
        swap_utilization = {
            'total': swap_memory.total,
            'used': swap_memory.used,
            'free': swap_memory.free,
            'percent': swap_memory.percent}
        info['swap-utilization'] = swap_utilization

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def retrieve_drives_info():
    try:
        info = []
        disk_partitions = psutil.disk_partitions()
        for disk_partition in disk_partitions:
            if not disk_partition.mountpoint.startswith('/snap'):
                disk_usage = psutil.disk_usage(disk_partition.mountpoint)

                drive_info = {
                    'mount-point': disk_partition.mountpoint,
                    'total': disk_usage.total,
                    'used': disk_usage.used,
                    'free': disk_usage.free,
                    'percent': disk_usage.percent}

                info.append(drive_info)

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


@app.route('/sysinfo', methods=['GET'])
def get_system_info():
    return retrieve_system_info()


@app.route('/utilization', methods=['GET'])
def get_resource_utilization_info():
    return retrieve_resource_utilization_info()


@app.route('/drives', methods=['GET'])
def get_drives_info():
    return retrieve_drives_info()


@app.route('/reboot', methods=['GET'])
def reboot():
    os.system("shutdown /r")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    os.system("shutdown /s")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
