import fcntl

from reboot import perform_reboot
from test_internet import run_checks
from wifi_connection import switch_to_iot_network, switch_to_primary_network

LOCK_FILE = "/var/lock/check_connectivity.lock"

with open(LOCK_FILE, "w") as lock:
    try:
        fcntl.flock(lock, fcntl.LOCK_NB | fcntl.LOCK_EX)
    except IOError:
        print("Reboot already in progress... Exiting.")
    else:
        if not run_checks():
            switch_to_primary_network()
            perform_reboot()
            switch_to_iot_network()
