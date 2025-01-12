import os
import subprocess
from time import sleep

from dotenv import load_dotenv


def _change_interface_state(ifname, state):
    run_subprocess(
        f"Changing state of {ifname} to {state}... ",
        ["ip", "link", "set", ifname, state],
    )


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
    run_subprocess(
        f"Requesting new IP for {ifname}... ",
        ["dhcpcd", "-n", ifname, "-m", "100", "-t", "180"],
    )


def _reload_netplan():
    run_subprocess("Reloading route tables... ", ["netplan", "apply"])


def run_subprocess(header, args, wait=5):
    print(header, end="")
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
    )

    sleep(wait)
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
