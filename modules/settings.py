APP_INFO = {
    "name": "Settings",
    "icon": "⚙️",
    "description": "Customize Cyber_CLI and view system information."
}

import time
import platform
from core import utils
import time
import socket
import requests

def change_logo_color():
    utils.Print_Typing(utils.Colors.col_text("\n--- Change logo color ---", utils.Colors.BRIGHT_MAGENTA) + "\n", fast=False)

    color_options = [
        "BRIGHT_CYAN", "BRIGHT_GREEN", "BRIGHT_YELLOW", 
        "BRIGHT_MAGENTA", "BRIGHT_BLUE", "RED"
    ]

    current_settings = utils.load_settings()
    current_color = current_settings.get("logo_color", "BRIGHT_CYAN")

    for i, color_name in enumerate(color_options, 1):
        color_code = getattr(utils.Colors, color_name)

        is_current = " (CURRENT)" if color_name == current_color else ""
        display_text = f"[{i}] {utils.Colors.col_text(color_name, color_code)}{is_current}"
        print(display_text)
    
    print(utils.Colors.col_text("[q] Cancel and return", utils.Colors.RED))

    choice = input("\nSelect a color number > ").strip()

    if choice.lower() == "q":
        return
    
    try:
        index = int(choice) - 1
        new_color_name = color_options[index]

        current_settings["logo_color"] = new_color_name
        utils.save_settings(current_settings)

        utils.Print_Typing(utils.Colors.col_text(
            f"\nSuccess! Logo color set to {new_color_name}.",
            utils.Colors.BRIGHT_GREEN
        ))

    except (ValueError, IndexError):
        utils.Colors.col_text("\nInvalid selection. Try again.", utils.Colors.RED)




def fetch_external_ip_info():
    try:
        response = requests.get('https://ipapi.co/json/', timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "External IP": data.get('ip', 'N/A'),
            "City": data.get('city', 'N/A'),
            "Region": data.get('region', 'N/A'),
            "Country": data.get('country_name', 'N/A'),
            "Organization": data.get('org', 'N/A')
        }
    except requests.exceptions.RequestException as e:
        return {"Error": f"Failed to fetch external IP data: {e}"}

def sys_info():
    utils.clear_console()
    utils.Print_Typing(utils.Colors.col_text("\n<< Sys Reporter: Generating Report >>", utils.Colors.BRIGHT_MAGENTA) + "\n", fast=False)
    
    report_data = {
        "--- System Information ---": None,
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Local Hostname": socket.gethostname(),
        "Local IP (Probable)": socket.gethostbyname(socket.gethostname()),
        "Python Version": platform.python_version(),
        
        "--- Network Information (External) ---": None,
    }
    
    utils.Print_Typing(utils.Colors.col_text("Fetching external network data (public API call)...", utils.Colors.BRIGHT_YELLOW))
    external_info = fetch_external_ip_info()
    report_data.update(external_info)
    
    print("\n" + "=" * 50)
    print(utils.Colors.col_text("SYSTEM AND NETWORK REPORT", utils.Colors.BRIGHT_GREEN).center(50))
    print("=" * 50)

    max_key_len = max(len(k) for k in report_data.keys() if report_data[k] is not None) + 2

    for key, value in report_data.items():
        if value is None:
            print(utils.Colors.col_text(f"\n{key}", utils.Colors.BRIGHT_MAGENTA))
            print("-" * len(key))
        else:
            formatted_line = f"{key.ljust(max_key_len)}: {utils.Colors.col_text(str(value), utils.Colors.BRIGHT_CYAN)}"
            print(formatted_line)

    print("\n" + "=" * 50)
    input(utils.Colors.col_text(f"\nReport Generated. Press Enter to return to Settings. . .", utils.Colors.BRIGHT_YELLOW))
    utils.clear_console()



def launch():
    while True:
        utils.clear_console()
        print(utils.Colors.col_text("\n<< Sys settings >>\n", utils.Colors.BRIGHT_MAGENTA))
        print("-"*33)
        print("[1] Change Logo Color")
        print("[2] Display System Info")
        print(utils.Colors.col_text("[q] Return to Desktop", utils.Colors.BRIGHT_YELLOW))

        choice = input(f"Choose option {utils.load_settings().get('prompt_char', '>')} ").strip().lower()
        if choice == "1":
            change_logo_color()
        elif choice == "2":
            sys_info()
        elif choice == "q":
            utils.clear_console()
            break
        else:
            print(utils.Colors.col_text("Invalid selection.", utils.Colors.RED))
            time.sleep(1)