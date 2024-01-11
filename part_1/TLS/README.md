# **Home Brewed TLS & Becoming Your Own Root CA**

To create a secure communication channel between a server and a client, you can use the ssl module in Python. The ssl module provides a wrapper for the socket module, which allows you to use SSL/TLS encryption for your network connections. SSL/TLS is a protocol that ensures the confidentiality, integrity, and authentication of the data exchanged between two parties.

In this article, we will show you how to become your own Root Certificate Authority, and create a simple SSL server and client using the ssl module. The server will listen on port 12345 and accept connections from clients that have a trusted root certificate. The client will connect to the server and send a HTTP request, and then receive a response from the server.

## Creating an SSL Server

To create an SSL server, you need to have a certificate and a private key for your domain. The certificate is a file that contains the public key and the identity of your domain, and it is signed by a certificate authority (CA) that is trusted by the clients. The private key is a file that contains the secret key that corresponds to the public key, and it is used to encrypt and decrypt the data.

## Creating a Root CA

To create a root certificate authority (CA) and generate certificates for your servers, you can use the openssl command-line tool. A root CA is a trusted entity that can issue certificates for other domains or servers. You only need to create a root CA once, and then you can use it to sign certificates for any number of servers.

First, you need to create a root key, which is the private key that will be used to sign the certificate requests. This key should be kept in a safe place, as anyone who has access to it can create certificates on your behalf. To create a root key, run the following command:

```bash
openssl genrsa -des3 -out rootCA.pem 4096
```

This will create a 4096-bit RSA key with DES3 encryption and save it to a file named rootCA.pem. If you want a non-password-protected key, you can omit the -des3 option.

Next, you need to create a root certificate, which is the public key that will be distributed to all the computers that have to trust your CA. To create a root certificate, run the following command:

```bash
openssl req -x509 -new -nodes -key rootCA.pem -sha256 -days 1024 -out rootCA.crt
```

This will create a self-signed X.509 certificate with SHA256 encryption and a validity of 1024 days. You will be prompted to enter some information about your CA, such as the country, state, organization, and common name. The common name is the most important field, as it should match the domain name or IP address of your CA.
Creating a Certificate for a Server

After creating a root CA, you can use it to generate certificates for your servers or appliances. Each server needs its own certificate key and certificate signing request (CSR). The certificate key is the private key that will be used to encrypt the communication with the server. The CSR is a file that contains the details for the certificate you want to generate, such as the domain name or IP address of the server. The CSR will be processed by the root CA to generate the certificate.

## To create a certificate key, run the following command:

```bash
openssl genrsa -out mydomain.com.pem 2048
```

This will create a 2048-bit RSA key and save it to a file named `mydomain.com.pem`. You can replace `mydomain.com` with the actual domain name or IP address of your server.

## To create a CSR, you can use one of the following methods:

## **Method A: Interactive**

This method will ask you some questions about the certificate you want to generate, such as the country, state, organization, and common name. **The common name is the most important field, as it should match the domain name or IP address of your server.** To create a CSR interactively, run the following command:

```bash
openssl req -new -key mydomain.com.pem -out mydomain.com.csr
```

This will create a CSR using the certificate key you created earlier and save it to a file named `mydomain.com.csr`.

## **Method B: One-liner**

This method will generate the same CSR as Method A, but without asking any questions. Instead, you can specify the information as arguments to the command. This method is suitable for automation. To create a CSR using a one-liner, run the following command:

```bash
openssl req -new -sha256 -key mydomain.com.pem -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=mydomain.com" -out mydomain.com.csr
# Thanks to Lorenzo F for this snippet of wisdom: https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309
```

This will create a CSR with SHA256 encryption using the certificate key you created earlier and the subject information you provided. The subject information should include the country ©, state (ST), organization (O), and common name (CN) of your server. You can replace the values with your own.

For example, to set up a certificate for localhost, use: `O = localhost`, and `CN = localhost`. 

If you need to pass additional configuration options, such as alternative names for your server, you can use the -config parameter. For example, to add DNS alternative names, you can run the following command:

