import ssl
import socket
import json


def send_msg(msg, port):
    message = json.dumps(msg)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ssl_context = ssl.create_default_context()
        # ssl_sock = ssl_context.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
        ssl_sock = sock
        ssl_sock.connect(('127.0.0.1', port))
    except:
       print("User Could not make a connection to the server at localhost:" + str(port))
       return

    ssl_sock.sendall(str.encode(message))
    reply_message = ssl_sock.recv(4096)
    reply_message = str(reply_message.decode("utf-8"))

    reply_message = json.loads(reply_message)
    return reply_message
