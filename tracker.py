# tracker.py
import socket
import threading

peers = {}

def handle_client(conn, addr):
    try:
        peer_name = conn.recv(1024).decode()
        peers[peer_name] = addr[0]
        print(f"[REGISTERED] {peer_name} at {addr[0]}")

        while True:
            data = conn.recv(1024).decode()
            if data == "LIST":
                response = "\n".join([f"{k}:{v}" for k, v in peers.items()])
                conn.sendall(response.encode())
    except:
        pass
    finally:
        conn.close()

def main():
    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.bind(('0.0.0.0', 9000))
    tracker.listen(5)
    print("[TRACKER STARTED ON PORT 9000]")

    while True:
        conn, addr = tracker.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
