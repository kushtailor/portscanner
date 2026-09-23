# Port Scanner v1.0

A lightweight, multi-threaded TCP port scanner written in pure Python — no external dependencies. Built as a hands-on exercise in socket programming, service banner grabbing, and basic network reconnaissance.

## Features

- **TCP Connect Scanning** — full `connect()` attempts to detect open ports
- **Banner Grabbing** — reads service responses (with a targeted HTTP probe on web ports) to help identify what's running
- **Three scan modes** — Fast, Common, and Stealth (see below)
- **Multi-threaded** — the Fast mode scans ports 1–1000 concurrently
- **Auto-saved reports** — every run writes a plain-text report to `<target>_portscan.txt`

## Requirements

- Python 3.x
- No third-party packages — only the standard library (`socket`, `threading`, `argparse`, `datetime`, `time`)

## Installation

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

No `pip install` needed.

## Usage

```bash
python3 portscanner.py -t <target> -m <mode>
```

| Flag | Description |
|------|--------------|
| `-t`, `--target` | Target IP address or hostname |
| `-m`, `--mode` | Scan mode: `fast`, `common`, or `stealth` |

### Examples

```bash
python3 portscanner.py -t 192.168.1.10 -m fast      # ports 1-1000, all threads at once
python3 portscanner.py -t example.com  -m common    # 14 well-known ports, sequential
python3 portscanner.py -t example.com  -m stealth    # same ports, 1.5s delay between probes
```

## Scan Modes

| Mode | Port Range | Behavior |
|------|------------|----------|
| **Fast** | 1–1000 | All threads launched at once — quickest, heaviest footprint |
| **Common** | 14 well-known ports (FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, RPC, NetBIOS, HTTPS, SMB, RDP, WinRM, HTTP-Alt) | Sequential, quick targeted check |
| **Stealth** | Same 14 ports as Common | 1.5s delay between each probe — lighter traffic burst |

## Sample Output

```
$ python3 portscanner.py -t 127.0.0.1 -m common

Target     : 127.0.0.1
IP Address : 127.0.0.1
Mode       : common

[*] Starting common port scan

SCAN RESULTS
Open Ports Found: 1
[+] 8080  HTTP-Alt   | Banner: HTTP/1.0 200 OK  Server: SimpleHTTP/0.6 Python/3.12.3

Scan Complete
[+] Results saved to: 127.0.0.1_portscan.txt
```

## Project Structure

```
.
├── portscanner.py   # main script
└── README.md
```

## Limitations

- TCP only — no UDP scanning
- Banners are truncated to 200 characters
- No OS or service-version fingerprinting

## Possible Improvements

- Add a UDP scan mode
- Export results as JSON/CSV
- Match grabbed banners against a CVE/service-version database

## Disclaimer

This tool is for educational use and authorized security testing only. Only scan hosts and networks you own or have explicit permission to test. Unauthorized scanning may violate the law depending on your jurisdiction.

## License

No license is currently specified. If you plan to share this publicly, consider adding one (e.g., the MIT License) so others know how they may use the code
