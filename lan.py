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
    print("Success!", flush=True)


def _remove_default_route(ifname):
    run_subprocess(
        f"Removing default route from {ifname}... ",
        ["ip", "route", "del", "default", "via", "192.168.0.1", "dev", ifname],
    )
    run_subprocess(
        f"Removing route additional route from {ifname}... ",
        ["ip", "route", "del", "192.168.0.1", "dev", ifname],
    )


def _add_default_route(ifname): ...


def teardown_interface():
    load_dotenv()
    _remove_default_route(os.environ.get("IFNAME"))


def bring_up_interface():
    load_dotenv()
    _add_default_route(ifname=os.environ.get("IFNAME"))
    _reload_netplan()
