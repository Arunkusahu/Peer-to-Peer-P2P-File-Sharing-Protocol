import socket
import threading
import os

SHARED_FOLDER = 'shared'
DOWNLOAD_FOLDER = 'downloads'
TRACKER_IP = '127.0.0.1'  # Change if tracker is on another machine
TRACKER_PORT = 9000

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 0))  # bind to any free port
    server.listen(5)
    port = server.getsockname()[1]
    print(f"[SERVER STARTED] Listening on port {port}")

    def handle_client(conn):
        try:
            request = conn.recv(1024).decode()
            if request.startswith("MSG:"):
                msg = request[4:]
                print(f"\n[MESSAGE RECEIVED] {msg}")
            elif request.startswith("GET:"):
                filename = request[4:]
                path = os.path.join(SHARED_FOLDER, filename)
                if os.path.exists(path):
                    print(f"[SENDING FILE] {filename} to client")
                    with open(path, 'rb') as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            conn.sendall(chunk)
                    print(f"[FILE SENT] {filename}")
                else:
                    print(f"[FILE NOT FOUND] {filename}")
                    conn.sendall(b"File not found.")
        except Exception as e:
            print(f"[ERROR] Handling client: {e}")
        finally:
            conn.close()

    def listen():
        while True:
            try:
                conn, _ = server.accept()
                threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
            except Exception as e:
                print(f"[ERROR] Accepting connections: {e}")
                break

    threading.Thread(target=listen, daemon=True).start()
    return port

def register_to_tracker(peer_name, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TRACKER_IP, TRACKER_PORT))
        # Send peer info as "peer_name:port"
        registration_info = f"{peer_name}:{port}"
        sock.sendall(registration_info.encode())
        return sock
    except Exception as e:
        print(f"[ERROR] Connecting to tracker: {e}")
        return None

def get_peer_list(sock):
    try:
        sock.sendall("LIST".encode())
        peers = sock.recv(4096).decode()
        return peers
    except Exception as e:
        print(f"[ERROR] Getting peer list: {e}")
        return ""

def send_message(ip, port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.sendall(f"MSG:{message}".encode())
        s.close()
        print("[MESSAGE SENT]")
    except Exception as e:
        print(f"[ERROR] Sending message: {e}")

def send_file(ip, port, filename):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.sendall(f"GET:{filename}".encode())

        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        data = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        s.close()

        if data.startswith(b"File not found"):
            print(f"[ERROR] File '{filename}' not found on peer {ip}:{port}")
            return

        with open(filepath, 'wb') as f:
            f.write(data)
        print(f"[FILE DOWNLOADED] Saved to {filepath}")
    except Exception as e:
        print(f"[ERROR] Downloading file: {e}")

def main():
    peer_name = input("Enter your peer name: ").strip()
    if not peer_name:
        print("Peer name cannot be empty.")
        return

    os.makedirs(SHARED_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    port = start_server()
    tracker_conn = register_to_tracker(peer_name, port)

    if not tracker_conn:
        print("[ERROR] Could not connect to tracker. Exiting...")
        return

    while True:
        print("\nMenu:")
        print("1. Show Peers")
        print("2. Send Message")
        print("3. Download File")
        choice = input("Choice: ").strip()

        if choice == '1':
            peers = get_peer_list(tracker_conn)
            print("\n[PEERS]")
            print(peers if peers else "No peers found.")
        elif choice == '2':
            ip = input("Enter peer IP: ").strip()
            port_ = input("Enter peer port: ").strip()
            msg = input("Enter message: ").strip()
            send_message(ip, port_, msg)
        elif choice == '3':
            ip = input("Enter peer IP: ").strip()
            port_ = input("Enter peer port: ").strip()
            filename = input("Enter filename to download: ").strip()
            send_file(ip, port_, filename)
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
