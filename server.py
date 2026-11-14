import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

# Maps connected client socket -> logged-in username
active_clients = {}
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    username = None

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode("utf-8").strip()
            if not message:
                continue

            print(f"[{addr}] Received: {message}")
            parts = message.split(" ", 1)
            command = parts[0].upper()

            if command == "LOGIN":
                if len(parts) < 2 or not parts[1].strip():
                    conn.sendall(b"ERR Username cannot be empty.\n")
                    continue

                requested_user = parts[1].strip()
                with clients_lock:
                    if requested_user in active_clients.values():
                        conn.sendall(b"ERR Username already taken.\n")
                    else:
                        active_clients[conn] = requested_user
                        username = requested_user
                        conn.sendall(f"OK Welcome {username}! Connected players: {len(active_clients)}\n".encode("utf-8"))
                        print(f"[LOGIN] {username} joined from {addr}. Total online: {len(active_clients)}")

            elif command == "STATUS":
                with clients_lock:
                    if not active_clients:
                        conn.sendall(b"STATUS Online players: None\n")
                    else:
                        users_list = ", ".join(active_clients.values())
                        conn.sendall(f"STATUS Online ({len(active_clients)}): {users_list}\n".encode("utf-8"))

            elif command == "PING":
                # Simple message exchange check for Week 6 milestone
                conn.sendall(b"PONG Server is alive!\n")

            elif command == "QUIT":
                conn.sendall(b"BYE Disconnecting cleanly.\n")
                break

            else:
                conn.sendall(b"ERR Unknown command. Use LOGIN <username>, STATUS, PING, or QUIT.\n")

    except (ConnectionResetError, BrokenPipeError):
        print(f"[DISCONNECT] {addr} disconnected unexpectedly.")
    except Exception as e:
        print(f"[ERROR] Unexpected error with {addr}: {e}")
    finally:
        with clients_lock:
            if conn in active_clients:
                removed_user = active_clients.pop(conn)
                print(f"[LOGOUT] {removed_user} left. Remaining online: {len(active_clients)}")
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Tic-Tac-Toe Server listening on {HOST}:{PORT}...")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE THREADS] {threading.active_count() - 1} client thread(s) running.")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()