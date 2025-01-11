import subprocess
from time import sleep


def _get_network_ssid(network_id) -> str:
    result = (
        subprocess.run(
            ["wpa_cli", "get_network", str(network_id), "ssid"],
            capture_output=True,
            text=True,
        )
        .stdout.strip()
        .split("\n")[1]
    )

    return result


def _switch_network(network_id) -> bool:
    print(f"Switching Wi-Fi network to {_get_network_ssid(network_id)}... ", end="")
    result = (
        subprocess.run(
            ["wpa_cli", "select_network", str(network_id)],
            capture_output=True,
            text=True,
        )
        .stdout.strip()
        .split("\n")[1]
    )
    if success := ("OK" == result):
        print("Success!")
    else:
        print("Failed!")

    sleep(5)

    return success


def switch_to_primary_network():
    _switch_network(0)


def switch_to_iot_network():
    _switch_network(1)
