import ssl
import socket
import json


def send_msg(msg, port):
    message = json.dumps(msg)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ssl_context = ssl.create_default_context()
        # ssl_sock = ssl_context.wrap_socket(sock)
        # ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
        try:
            key_file_path = './certificates/CA/client-key.pem'
            cert_file_path = './certificates/CA/client_cert.pem'
            ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS, ciphers="TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256", keyfile=key_file_path, certfile=cert_file_path)
        except:
            ssl_sock = sock
        ssl_sock.connect(('127.0.0.1', port))
    except:
       print("User Could not make a connection to the server at localhost:" + str(port))
       return

    ssl_sock.sendall(str.encode(message))
    reply_message = ssl_sock.recv(4096)
    reply_message = str(reply_message.decode("utf-8"))

    reply_message = json.loads(reply_message)
    ssl_sock.close()
    return reply_message
