import json
import logging
import os
import platform
import psutil
import re
import socket
import uuid

from flask import Flask

app = Flask(__name__)


def getSystemInfo():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def getResourceUtilizationInfo():
    try:
        info = {}

        cpu_utilization = {}
        if hasattr(psutil, 'sensors_temperatures'):
            cpu_utilization['cpu-temperature'] = psutil.sensors_temperatures()['coretemp'][0].current

        cpu_utilization['cpu-load-percent'] = psutil.cpu_percent()
        cpu_utilization['cpu-load-percent-per-core'] = psutil.cpu_percent(interval=None, percpu=True)
        info['cpu-utilization'] = cpu_utilization

        virtual_memory = psutil.virtual_memory()
        memory_utilization = {}
        memory_utilization['total'] = virtual_memory.total
        memory_utilization['used'] = virtual_memory.used
        memory_utilization['free'] = virtual_memory.free
        memory_utilization['percent'] = virtual_memory.percent
        info['memory-utilization'] = memory_utilization

        swap_memory = psutil.swap_memory()
        swap_utilization = {}
        swap_utilization['total'] = swap_memory.total
        swap_utilization['used'] = swap_memory.used
        swap_utilization['free'] = swap_memory.free
        swap_utilization['percent'] = swap_memory.percent
        info['swap-utilization'] = swap_utilization

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def getDrivesInfo():
    try:
        info = []
        disk_partitions = psutil.disk_partitions()
        for disk_partition in disk_partitions:
            if not disk_partition.mountpoint.startswith('/snap'):
                disk_usage = psutil.disk_usage(disk_partition.mountpoint)

                drive_info = {}
                drive_info['mount-point'] = disk_partition.mountpoint
                drive_info['total'] = disk_usage.total
                drive_info['used'] = disk_usage.used
                drive_info['free'] = disk_usage.free
                drive_info['percent'] = disk_usage.percent

                info.append(drive_info)

        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


@app.route('/sysinfo', methods=['GET'])
def get_system_info():
    return getSystemInfo()


@app.route('/utilization', methods=['GET'])
def get_resource_utilization_info():
    return getResourceUtilizationInfo()


@app.route('/drives', methods=['GET'])
def get_drives_info():
    return getDrivesInfo()


@app.route('/reboot', methods=['GET'])
def reboot():
    os.system("shutdown /r")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    os.system("shutdown /s")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)
