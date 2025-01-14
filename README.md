# TP-Link Deco Monitor

A Python utility to monitor and automatically reboot TP-Link Deco mesh network devices when internet connectivity issues are detected.

## Background

My home network is centered around a NUC server running Pi-hole, Plex, and Home Assistant for home automation. The network infrastructure consists of a TP-Link Deco M4 mesh system with two separate networks:

1. A primary network for regular devices
2. A guest network for IoT devices (separate subnet for security isolation, as VLANs aren't supported on the Deco)

The NUC requires dual network connectivity:

- Primary connection via ethernet to the Deco router
- Secondary connection via Wi-Fi to the guest network (enables Home Assistant to communicate with IoT devices)

## The Problem

The Deco system exhibits a critical issue where it fails to re-establish internet connectivity after ISP maintenance or outages. When this occurs:

1. The WAN connection remains down even after ISP service is restored
2. The Deco's ethernet ports become unresponsive (possibly due to misidentifying them as WAN ports)
3. Remote access to Home Assistant (via Cloudflare tunnel) becomes impossible
4. Manual router reboot is required to restore connectivity

## Technical Quirks

During development, I discovered several interesting quirks that led to this seemingly complex solution:

1. 🤔 When the WAN connection drops, the Deco mysteriously makes all ethernet ports unresponsive - possibly misidentifying them as WAN ports
2. 🤡 The ethernet interface remains set as the default route even when unresponsive, creating a catch-22 for management access
3. 🔧 Traditional interface management (`ifup`/`ifdown`) proved unreliable, with interfaces sometimes refusing to come back up (NO-CARRIER state)
4. 🎉 Solution: Rather than bringing interfaces down, we just remove the route table entries - keeping the interface up but forcing traffic over Wi-Fi
5. 🔒 The Deco management portal isn't accessible via guest network (by design), requiring Wi-Fi network switching
6. 🔄 Restoring the network state isn't always reliable - sometimes `netplan apply` needs multiple attempts

## The Solution

This utility automatically handles recovery through a series of carefully orchestrated steps:

1. Monitors internet connectivity
2. Manages network routes to maintain access (rather than bringing interfaces down)
3. Switches Wi-Fi networks as needed for management access
4. Performs a controlled router reboot via web interface
5. Restores original network configuration

The solution may seem complex, but each component addresses specific technical constraints of the Deco system and Ubuntu networking behavior.

## Features

- Automated connectivity monitoring
- Automatic failover between Wi-Fi networks
- Selenium-based web automation for device reboot
- Network interface management
- Process locking to prevent concurrent executions

## Requirements

- Python 3.8+
- Firefox browser (for Selenium)
- `wpa_cli` for Wi-Fi management
- Root/sudo access for network operations

## Installation

1. Install uv:

```bash
pip install uv # for Windows use winget install uv
```

2. Clone the repository:

```bash
git clone <repository-url>
cd tp-link-deco-monitor
```

3. Create virtual environment and install required dependencies:

```bash
uv sync
```

## Configuration

Create a `.env` file with the following variables:

```env
PASSWORD=your_deco_password
BASE_URL=http://your_deco_ip
IFNAME=your_network_interface
```

## Usage

Run the monitor:

```bash
sudo python main.py
```

The script will:

1. Check internet connectivity
2. Switch to the primary Wi-Fi network if (Deco guest network does not have access to the router management page)
3. Remove the default ethernet route to ensure router access happens over the Wi-Fi connection
4. Reboot the Deco system
5. Restore network configuration

## License

MIT
