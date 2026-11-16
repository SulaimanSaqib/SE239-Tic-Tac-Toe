# Milestone Verification & Test Notes (Weeks 6 & 8)
**Author:** Mohammed Fahiyan (Testing & Demo Lead)

## Environment
- **Language:** Python 3 (built-in `socket` and `threading` modules)
- **Host / Port:** `127.0.0.1:5555`

## Test Cases Executed

### 1. Week 6 Milestone: First Connection & Simple Message Exchange
- **Steps:** Started `server.py` in Terminal 1, started `client.py` in Terminal 2, logged in as `Sulaiman`, and sent `PING`.
- **Expected Result:** Server accepts TCP connection, prints connection log, and replies `PONG Server is alive!`.
- **Actual Result:** Passed. Connection established and message echoed properly.

### 2. Week 8 Milestone: Concurrent Multi-Client Connections (3+ Clients)
- **Steps:** Kept `server.py` running and opened three separate client terminals simultaneously:
  - Client 1 logged in as `Sulaiman`
  - Client 2 logged in as `Khaled`
  - Client 3 logged in as `Ibrahim`
  - Executed `STATUS` from Client 3.
- **Expected Result:** All 3 clients remain connected concurrently on separate threads, and `STATUS` returns all 3 usernames (`Online (3): Sulaiman, Khaled, Ibrahim`).
- **Actual Result:** Passed. All 3 clients connected and interacted simultaneously without blocking each other.

### 3. Duplicate Username & Clean Disconnect Check
- **Steps:** Attempted to log in with an already active username (`Sulaiman`), then tested `QUIT` on one client while running `STATUS` on a remaining client.
- **Expected Result:** Server rejects duplicate username with `ERR Username already taken.`, and after one client quits, the server stays online and updates the active count to `2`.
- **Actual Result:** Passed. Server handled disconnect cleanly with zero crashes.