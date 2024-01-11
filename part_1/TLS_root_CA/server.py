import socket
import ssl
from datetime import datetime


def deal_with_client(connstream):
    print(f'[*] client connected @ {datetime.now():%m %d %H %M %S}')
    data = connstream.recv(1024)
    # Empty data means the client is finished with us:
    while data:
        if not do_something(connstream, data):
            # we'll assume do something returns false
            # when we're finished with client
            break
        data = connstream.recv(1024)


def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="mydomain.com.crt", keyfile="mydomain.com.pem")
    bindsocket = socket.socket()
    bindsocket.bind(('127.0.0.1', 12345))
    bindsocket.listen(5)
    print('[*] waiting for connection...')
    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] exiting...')
