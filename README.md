# Cyber_CLI 💾

A multi-functional, modular Command Line Interface (CLI) application suite built entirely in Python. Cyber_CLI is designed to showcase a desktop-like environment and a collection of useful, standalone command-line applications, including a real-time chat client, a network scanner, and a basic web browser.

## ✨ Features

* **Modular Desktop:** A core desktop system (`desktop.py`) that discovers and launches modules (apps) dynamically.
* **Customizable Settings:** Change the logo color and prompt character via the `Settings` app.
* **Real-Time Messenger:** A multi-threaded chat client (`messenger_work(probably).py`) that connects to a required standalone server (`messenger_server.py`).
* **Network Scanner:** An application (`net_scanner.py`) capable of:
    * **Port Scanning:** Scanning a target host (IP or hostname) for open ports within a specified range.
    * **Network Sweep:** Pinging local network IPs concurrently using a `ThreadPoolExecutor` to find active hosts.
* **CLI Web Browser:** A basic command-line web browser (`Browser.py`) that fetches and displays the main text content of a given URL, complete with basic text pagination.
* **System Info Reporter:** The `Settings` app includes a utility to display local and external network/system information (OS, IP, processor, etc.) using `platform`, `socket`, and `requests`.

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.x
* The following Python packages:
    ```bash
    pip install requests beautifulsoup4
    ```

### Running the Application

1.  **Clone the repository** (or ensure all provided files are in the correct directory structure, including `core/` and `modules/` folders).
2.  **Launch the CLI:**
    ```bash
    python cyber_cli_launch.py
    ```

### 💬 Messenger Setup (Optional)

To use the **Messenger** app, the separate server process must be running:

1.  Open a new terminal window.
2.  Run the server script:
    ```bash
    python messenger_server.py
    ```
3.  The Messenger app in the main CLI will now be able to connect to `127.0.0.1:55555`.

## 📂 Project Structure Overview

| File / Path | Description |
| :--- | :--- |
| `cyber_cli_launch.py` | The main entry point for the application. Initializes the logo and launches the desktop. |
| `desktop.py` | The core desktop manager. Discovers apps in the `modules/` folder and handles app launching. |
| `core/utils.py` | **Core utility functions.** Handles console clearing, colored text, logo display, and settings loading/saving. |
| `modules/settings.py` | The `Settings` application. Manages logo color, system info reporting (local and external IP). |
| `modules/Browser.py` | The `Cyb_browser` application. Fetches website content and displays it in the terminal. |
| `modules/messenger_work(probably).py` | The `Messenger` client application. Connects to the chat server using sockets and threads. |
| `messenger_server.py` | **The required standalone chat server.** Handles client connections, broadcasts, and disconnections. |
| `modules/net_scanner.py` | The `Network Scanner` application. Implements port scanning and network ping sweeping. |
| `settings/config.json` | Stores user settings like `logo_color` and `prompt_char`. |

## 📦 Building an Executable

The `desktop.py` file includes a template command for building a single-file executable using **PyInstaller**. This ensures all modules are correctly packaged.

> **NOTE:** You must have `PyInstaller` installed (`pip install pyinstaller`).

```bash
pyinstaller --onefile --add-data "modules;modules" --add-data "settings;settings" cyber_cli_launch.py --hidden-import=platform --hidden-import=socket --hidden-import=requests --hidden-import=subprocess --hidden-import=bs4
