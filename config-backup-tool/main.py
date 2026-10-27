import os
from dotenv import load_dotenv
from nornir import InitNornir
import yaml
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import random

load_dotenv()  # reads .env into environment variables

nr = InitNornir(config_file="config.yaml")

ios = nr.inventory.groups["cisco_ios"]
ios.username = os.environ["LAB_USER"]
ios.password = os.environ["LAB_SECRET"]

def get_device_info(task):
    r = task.run(
        task=netmiko_send_command,
        command_string="show run"
    )
    with open(f"{task.host.name}.cfg", "w") as f:
        f.write(r.result)



result = nr.run(task=get_device_info)


for host, multi in result.items():
    print(host, "FAILED" if multi.failed else "saved")
