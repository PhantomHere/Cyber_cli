import shutil
from pathlib import Path
import os
import time
import json

DEFAULT_SETTINGS = {
    "logo_color": "BRIGHT_GREEN",
    "typing_delay": 0.01,
    "prompt_char": ">",
}

script_path = Path(__file__).resolve()
SETTINGS_FILE = script_path.parent.parent / 'settings' / 'config.json'

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            return {**DEFAULT_SETTINGS, **settings}
    except FileNotFoundError:
        print("\nCreating default configuration file...")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    except json.JSONDecodeError:
        print("\nERROR: Configuration file corrupted. Resetting to defaults.")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(data):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"\nERROR saving settings: {e}")
            
def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

class Colors():
    RESET = '\033[0m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_BLUE = '\033[94m'
    RED = '\033[31m'
    def col_text(text, color_code):
        return f"{color_code}{text}{Colors.RESET}"

def logo_loader(delay=1.5):
    clear_console()
    script_path = Path(__file__).resolve()
    logo_path = script_path.parent.parent / 'settings' / 'logo.txt'

    settings = load_settings()
    color_name = settings.get("logo_color", "BRIGHT_CYAN")

    try:
        color_code = getattr(Colors, color_name)
    except AttributeError:
        color_code = Colors.BRIGHT_CYAN

    try:
        try:
            terminal_width = shutil.get_terminal_size().columns
        except OSError:
            terminal_width = 80
            
        print()

        with open(logo_path, 'r') as file:
            for line in file:
                 clean_line = line.strip()
                 centered_line = clean_line.center(terminal_width)
                 colored_line = Colors.col_text(centered_line, color_code=color_code)
                 print(colored_line)
            
    except FileNotFoundError:
        print(f"\nERROR: Logo file not found. Checked path: {logo_path}\n") 
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
    time.sleep(delay)
    clear_console()


def Print_Typing(text, delay=0.05, center=False, fast=True):
    if center:
        try:
            terminal_width = shutil.get_terminal_size().columns
            padding = terminal_width - (len(text))/2
            print(padding * " ", end="")
        except OSError:
            center = False

    for char in text:
        print(char, end="", flush=True)
        if fast:
            time.sleep(delay)





if __name__ == "__main__":
    logo_loader()
    a = input()
    Print_Typing(Colors.col_text(a, color_code=Colors.RED))