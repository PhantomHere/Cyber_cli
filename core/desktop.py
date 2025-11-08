import os
import importlib.util
from pathlib import Path
from core import utils
import sys

def get_modules_path():
    """Return correct modules directory depending on freeze status."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        base_path = Path(sys._MEIPASS)
        return base_path / 'modules'
    else:
        # Running as regular script
        script_path = Path(__file__).resolve()
        return script_path.parent.parent / 'modules'

MOD_PATH = get_modules_path()

def discover_apps(modules_path=MOD_PATH):
    apps = []
    for fname in os.listdir(modules_path):
        if fname.endswith(".py") and not fname.startswith("_"):
            fpath = os.path.join(modules_path, fname)
            spec = importlib.util.spec_from_file_location(fname[:-3], fpath)
            app_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_mod)
            # Only register valid app modules
            if hasattr(app_mod, "APP_INFO") and hasattr(app_mod, "launch"):
                apps.append((app_mod.APP_INFO, app_mod.launch))
    return apps

def show_desktop():
    utils.clear_console()
    apps = discover_apps()
    while True:
        print("\n<< Cyber_CLI Desktop >>")
        for idx, (info, _) in enumerate(apps, 1):
            print(f"[{idx}] {info.get('icon', '🟦')} {info.get('name', 'Unnamed App')}")
        print(f"[q] Quit Desktop")
        choice = input("Choose app > ").strip()
        if choice.lower() in ("q", "quit", "exit"):
            utils.clear_console()
            utils.logo_loader()
            break
        try:
            idx = int(choice) - 1
            _, launch_func = apps[idx]
            utils.clear_console()
            launch_func()
        except (ValueError, IndexError):
            utils.clear_console()
            print("Invalid selection.")

if __name__ == "__main__":
    show_desktop()




''' 
requires pip install pyinstaller and others import this cli expects from your env
to create an exe copy this into terminal - "pyinstaller --onefile --add-data "modules;modules" --add-data "settings;settings" cyber_cli_launch.py --hidden-import=platform --hidden-import=socket --hidden-import=requests --hidden-import=subprocess --hidden-import=bs4"
'''