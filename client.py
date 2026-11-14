import socket

HOST = "127.0.0.1"
PORT = 5555


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Connected to Tic-Tac-Toe server at {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure server.py is running first.")
        return

    try:
        # Step 1: Basic Login / Join Step (Week 8 Milestone)
        while True:
            username = input("Enter a username to join: ").strip()
            if not username:
                print("Username cannot be blank.")
                continue

            client.sendall(f"LOGIN {username}\n".encode("utf-8"))
            response = client.recv(1024).decode("utf-8").strip()
            print(f"Server: {response}")

            if response.startswith("OK"):
                break

        # Step 2: Keep session active for commands and concurrent testing
        print("\nCommands: STATUS (see online players), PING (test connection), QUIT (exit)")
        while True:
            cmd = input(f"[{username}] > ").strip()
            if not cmd:
                continue

            client.sendall(f"{cmd}\n".encode("utf-8"))
            reply = client.recv(1024).decode("utf-8").strip()

            if not reply:
                print("Server closed the connection.")
                break

            print(f"Server: {reply}")
            if cmd.upper() == "QUIT":
                break

    except (ConnectionResetError, BrokenPipeError):
        print("\nLost connection to the server.")
    except KeyboardInterrupt:
        print("\nExiting client...")
        try:
            client.sendall(b"QUIT\n")
        except Exception:
            pass
    finally:
        client.close()
        print("Disconnected.")


if __name__ == "__main__":
    run_client()