```bash
openssl req -new -sha256 \
    -key mydomain.com.pem \
    -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=mydomain.com" \
    -reqexts SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf "\n[SAN]\nsubjectAltName=DNS:mydomain.com,DNS:www.mydomain.com")) \
    -out mydomain.com.csr
```

This will create a CSR with the same subject information as before, but also with the SAN extension that specifies the alternative names for your server. You can add as many DNS names as you want, separated by commas.

## Verifying the CSR

To verify the content of the CSR, you can run the following command:

```bash
openssl req -in mydomain.com.csr -noout -text
```

This will display the information contained in the CSR, such as the subject, the public key, and the extensions. You can check if the information matches your expectations before proceeding to the next step.
Generating the Certificate

Once you have a CSR, you can use it to generate a certificate for your server. To do this, you need to use the root CA key and certificate you created earlier. To generate a certificate using the CSR, run the following command:

```bash
openssl x509 -req -in mydomain.com.csr -CA rootCA.crt -CAkey rootCA.pem -CAcreateserial -out mydomain.com.crt -days 500 -sha256
```

This will create a X.509 certificate with SHA256 encryption and a validity of 500 days. The certificate will be signed by the root CA using its key and certificate. The certificate will be saved to a file named mydomain.com.crt. You will also need to enter the password for the root CA key, if you used the -des3 option when creating it.
Verifying the Certificate

To verify the content of the certificate, you can run the following command:

```bash
openssl x509 -in mydomain.com.crt -text -noout
```

This will display the information contained in the certificate, such as the issuer, the subject, the public key, the signature, and the extensions. You can check if the information matches your expectations and if the certificate is valid.
Summary

#### To review, here are the steps to create a root CA and generate certificates for your servers:

1) Create a root key using openssl genrsa.
2) Create a root certificate using openssl req and openssl x509.
3) Create a certificate key for each server using openssl genrsa.
4) Create a CSR for each server using openssl req.
5) Verify the CSR for each server using openssl req.
6) Generate a certificate for each server using openssl x509.
7) Verify the certificate for each server using openssl x509.

That’s all there is to the openssl tool! You can learn more about its features and options from https://www.openssl.org/docs/.

## Creating an SSL Connection to Encrypt Network Communication

The ssl module in Python lets you create and manage secure connections between clients and servers using the SSL/TLS protocol. SSL/TLS is a cryptographic protocol that protects the data transmitted over a network. In this section, we will see how to use the ssl module to connect to a server securely, exchange data, and verify the server’s identity with certificates.

The code below shows how to create an SSL connection with a server on the local machine (127.0.0.1) on port 12345. The code assumes that the server has a certificate signed by a trusted certificate authority (CA), and that the client has the CA’s root certificate in a file named “rootCA.crt”.

```python
import pprint
import socket
import ssl

# To use automatic context:
# context = ssl.create_default_context()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # 1) Create the ssl Context object
context.load_verify_locations("rootCA.crt")`  # 2) Load your self-signed root CA

conn = context.wrap_socket(socket.socket(socket.AF_INET),  # 3) Create a Socket object
                           server_hostname="localhost")
conn.connect(("127.0.0.1", 12345))

