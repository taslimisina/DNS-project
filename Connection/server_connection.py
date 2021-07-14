import ssl
import threading
import socket
import json


class ServerConnection:
    def __init__(self, process_fnc, port):
        self.process_fnc = process_fnc

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
        ssl_sock.bind(('', port))

        ssl_sock.listen(5)

        self.receiveThread = threading.Thread(target=self._recieve, args=(ssl_sock,))
        self.receiveThread.start()

    def _recieve(self, sock):
        while True:
            # establish connection
            clientSocket, addr = sock.accept()
            data = sock.recv(4096)
            # check if data != '' ?
            data = str(data.decode("utf-8"))

            data = json.loads(data)
            reply_message = self.process_fnc(data)
            reply_message = json.dumps(reply_message)

            if reply_message is not None:
                clientSocket.send(str.encode(reply_message))
            clientSocket.close()


