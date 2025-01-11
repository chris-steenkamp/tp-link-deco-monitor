from reboot import perform_reboot
from test_internet import run_checks

if not run_checks():
    perform_reboot()