cert = conn.getpeercert()  # 5) Fetch the server's Certificate
pprint.pprint(cert)
conn.sendall(b"HEAD / HTTP/1.0\r\nHost: poop\r\n\r\n")  # 6) Send & receive data secured with TLS
pprint.pprint(conn.recv(1024).split(b"\r\n"))
```

**In this code you accomplish the following:**

1) Create an SSL context object, which holds the settings and options for the SSL connection. The parameter ssl.PROTOCOL_TLS_CLIENT means that the context is for a TLS client. This will enable the highest protocol version that both the client and server support, and perform the necessary certificate verification and hostname checking.
2) Load the CA’s root certificate from the file “rootCA.crt” into the context. This will allow the client to check the server’s certificate chain and ensure that it is issued by a trusted CA.
3) Create a socket object using the socket.AF_INET address family (IPv4) and wrap it with the SSL context using the wrap_socket() method. The parameter server_hostname="localhost" specifies the expected hostname of the server, which will be matched against the server’s certificate during the handshake.
4) Connect to the server using the connect() method of the wrapped socket. This will start the SSL handshake, which involves exchanging messages and cryptographic keys between the client and server, and verifying each other’s identities and capabilities.
5) Get the server’s certificate using the getpeercert() method of the wrapped socket. This will return a dictionary with the fields of the certificate, such as the subject, issuer, serial number, and validity period. The pprint module is used to print the dictionary nicely.
6) Send and receive data using the sendall() and recv() methods of the wrapped socket, as if it were a regular socket. The data is automatically encrypted and decrypted by the SSL layer. In this example, the client sends a simple HTTP request for the root path (/) of the server, and prints the response. The data is split by the newline character (\r\n) for readability.

Creating a Server-Side SSL Connection with Python

Now we'll look at how to use the TLS/SSL protocol, and the corresponding ssl module in Python, to create and manage secure connections from the server side. This way, you can ensure that the data exchanged between your server and the clients is protected from eavesdropping and tampering. In this section, we will see how to use the ssl module to create a server-side SSL connection, accept and handle client requests, and verify the client’s identity with certificates.

The code below shows an example of creating a server-side SSL connection on the local machine (127.0.0.1) on port 12345. The code assumes that the server has a certificate and a private key for its domain name (mydomain.com), and that the client has the server’s certificate or the CA’s root certificate to verify the server’s identity. 

```python
import socket
import ssl
from datetime import datetime


def deal_with_client(connstream):
    print(f'[*] client connected @ {datetime.now():%m %d %H %M %S}')
    data = connstream.recv(1024)
    # Empty data means the client is finished with us:
    while data:
        if not do_something(connstream, data):
            # placeholder function
            # when we're finished with client
            break
        data = connstream.recv(1024)


def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # 1) Create the SSL object context
    context.load_cert_chain(certfile="mydomain.com.crt", keyfile="mydomain.com.pem")  # 2) Load the certificates for TLS/SSL
    bindsocket = socket.socket()  # 3)
    bindsocket.bind(('127.0.0.1', 12345))
    bindsocket.listen(5)
    print('[*] waiting for connection...')
    while True:
        newsocket, fromaddr = bindsocket.accept()  # 4) Accept client connections
        connstream = context.wrap_socket(newsocket, server_side=True)  # 5)Wrap the socket in SSL
        try:
            deal_with_client(connstream)  # 6) Deal with the client
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] exiting...')
```

#### **The code does the following:**

1) Create an SSL context object, which holds the settings and options for the SSL connection. The parameter ssl.Purpose.CLIENT_AUTH indicates that the context is for a server that requires client authentication. This will enable the highest protocol version that both the server and client support, and perform the necessary certificate verification and hostname checking.
2) Load the server’s certificate and private key from the files “mydomain.com.crt” and “mydomain.com.pem” into the context. This will allow the server to prove its identity to the client and establish a secure connection.
3) Create a socket object using the socket.AF_INET address family (IPv4) and bind it to the local address and port using the bind() method. Then, listen for incoming connections using the listen() method.
4) Accept a connection from a client using the accept() method of the socket. This will return a new socket object and the client’s address.
5) Wrap the new socket object with the SSL context using the wrap_socket() method. The parameter server_side=True specifies that the socket is used as a server. This will initiate the SSL handshake, which involves exchanging messages and cryptographic keys between the server and client, and verifying each other’s identities and capabilities.
6) Call the deal_with_client() function, which handles the communication with the client. The function uses the recv() and sendall() methods of the wrapped socket to exchange data, as if it were a regular socket. The data is automatically encrypted and decrypted by the SSL layer. The function also prints the time of the connection and checks if the client is finished by looking for empty data. The function calls the do_something() function, which performs some logic on the data and returns a boolean value indicating whether to continue or not. 
7) Finally, close the connection using the shutdown() and close() methods of the wrapped socket. This will terminate the SSL session and release the resources.

That's all we're going to cover, but there is a lot more you can do with the ssl module! You can learn more about its features and options from https://docs.python.org/3/library/ssl.html.
