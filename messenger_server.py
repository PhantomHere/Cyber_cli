# messenger_server.py
# This script must be running for the 'messenger.py' app to work.
import socket
import threading
import time

# --- SERVER CONFIGURATION ---
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 55555      # A high-numbered, unused port

# --- GLOBAL STATE ---
clients = []
usernames = []
# Using simple ANSI escape codes for server status colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

def broadcast(message, sender_client=None):
    """Sends a message to all connected clients."""
    for client in clients:
        # Don't send the message back to the sender
        if client != sender_client:
            try:
                client.send(message)
            except:
                # Handle broken connections silently
                remove_client(client)

def remove_client(client):
    """Removes a disconnected client."""
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        clients.remove(client)
        usernames.remove(username)
        print(f"{YELLOW}[DISCONNECT]{ENDC} {username} has left the chat.")
        broadcast(f"{username} left the chat.".encode('utf-8'))
        
def handle_client(client, addr):
    """Handles all communication for a single client connection."""
    
    # First message from client must be the username
    try:
        username = client.recv(1024).decode('utf-8')
        if not username:
            client.close()
            return
    except:
        client.close()
        return

    usernames.append(username)
    clients.append(client)
    
    print(f"{GREEN}[NEW CONNECTION]{ENDC} {username} connected from {addr}")
    broadcast(f"{username} joined the chat.".encode('utf-8'), client)
    
    while True:
        try:
            # Keep receiving message data
            message = client.recv(1024)
            if not message:
                # Empty message means the client gracefully disconnected
                break
                
            # Prepend the username to the message and broadcast
            full_message = f"<{username}>: ".encode('utf-8') + message
            print(f"[{time.strftime('%H:%M:%S')}] {full_message.decode('utf-8').strip()}")
            broadcast(full_message, client)
            
        except:
            # Client abruptly disconnected
            break

    # Cleanup when the loop breaks
    remove_client(client)
    client.close()

def start_server():
    """Main server loop to listen for connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"\n{GREEN}<< Messenger Server Running >>{ENDC}")
        print(f"Listening on {HOST}:{PORT}")
        
    except Exception as e:
        print(f"{RED}ERROR: Could not start server. {e}{ENDC}")
        return

    while True:
        try:
            client, addr = server.accept()
            # Start a new thread for every connected client
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.start()
            print(f"{YELLOW}[STATUS]{ENDC} Active connections: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Server shut down by user.{ENDC}")
            server.close()
            break
        except Exception as e:
            print(f"{RED}Error accepting connection: {e}{ENDC}")
            time.sleep(1)

if __name__ == '__main__':
    start_server()