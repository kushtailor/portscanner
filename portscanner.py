import socket
import datetime
import time
import threading
import argparse


# ==============================
# PORT SCANNER BANNER
# ==============================

def show_banner():
    print(r"""
 ________  ____  ____  ______   _________  ________
|_   __  ||_  _||_  _||_   _ \ |  _   _  ||_   __  |
  | |_ \_|  \ \  / /    | |_) ||_/ | | \_|  | |_ \_|
  |  _|      \ \/ /     |  __/     | |      |  _|
 _| |_       _|  |_    _| |_       _| |_    _| |_
|_____|     |______|  |_____|     |_____|  |_____|

              PORT SCANNER v1.0
          Network Reconnaissance Tool
    """)


# ==============================
# BANNER GRABBING
# ==============================

def grab_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        sock.connect((ip, port))

        # Send HTTP request to web servers
        if port in [80, 8080, 8000, 8888]:
            request = (
                "HEAD / HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )

            sock.send(request.encode())

        elif port == 443:
            # Don't send normal HTTP because HTTPS expects TLS.
            # Just attempt to receive anything the service may provide.
            pass

        banner = sock.recv(2048).decode(
            "utf-8",
            errors="ignore"
        ).strip()

        sock.close()

        if banner:
            return banner.replace("\r", " ").replace("\n", " ")[:200]

        return "No banner"

    except (socket.timeout, socket.error, ConnectionError):
        return "No banner"

    finally:
        try:
            sock.close()
        except:
            pass


# ==============================
# PORT SCANNING
# ==============================

def scan_port(target, port, open_ports, lock):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:

            banner = grab_banner(target, port)

            with lock:
                open_ports.append((port, banner))

    except socket.error:
        pass

    finally:
        sock.close()


# ==============================
# FAST SCAN
# ==============================

def fast_scan(target, open_ports, lock):

    threads = []

    print("\n[*] Starting fast scan: ports 1-1000")

    for port in range(1, 1001):

        thread = threading.Thread(
            target=scan_port,
            args=(target, port, open_ports, lock)
        )

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


# ==============================
# COMMON PORT SCAN
# ==============================

def common_scan(target, open_ports, lock):

    ports = [
        21, 22, 23, 25, 53,
        80, 110, 135, 139,
        443, 445, 3389,
        5985, 8080
    ]

    print("\n[*] Starting common port scan")

    for port in ports:
        scan_port(target, port, open_ports, lock)


# ==============================
# STEALTH SCAN
# ==============================

def stealth_scan(target, open_ports, lock):

    ports = [
        21, 22, 23, 25, 53,
        80, 110, 135, 139,
        443, 445, 3389,
        5985, 8080
    ]

    print("\n[*] Starting stealth scan")

    for port in ports:

        scan_port(
            target,
            port,
            open_ports,
            lock
        )

        # Delay between requests
        time.sleep(1.5)


# ==============================
# MAIN
# ==============================

def main():

    show_banner()

    parser = argparse.ArgumentParser(
        description="PORT SCANNER v1.0"
    )

    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=["fast", "common", "stealth"],
        help="Scan mode"
    )

    args = parser.parse_args()

    target = args.target
    mode = args.mode

    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n[-] Unable to resolve target")
        return

    open_ports = []
    lock = threading.Lock()

    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "RPC",
        139: "NetBIOS",
        443: "HTTPS",
        445: "SMB",
        3389: "RDP",
        5985: "WinRM",
        8080: "HTTP-Alt"
    }

    print("=" * 60)
    print(f"Target     : {target}")
    print(f"IP Address : {target_ip}")
    print(f"Mode       : {mode}")
    print(f"Started    : {datetime.datetime.now()}")
    print("=" * 60)

    # Select scan mode
    if mode == "fast":

        fast_scan(
            target_ip,
            open_ports,
            lock
        )

    elif mode == "common":

        common_scan(
            target_ip,
            open_ports,
            lock
        )

    elif mode == "stealth":

        stealth_scan(
            target_ip,
            open_ports,
            lock
        )

    # Sort ports numerically
    open_ports.sort(key=lambda x: x[0])

    # ==============================
    # RESULTS
    # ==============================

    print("\n" + "=" * 60)
    print("SCAN RESULTS")
    print("=" * 60)

    print(f"Open Ports Found: {len(open_ports)}")

    if not open_ports:

        print("\n[-] No open ports found.")

    else:

        for port, banner in open_ports:

            service = services.get(
                port,
                "Unknown"
            )

            print(
                f"[+] {port:<5} "
                f"{service:<10} "
                f"| Banner: {banner}"
            )

    print("=" * 60)
    print("Scan Complete")
    print("=" * 60)

    # ==============================
    # SAVE RESULTS
    # ==============================

    filename = (
        target.replace("/", "_")
        + "_portscan.txt"
    )

    with open(filename, "w") as file:

        file.write("PORT SCANNER v1.0\n")
        file.write("=" * 60 + "\n")
        file.write(f"Target: {target}\n")
        file.write(f"IP: {target_ip}\n")
        file.write(f"Mode: {mode}\n")
        file.write(
            f"Started: {datetime.datetime.now()}\n"
        )
        file.write("=" * 60 + "\n\n")

        for port, banner in open_ports:

            service = services.get(
                port,
                "Unknown"
            )

            file.write(
                f"Port {port} "
                f"({service}) "
                f"- Banner: {banner}\n"
            )

    print(f"\n[+] Results saved to: {filename}")


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()
