import socket

import globals as g

# Check if the connection is alive
def check_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((g.TARGET_ADDR, g.TARGET_PORT))
            s.close()
            print("True")
            return True
        except ConnectionRefusedError:
            print("False")
            return False
        except ConnectionResetError:
            print("CRE")
            continue

check_connection()