import pprint
import socket
import ssl

# To use automatic context:
# context = ssl.create_default_context()

# For botnet
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("rootCA.crt")

conn = context.wrap_socket(socket.socket(socket.AF_INET),
                           server_hostname="localhost")
conn.connect(("127.0.0.1", 12345))

cert = conn.getpeercert()
pprint.pprint(cert)
conn.sendall(b"HEAD / HTTP/1.0\r\nHost: poop\r\n\r\n")
pprint.pprint(conn.recv(1024).split(b"\r\n"))
