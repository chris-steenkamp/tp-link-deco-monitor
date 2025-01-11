import socket


def check_host_and_port_are_reachable(host: str, port: int) -> bool:
    print(f"Checking connectivity: {host}... ", end="")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)

            sock.connect((host, port))
        print("Success!")
        return True
    except socket.error as e:
        print(f"Failed with error: {e}")
        return False


HOSTS = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "169.1.1.1", "169.1.1.2"]


def run_checks():
    return any((check_host_and_port_are_reachable(host, 53) for host in HOSTS))


if __name__ == "__main__":
    run_checks()
