import os
import subprocess
from time import sleep

from dotenv import load_dotenv


def _change_interface_state(ifname, state):
    print(f"Changing state of {ifname} to {state}... ", end="")
    # os.system(f"ifconfig {ifname} {state}")
    result = subprocess.run(
        ["ip", "link", "set", ifname, state],
        capture_output=True,
        text=True,
    )

    sleep(5)
    result.check_returncode()
    print("Success!")


def _kill_existing_dhcpcd():
    print("Terminating existing instances of dhcpcd... ", end="")
    grep_result = subprocess.Popen(
        ["pgrep", "dhcpcd"],
        stdout=subprocess.PIPE,
    )

    result = subprocess.run(
        ["xargs", "kill"],
        stdin=grep_result.stdout,
        capture_output=True,
        text=True,
    )

    sleep(5)
    result.check_returncode()
    print("Success!")


def _refresh_dhcp(ifname):
    print(f"Requesting new IP for {ifname}... ", end="")
    result = subprocess.run(
        ["dhcpcd", "-n", "enp3s0", "-m", "100", "-t", "180"],
        capture_output=True,
        text=True,
    )

    sleep(5)
    result.check_returncode()
    print("Success!")


def _reload_netplan():
    print("Reloading route tables... ", end="")
    result = subprocess.run(
        ["netplan", "apply"],
        capture_output=True,
        text=True,
    )

    sleep(5)
    result.check_returncode()
    print("Success!")


def teardown_interface():
    load_dotenv()
    _change_interface_state(os.environ.get("IFNAME"), "down")


def bring_up_interface():
    load_dotenv()
    ifname = os.environ.get("IFNAME")
    _change_interface_state(ifname, "up")
    _kill_existing_dhcpcd()
    _refresh_dhcp(ifname)
    _reload_netplan()


test = 1
