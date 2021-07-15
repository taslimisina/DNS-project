import ssl
import threading
import socket
import json


class ServerConnection:
    def __init__(self, process_fnc, port):
        self.process_fnc = process_fnc

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ssl_context = ssl.create_default_context()
        # ssl_sock = ssl_context.wrap_socket(sock)
        # ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS, ciphers="ADH-AES256-SHA")
        try:
            key_file_path = './certificates/CA/ca_private.pem'
            cert_file_path = './certificates/CA/ca_cert.pem'
            ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS, server_side=True, ciphers="TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256", keyfile=key_file_path, certfile=cert_file_path)
        except:
            ssl_sock = sock
        
        
        ssl_sock.bind(('127.0.0.1', port))

        ssl_sock.listen(5)

        self.receiveThread = threading.Thread(target=self._recieve, args=(ssl_sock,))
        self.receiveThread.start()

    def _recieve(self, sock):
        while True:
            # establish connection
            clientSocket, addr = sock.accept()
            print('Got connection from', addr)
            data = clientSocket.recv(4096)
            print('got data: ', data)
            # check if data != '' ?
            data = str(data.decode("utf-8"))

            data = json.loads(data)
            reply_message = self.process_fnc(data)
            reply_message = json.dumps(reply_message)

            if reply_message is not None:
                clientSocket.send(str.encode(reply_message))
            clientSocket.close()


