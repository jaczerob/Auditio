import subprocess
import sys
import time

import psutil


def process_is_running(name: str) -> bool:
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
            if name.lower() in pinfo['name'].lower():
                return True
        except:
            pass
    return False


def restart_process():
    args = [sys.executable] + sys.argv
    subprocess.Popen(args)
    time.sleep(5)
    sys.exit('Restarting process')


def wait_for_process(name: str) -> None:
    while not process_is_running(name):
        time.sleep(5)