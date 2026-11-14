# SE239 Tic-Tac-Toe Message Protocol & Data Design
**Author:** Ibrahim Shareef (Messages & Data Lead)

## 1. Transport & Encoding
- **Protocol:** TCP Sockets (`AF_INET`, `SOCK_STREAM`)
- **Encoding:** UTF-8 plain-text commands delimited by newlines (`\n`)

## 2. Client-to-Server Commands (Weeks 6 & 8)

| Command | Format | Description |
| :--- | :--- | :--- |
| **PING** | `PING` | Tests basic client-server message exchange (Week 6 check). |
| **LOGIN** | `LOGIN <username>` | Registers a unique username for the connected client session (Week 8 check). |
| **STATUS** | `STATUS` | Requests the total count and usernames of all currently connected players. |
| **QUIT** | `QUIT` | Cleanly closes the client session and removes the user from the active list. |

## 3. Server-to-Client Responses

| Response Prefix | Example | Meaning |
| :--- | :--- | :--- |
| `PONG` | `PONG Server is alive!` | Confirms the server received a `PING` message. |
| `OK` | `OK Welcome Sulaiman! Connected players: 3` | Login succeeded and session is registered. |
| `STATUS` | `STATUS Online (3): Sulaiman, Khaled, Ibrahim` | Lists all active players currently connected to the server. |
| `BYE` | `BYE Disconnecting cleanly.` | Confirms client disconnect request before closing socket. |
| `ERR` | `ERR Username already taken.` | Indicates invalid command syntax or duplicate username. |

## 4. Server Data Storage (In-Memory)
- `active_clients`: A Python dictionary mapping `{client_socket: username}` for all logged-in clients.
- `clients_lock`: A `threading.Lock()` object ensuring thread-safe reads and writes when multiple clients join or disconnect simultaneously.