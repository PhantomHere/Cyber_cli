APP_INFO = {
    "name": "Example App",
    "icon": "💡",
    "description": "A demo app."
}

from core import utils

def launch():
    print("\n--- Welcome to the Example App! ---")
    while True:
        user_input = input("Type 'exit' to return to desktop: ").strip().lower()
        if user_input in ("exit", "quit", "q"):
            print("Exiting Example App...\n")
            utils.clear_console()
            break
        else:
            print("Unknown command. Try typing 'exit'.")