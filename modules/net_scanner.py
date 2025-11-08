APP_INFO = {
    "name": "Network Scanner",
    "icon": "🔍",
    "description": "Scans a host for open ports or sweeps the local network for active hosts."
}

from core import utils
import time
import socket
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor

# --- Helper Functions for Network Scanning ---

def get_local_ip():
    """Fetches the local IP address using a common socket trick."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a non-existent external address (like a DNS server) to find the correct local interface IP.
        s.connect(('8.8.8.8', 1)) 
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_ip_range_for_sweep(local_ip):
    """Infers the /24 subnet range (1-254) from the local IP."""
    # e.g., '192.168.1.100' -> '192.168.1.'
    if local_ip == '127.0.0.1':
        # Cannot sweep from localhost. Return an empty list or an error message.
        return []
        
    network_prefix = ".".join(local_ip.split('.')[:-1]) + "."
    # Create a list of all 254 possible host IPs in the /24 subnet
    return [network_prefix + str(i) for i in range(1, 255)]

def is_host_alive(ip):
    """Checks if a host is alive using the system's ping command."""
    # Use platform-specific flags for reliability
    if platform.system().lower() == "windows":
        command = ['ping', '-n', '1', '-w', '100', ip] # -n 1 packet, -w 100ms timeout
    else:
        command = ['ping', '-c', '1', '-W', '1', ip] # -c 1 packet, -W 1 second timeout

    try:
        # Run the ping command, suppressing output
        result = subprocess.run(
            command,
            timeout=1, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        # Return the IP if the ping was successful (returncode 0)
        return ip if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def threaded_ping_sweep():
    """Orchestrates the local network sweep."""
    local_ip = get_local_ip()
    ip_list = get_ip_range_for_sweep(local_ip)
    
    if not ip_list:
        utils.Print_Typing(utils.Colors.col_text("\n[ERROR] Cannot sweep. Local IP is '127.0.0.1' or network lookup failed.", utils.Colors.RED))
        return

    utils.Print_Typing(utils.Colors.col_text(f"\nLocal IP: {local_ip}", utils.Colors.BRIGHT_MAGENTA))
    utils.Print_Typing(f"Sweeping local network ({'.'.join(local_ip.split('.')[:-1])}.1-254) for active hosts (20 threads)...", delay=0.01)
    
    active_hosts = []
    
    # Use a thread pool for concurrent checking (max_workers=20 for speed)
    with ThreadPoolExecutor(max_workers=20) as executor:
        # The executor maps the function 'is_host_alive' to all IPs in 'ip_list'
        # This runs 20 pings simultaneously.
        results = executor.map(is_host_alive, ip_list)
        
        # Filter and collect successful results
        for ip in results:
            if ip is not None:
                active_hosts.append(ip)
                print(utils.Colors.col_text(f"[ACTIVE] Host found at {ip}", utils.Colors.BRIGHT_GREEN))

    print("\n" + "=" * 50)
    if active_hosts:
        utils.Print_Typing(utils.Colors.col_text(f"Sweep Complete. {len(active_hosts)} device(s) found.", utils.Colors.BRIGHT_GREEN))
        print("Active IPs: " + ", ".join(active_hosts))
    else:
        utils.Print_Typing(utils.Colors.col_text("Sweep Complete. No other active hosts detected.", utils.Colors.BRIGHT_YELLOW))
    print("=" * 50)

# --- Port Scanning (Refactored from previous) ---

def scan_ports(host, start_port, end_port):
    """Attempts to connect to a range of ports on a specified host."""
    
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        utils.Print_Typing(utils.Colors.col_text(f"\n[ERROR] Hostname '{host}' could not be resolved.", utils.Colors.RED))
        return

    utils.Print_Typing(utils.Colors.col_text(f"\nTarget Host: {host} ({ip})", utils.Colors.BRIGHT_CYAN))
    utils.Print_Typing(f"Scanning ports {start_port} to {end_port}...", delay=0.01)
    print("-" * 40)

    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1) 
        
        # Check connection (connect_ex is faster and avoids exceptions on refusal)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            open_ports.append(port)
            print(utils.Colors.col_text(f"[OPEN] Port {port}", utils.Colors.BRIGHT_GREEN))
        # else: # Removed printing closed ports to make output cleaner
        #     print(f"[CLOSED] Port {port}") 

    print("-" * 40)
    if open_ports:
        utils.Print_Typing(utils.Colors.col_text(f"Scan Complete. {len(open_ports)} port(s) open.", utils.Colors.BRIGHT_GREEN))
        print(f"Open Ports: {', '.join(map(str, open_ports))}")
    else:
        utils.Print_Typing(utils.Colors.col_text("Scan Complete. No open ports found in range.", utils.Colors.BRIGHT_YELLOW))

# --- Application Launch ---

def launch():
    prompt_char = utils.load_settings().get('prompt_char', '>')
    while True:
        utils.clear_console()
        print(utils.Colors.col_text("\n<< Network Scanner >>", utils.Colors.BRIGHT_MAGENTA))
        print("Usage:")
        print("  - " + utils.Colors.col_text("scan <host> <start_port> <end_port>", utils.Colors.BRIGHT_CYAN))
        print("    Example: scan localhost 20 80 (Scan the current PC)")
        print("    Example: scan 192.168.1.1 22 443 (Scan a remote IP)")
        print("  - " + utils.Colors.col_text("sweep", utils.Colors.BRIGHT_CYAN) + " (Ping sweep the local network)")
        print("\nType 'exit' to return to desktop.")
        
        user_input = input(f"Scan {prompt_char} ").strip()
        
        if user_input.lower() in ("exit", "quit", "q"):
            utils.Print_Typing("Closing Network Scanner...")
            utils.clear_console()
            break
        
        parts = user_input.split()
        command = parts[0].lower() if parts else ""

        if command == 'sweep':
            threaded_ping_sweep()
            input(utils.Colors.col_text(f"\nPress Enter to continue. . .", utils.Colors.BRIGHT_YELLOW))
            continue
            
        elif command == 'scan' and len(parts) == 4:
            try:
                host = parts[1]
                start_port = int(parts[2])
                end_port = int(parts[3])
                
                if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
                    utils.Print_Typing(utils.Colors.col_text("\nPorts must be between 1 and 65535, and start port must be <= end port.", utils.Colors.RED))
                    time.sleep(1)
                    continue

                scan_ports(host, start_port, end_port)
                input(utils.Colors.col_text(f"\nPress Enter to continue. . .", utils.Colors.BRIGHT_YELLOW))
                
            except ValueError:
                utils.Print_Typing(utils.Colors.col_text("\nPorts must be valid numbers.", utils.Colors.RED))
                time.sleep(1)
            except Exception as e:
                utils.Print_Typing(utils.Colors.col_text(f"\nAn unexpected error occurred: {e}", utils.Colors.RED))
                time.sleep(1)

        else:
            utils.Print_Typing(utils.Colors.col_text("\nInvalid command or arguments. Check usage above.", utils.Colors.RED))
            time.sleep(1)