# messenger.py
APP_INFO = {
    "name": "Messenger",
    "icon": "💬",
    "description": "Real-time command-line chat client."
}

from core import utils
import socket
import threading
import sys
import time

# --- CLIENT CONFIGURATION (Must match server) ---
HOST = '127.0.0.1'  # Connect to the local machine where the server is running
PORT = 55555      

def receive_messages(client_socket):
    """Thread function to continuously listen for and display messages."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Server shut down or connection lost
                sys.stdout.write(utils.Colors.col_text("\n[CONNECTION LOST] Server closed the connection.", utils.Colors.RED) + "\n")
                # This breaks the loop, and the thread dies.
                break 
                
            # Clear current input line and print new message
            sys.stdout.write("\r" + " " * 80 + "\r") # Clear line
            sys.stdout.write(message + "\n")
            
            # Re-draw the prompt
            prompt_char = utils.load_settings().get('prompt_char', '>')
            sys.stdout.write(f"Message {prompt_char} ")
            sys.stdout.flush()

        except OSError:  # Closed socket
            break
        except Exception as e:
            # print(f"An error occurred in receiving: {e}") 
            break

def write_messages(client_socket):
    """Main thread loop for user input and sending messages."""
    prompt_char = utils.load_settings().get('prompt_char', '>')
    while True:
        try:
            # Input is taken in the main thread
            message = input(f"Message {prompt_char} ")

            if message.lower() in ('/quit', 'exit', 'q'):
                client_socket.send("/quit".encode('utf-8'))
                return # Exit the main loop
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            
        except EOFError: # Catch Ctrl+D on Unix systems
            client_socket.send("/quit".encode('utf-8'))
            return
        except Exception as e:
            # print(f"An error occurred in writing: {e}")
            break


def launch():
    utils.clear_console()
    print(utils.Colors.col_text("\n<< Messenger Client >>", utils.Colors.BRIGHT_MAGENTA))
    
    # 1. Get Username
    username = input("Enter your chat username: ").strip()
    if not username:
        utils.Print_Typing(utils.Colors.col_text("Username required. Exiting...", utils.Colors.RED))
        time.sleep(1)
        utils.clear_console()
        return

    # 2. Connect to Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        utils.Print_Typing(utils.Colors.col_text(f"Connecting to {HOST}:{PORT}...", utils.Colors.BRIGHT_YELLOW))
        client.connect((HOST, PORT))
        
        # Send username immediately
        client.send(username.encode('utf-8'))
        utils.Print_Typing(utils.Colors.col_text("Connected! Type '/quit' to exit.", utils.Colors.BRIGHT_GREEN))
        
    except ConnectionRefusedError:
        utils.Print_Typing(utils.Colors.col_text("\n[ERROR] Connection refused. Is the server running?", utils.Colors.RED))
        time.sleep(2)
        utils.clear_console()
        return
    except Exception as e:
        utils.Print_Typing(utils.Colors.col_text(f"\n[ERROR] Could not connect: {e}", utils.Colors.RED))
        time.sleep(2)
        utils.clear_console()
        return
    
    # 3. Start Listener Thread
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True # Allows the main program to exit even if this thread is running
    receive_thread.start()
    
    # 4. Start Writer Loop (main thread)
    write_messages(client)
    
    # 5. Cleanup
    client.close()
    utils.Print_Typing(utils.Colors.col_text("Disconnected from chat.", utils.Colors.BRIGHT_YELLOW))
    time.sleep(1)
    utils.clear_console()