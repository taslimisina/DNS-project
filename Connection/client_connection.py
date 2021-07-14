import ssl
import threading
import socket
import json

class Client_Connection:
    def __init__(self, host, port, message):
        message = json.dumps(message)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
            ssl_sock.connect((host, port))
        except:
            print("User Could not make a connection to the server at " + str(host) + " port " + str(prot))
            return

        ssl_sock.sendall(str.encode(message))
        reply_message = ssl_sock.recv(4096)
        reply_message = str(reply_message.decode("utf-8"))

        reply_message = json.loads(reply_message)
        return reply_message
