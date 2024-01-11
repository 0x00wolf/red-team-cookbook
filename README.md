# **Red-Team Cookbook**
![alt text](https://github.com/0x00wolf/red-team-cookbook/blob/main/imgs/rtcb5.jpeg)
#### **Learn to emulate the programmatic methods high-level adversaries employ to wage cyber-warfare.**

---

### A quick note before you continue:

This project is currently in production, however most of the code is already written. I produced this document for a few reasons: As a means of organizing the cookbook, to be able to track progress as I produce deliverables, to cement the programmatic goals I have set out to accomplish, and the resources I need to realize them. 

Examples are available below representing the style and tone that I intend to take when generating the tutorials.

---

# **Introduction**

---

The Red Team Cookbook (RTCB) is a practical guide to programmatically emulate the methods and techniques that advanced persistent threats (APTs) use at every stage of an attack. From enumeration and initial compromise, to establishing an advanced botnet command infrastructure, the author’s goal is to provide a comprehensive guide for performing techniques used by APTs in a way that readers can understand and emulate them for whatever legitimate application their job may require.

The RTCB focuses on using object-oriented Python and procedural C to provide programmatic solutions for the techniques that malicious actors use to develop malware that targets enterprise organizations. Readers will develop the ability to explain, execute, and automate a wide range of techniques used in cyber-warfare.

The RTCB features a number of tutorials, which are all based on Arch Linux. Readers can use individual components for their learning process, or follow along from start to finish and gain a strong understanding of how APTs conduct sophisticated attacks. The RTCB assumes a solid understanding of programming - including object-oriented programming (OOP), as well as comfortable Linux administration. This is not intended to be a collection of scripts for script kiddies, but a method of learning and developing fully undetectable (FUD) tooling for red-team operators and penetration testers.

The final section of the RTCB is devoted to demonstrating how you can use artificial intelligence (AI) to enhance your red-teaming capabilities.

---

# **Sections Overview:**

The RTCB is broken into six parts: 

---

### **Part 1: Proper Prior Preparation Prevents Pi$$-Poor Performance** 


Part one contains tutorials that explain how to use the Python libraries, programmatic techniques, and tools that are required to build a fully functioning exploit kit and command center from scratch with OOP design patterns. Some example content includes: learning how to code your own domain name system (DNS) server, which readers will later use to create a rogue DNS and exfiltrate data with a DNS tunnel. You will also learn how to become your own root certificate authority and implement your own public key infrastructure (PKI), which you will use to mask traffic to and from your command and control (C2) server via transport layer security (TLS), hiding your communications among regular HTTPS traffic.

In Part 1, readers will also be guided through setting up a virtual lab, with QEMU/KVM and Virt-Manager, to test their exploits and command servers as they progress through the RTCB

---

### **Part 2: Reconnaissance - While Network Programming, Do Bad Stuff** 


Part 2 features a deep dive into different options for network programming using Python, including sockets, SSL, SocketServer, Twisted, Requests, Flask, Scapy, and more. You will manually create servers to receive reverse shells, learn to craft packets layer by layer, and enumerate networks - discovering devices that won’t respond to internet control message protocol (ICMP) requests. You will also learn how to automate encrypting and decrypting data you send across insecure networks with RSA-wrapped-AES and TLS.

An example from Part 2 is included below: Mini-VPN-Chat, a manual implementation of an encrypted two-way secure communication channel to connect devices across insecure networks. Mini-VPN-Chat uses both TLS and a manually AES-encrypted payload (double encryption). Part 3: Exploitation, Obfuscation, & Basic Tooling

---

### **Part 3: Exploitation, Obfuscation, & Basic Tooling**


In Part 3, you will begin to develop standalone versions of different common potentially unwanted programs (PUPs), as well as start developing the skeleton of your exploit kit. Part 3 will introduce a wide variety of tools for surveillance and data exfiltration - learning how to encrypt and mask traffic.

Introduced in Part 3, and central to the exploit kit, is the OOP WorkerRAT and C2 framework (the Mothership Connection). Moving forward, every component will be constructed as a standalone tool, and then used to extend these basic models.

The WorkerRAT employs three object-oriented design patterns covered in Part 1: Worker-Slave, Consumer-Producer, and Factory. The implementation of these patterns enables easy extension and customization. 

---

### **Part 4: Privilege Escalation, Lateral Movement, & Exfiltration**


Part 4 will teach you how to perform privilege escalation, lateral movement, and data exfiltration on your target network. You will master various techniques and tools for these tasks, such as credential theft, keylogging, clipboard hijacking, screen capture, audio and video recording, and DNS tunneling. You will also learn how to secure your data with RSA-wrapped-AES encryption and embed your public key into your RAT. You will then upgrade your WorkerRAT and C2 framework to use these modules to stealthily extract data and compromise the host.

---

### **Part 5: Deny, Destroy, & Alter** 


Part 5 introduces readers to tools that are specifically designed to cause damage on networks and hosts. You will gain a deep understanding of the programmatic elements that are employed in the development of ransomware, as well as learn how to build network stress-test tools in C and Python (DoS). Part 5 concludes with automating and installing XMRminer to hijack hosts and turn them into crypto miners for malicious actors.

The principle of Part 5 is to introduce the programmatic components of these tools to develop a better understanding. The author believes that the only difference between a full disk encryption (FDE) tool and ransomware is the author’s intent when they developed the program.

___

### **Part 6: The Mothership Connection C2 & Advanced Exfiltration**


Part 6 will focus on expanding and improving the C2 framework. At this point, a well-developed exploit kit is in place, and the next step is to improve the delivery, control, and exfiltration mechanisms.

The Mothership Connection is the author’s solution. It features a Flask backend, SQLAlchemy for botnet databasing, DNS servers for data exfiltration and rogue DNS, a homegrown certificate authority, the ability to encrypt and package payloads for drive-by-downloads, and many more features. Front-end development will feature JavaScript and Jinja templates to create a botnet admin console. The ultimate goal of Part 6 is to leave readers with a robust and full-featured command and control server, and the knowledge to go out and build their own unique C2s.

---

### **Part 7:  Using AI to Become Significantly More Dangerous**


Part 7 intends to provide readers with the tools and techniques to incorporate AI into their red-teaming and penetration testing workflow, to significantly boost their productivity and effectiveness. Areas of focus will include strategies for implementing AI into your research process, an introduction to some incredibly useful tools, and an overview of prompt-engineering.

Included in this chapter will also be the final module for the C2 framework, an AI automated MalSpammer, however the code is intentionally broken to prevent misuse. This is a tool intended for red-team engagements that include phishing attacks on corporate emails. If it’s a tool you’d find a legitimate use for at work, by all means find the bug!

___

### **Remember:**


**1) The world is full of fascinating problems to solve.**

**2) Attitude is no substitute for competence**

**3) No problem solved well should need to be solved a second time**

**4) Drugery and boredom are evil**

**5) Freedom is good**

---

# Examples Articles & Code:

**Part 1:** [Homebrewed TLS/SSL & Becoming a Root Certificate Authority](https://github.com/0x00wolf/red-team-cookbook/tree/main/part_1/TLS_root_CA/README.md)

---

# **Part 1: Preparation & Discovery**

---

## **Necessary Python Libraries**


**Standard Library:** https://docs.python.org/3/library/index.html

**1) Sockets**  # https://docs.python.org/3/library/socket.html

**2) SocketServer**  # https://docs.python.org/3/library/socketserver.html

**3) SSL**  # https://docs.python.org/3/library/ssl.html

**4) Thread**  # https://docs.python.org/3/library/threading.html

**5) Concurrent Futures**  # https://docs.python.org/3/library/concurrent.futures.html

**6) Subprocess**  # https://docs.python.org/3/library/subprocess.html

**7) Queue**  # https://docs.python.org/3/library/queue.html 

**8) Multiprocessing**  # https://docs.python.org/3/library/multiprocessing.html

**9) Requests**  # https://requests.readthedocs.io/en/latest/

**10) Nuitka**  # https://nuitka.net/

**11) Flask**  # https://flask.palletsprojects.com/en/3.0.x/

**12) SQLAlchemy**  # https://www.sqlalchemy.org/

**13) SQLite3**  # https://docs.python.org/3/library/sqlite3.html

**14) Pynput**  # https://pynput.readthedocs.io/en/latest/

**15) Pyclipper**  # https://github.com/asweigart/pyperclip

**16) pillow.ScreenGrab**  # https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html

**17) Pycryptodome**  # https://pycryptodome.readthedocs.io/en/latest/

**18) Win32**  # https://github.com/mhammond/pywin32

**19) PSutil**  # https://psutil.readthedocs.io/en/latest/

**20) Scapy**  # https://scapy.net/

**21) Twisted**  # https://twisted.org/

**22) Event Scheduler**  # https://docs.python.org/3/library/sched.html

**23) mmap**  # https://docs.python.org/3/library/mmap.html

**24) urllib.requests**  # https://docs.python.org/3/library/urllib.request.html

**25) abstract base classes**  # https://docs.python.org/3/library/abc.html

---


## **Necessary C Libraries**


**1) Socket programming**  # https://www.ibm.com/docs/en/zos/2.2.0?topic=interface-sample-c-socket-programs

**2) Execv**  # https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_lib_ref/e/execv.html

**3) System**  # https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-system-execute-command

**4) LibCurl**  # https://curl.se/

**5) windows.h**  # https://learn.microsoft.com/en-us/windows/win32/api/winbase/

---

## **Additional Knowledge**


**1) OOP Design Patterns:**  # See WorkerRAT v1
   - Producer-Consumer (threading & queues *Producer phones home)  # https://cs.wellesley.edu/~cs304flask/readings/threads/producer-consumer.html
   - Worker-Slave (threading & subprocesses *Slaves phone home)  # https://docs.gigaspaces.com/solution-hub/master-worker-pattern.html
   - Dynamic-Dispatching
   - Factory (abstract classes)

**2) Concurrent / Asynchronous Programming**
- Threading (Queue, Timer, Event)
- Multiprocessing (Pool, Map, Process)
- Concurrent.Futures (ThreadPoolExecutor)
- Queues
- Pipes

**3) Containerization** 
- NGINX Docker container for HTTP server to go with Flask C2 Server

**4) SQL**
- Botnet DB maintained with SQLAlchemy's ORM (mapped_column)

**5) Full Stack Development**
- C2 Backend (DNS Server, HTTP(s) server, self-signed root CA, authentication, database CRUD, DNS server(s)
    - Flask, SQLAlchemy, Requests, Sockets, SocketServer, etc etc
- Front end: HTML/CSS/JavaScript/Jinja
    - Drive by downloads for OS specific droppers
    - Fingerprinting connections
    - Some sort of defense mechanisms 
    - thoughts: scripting banning IP addresses that send packets that break from baseline expected bot or DBD patterns

**6) OPENSSL - Become Your Own Certificate Authority**

**7) CURL - Advanced usage https://curl.se**

**8) HTTP Headers**  # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers  https://datatracker.ietf.org/doc/html/rfc1945

**9) Building your own DNS Server (DNS Headers)**  # https://implement-dns.wizardzines.com/  https://www.statdns.com/rfc/

**10) Threading vs Multi-Processing, when to choose one or the other**

**11) Docker & Containerization  # just to get some practice**

**12) NGINX in Docker Container (HTTP server for Flask)**

**13) Snort & IPtables-nft**

**14) QEMU/KVM + Virt-Manager (Lab Sandbox)**

**15) IPset scripting**

**16) Homebrewed TLS & Becoming Your Own Root CA**

---

# **Part 2: Reconnaissance, aka While Network-Programming, Do Bad Stuff**

**MITRE / CKC:** Reconnaissance > Resource Development

Tasting notes:

>All Your Base Are Belong To Us:**

-Cats

---

1) Scapy: A Python module that allows you to manipulate network packets and perform various network attacks.
2) Arp Scan: A technique that uses the Address Resolution Protocol (ARP) to discover the IP and MAC addresses of devices on a local network.
3) ICMP Scan: A technique that uses the Internet Control Message Protocol (ICMP) to ping devices on a network and check their availability.
4) Port Scan: A technique that scans the ports of a target device and identifies the services running on them.
5) OS Fingerprinting: A technique that analyzes the network packets of a target device and determines its operating system and version.
6) Service Discovery: A technique that probes the services running on a target device and determines their version and configuration.
7) ARP Poisoning & MITM: A technique that spoofs the ARP cache of devices on a local network and redirects their traffic to an attacker-controlled device, allowing the attacker to intercept and modify the data.
8) Socket Programming & SSL: A technique that allows you to create and manage network connections and encrypt them using the Secure Sockets Layer (SSL) protocol.
9) Threaded Sockets, and ThreadPoolExecutor, and SocketServer: A technique that allows you to handle multiple network connections concurrently using threads.
10) Threaded File Hosting class: A class that allows you to host and serve files over the network using threads to many clients asynchronously.
11) SocketServer File Hosting class: A class that allows you to host and serve files over the network using the SocketServer module.
12) Basic command and control (C2): A server that allows you to manage and control multiple compromised devices remotely by setting commands.
13) ET Phone Home: HTTP callbacks: A technique that allows the compromised devices to communicate with the C2 server using HTTP requests and responses.
14) Reverse Shell(s): A technique that allows you to execute commands on a compromised device remotely, using a shell program that connects back to the C2 server.

---

# **Part 3: Exploitation, Obfuscation & Basic Tooling**


**MITRE / CKC:** Initial Access > Weaponization > Delivery > Exploitation > Installation > Command & Control > Actions on Objectives > Persistence > Privilege Escalation > Execution


## **Attack Vector - All warfare is based on deception**


**1) Droppers  # C + Python**

**2) Worker-Slave OOP RAT skeleton & Simple Command-Server**  # All code client-side code extends RAT, all server-side code extends C2 server

**3) Download and install a new Slave Module**

**4) Download a File and Execute it**

**5) Automated Vulnerability Scanning & Reporting**

**6) Install Python with C dropper to run .py as modules without compiling**

**7) Use UPNP to open a public facing port on a router**

**8) Windows Persistence**
- Window's Service 
- Startup Folder
- Scripts to Run When Browser is Open (if infected, pass)

**9) Linux Persistence**
- Systemd service
- Modifying Bashrc script
- cronjob

---

# Part 3: Building an Arsenal & the Art of Covert Surveillance

**MITRE / CKC:** Credential Access > Discovery > Lateral Movement > Collection 

Tasting notes:

>The enemy does not want you to know anything about them, just as you will jealously guard your own information and plans.

>If you cannot get the knowledge by fair means, it must be gained by subterfuge, including the employment of spies and double agents.

-Sun Tzu

---

1) Stealer:
2) Key Loggers: 
3) Clippers & Crypto Clippers: 
4) Screen Grabbers: P
5) Microphone Recording & Streaming: 
6) Webcam Streaming: 

**1) Stealer:**

A program that steals sensitive information from the target system, such as tokens, passwords, databases, or files. You will use the sqlite3, re, os, system, shutil, win32crypt, and pywin32 modules to access and extract the information.

Features:
   - Browser Passwords & Cookies
   - Windows & Linux Password Files
   - os.path.expanduser() regex easter-egg hunt:
     - regexs in os.path.expanduser()
       - Emails 
       - Phone Numbers
       - 'Password'
       - credit card number
       - Crypto Strings 
     - Routing Tables
     - Mac Tables
   - Device Fingerprinting:
     - Hostname
     - Localnet IPv4 address
     - Inet Connection?
     - if connection IPify API for public IP
     - Subnet Mask  # enumerate local devices and collect information on them (maybe include device fingerprinting))
     - UUID # Generate a UUID for authentication and database for c2 botnet CRUD
     - ETC # definitely forgetting things

**2) Key Loggers**

Programs that record the keystrokes of the user and save them to a file or send them to a C2. You will create eight variations of this PUP, using different methods to capture the keyboard input. Four of them will be in Python, using the pynput, keyboard, pyHook, and ctypes modules. The other four will be in C, using the Windows API, the X11 API, the ncurses library, and the libpcap library.

**3) Clippers & Crypto Clippers**

A program that monitors the clipboard of the user and replaces any copied text with a predefined text, such as a malicious URL or a cryptocurrency address. You will create two variations of this PUP, using different methods to access and manipulate the clipboard. One of them will be in Python, using the pyperclip module. The other one will be in C, using the GetClipboardData and SetClipboardData functions on Windows, or the XGetSelectionOwner and XSetSelectionOwner functions on Linux.

**4) Screen Grabbers**

Programs that capture the screen of the user and save it to a file or send it to a C2. You will create one variation of this PUP in Python, using the PIL and io modules to capture and encode the screen image.

**5) Microphone Recording & Streaming**

Programs that record or stream the microphone of the user to a C2, to spy on the user’s activities and surroundings. You will create one variation of this PUP in Python, using the pyaudio and socket modules to access and stream the microphone data.

**6) Webcam Streaming**

A program that streams the webcam of the user to a C2, to spy on the user’s activities and surroundings. You will create one variation of this PUP in Python, using the cv2, pyaudio, and socket modules to access and stream the webcam data.

---

# **Part 5: DoS - Deny, Destroy, & Alter**

---

Tasting notes:

>Oh, I'm gonna hit you so hard, your children will be born bruised!

-Tank Girl

---

**MITRE:** Impact


**1) DoS Modules**
   - SYN Flood: A program that sends a large number of TCP SYN packets to a target server, without completing the three-way handshake, to exhaust its resources and prevent legitimate connections. You will create one variation of this PUP, using the socket module in Python, or the raw socket API in C, to craft and send the packets.
   - HTTP Flood: A program that sends a large number of HTTP requests to a target web server, to overload its processing capacity and bandwidth. You will create one variation of this PUP, using the requests module in Python, or the libcurl library in C, to generate and send the requests.

**2) Ransomware Module**  # Pathbyter v2.0 Update

- Generates Session keys
- In-memory Encryption
- Multiprocessing pool for Linux
- Spawn processes for Windows (or use Threads)
- Appends encrypted AES keys to the ends of files


**3) XMRrig:**  

   - Scripted Installation and Configuration: A technique that downloads and installs the XMRig software, which is a high-performance Monero (XMR) miner, and configures it to mine for the attacker’s wallet address. You will learn how to use the requests or urllib modules in Python, or the libcurl or WinINet libraries in C, to download the XMRig binary or source code, and the subprocess or os modules in Python, or the system or CreateProcess functions in C, to execute it. You will also learn how to use the json module in Python, or the json-c library in C, to modify the XMRig configuration file with the attacker’s parameters.
   - Monitor and Stop When Task Manager is Open (to hide usage): A technique that monitors the system for the presence of the Task Manager process, and stops the XMRig process if it is detected, to hide the CPU and memory usage. You will learn how to use the psutil module in Python, or the psapi or proc libraries in C, to enumerate and terminate the processes.

---

# Part 4: Encrypting Communications - Using Cryptography as a Weapon

**MITRE / CKC:** Reconnaissance > Resource Development > Defense Evasion > Collection > Command and Control > Exfiltration

Tasting notes:

>'536868682E204265207665777920766577792071756965742C2049276D2068756E74696E672077616262697473'

-EF

```
input_string = '53 68 68 68 2E 20 42 65 20 76 65 77 79 20 76 65 77 79 20 71 75 69 65 74 2C 20 49 27 6D 20 68 75 6E 74 69 6E 67 20 77 61 62 62 69 74 73'
output_string = ''.join([chr(int(x, 16)) for x in input_string.split()])
print(output_string)
```

---

Techniques that allows the RAT and the C2 server to communicate securely and covertly:

1) Implement Base64 for binary data transfers: A technique that encodes the binary data into ASCII characters, using the Base64 algorithm, to avoid transmission errors and bypass some filters.
2) Implement RSA Wrapped AES for communications: A technique that encrypts the communication between the RAT and the C2 server, using a hybrid encryption scheme that combines the RSA and AES algorithms. 
3) Become Your Own Root CA & Implement TLS Connections: A technique that allows you to create your own root certificate authority (CA) and issue certificates for the RAT and the C2 server, to establish secure TLS connections between compromised devices and your C2. 
4) Public Key Encryption: A technique that encrypts the communication between the PUP and the C2, using a pair of keys: a public key and a private key. The public key is known to both parties, and can be used to encrypt the data. The private key is known only to the receiver, and can be used to decrypt the data. This way, only the intended receiver can read the data, even if it is intercepted by a third party. You will learn how to hardcode the attacker’s public key into the WorkerRAT, and use the cryptography module to encrypt the data before sending it to the C2. You will also learn how to use the ssl module to encrypt the data again at the transport layer, using the Secure Sockets Layer (SSL) protocol. 
5) Mini-VPN-Chat, manually implement TLS on top of RSA-Wrapped-AES payloads creating a chat client, in preparation for the upcoming Command & Control chapter.

**5) Update C2 & RAT to use HTTPS Callbacks via SSL**

**6) Modifying Certificate Chains on Windows & Linux**

**7) Hiding Traffic in the Clear - if HTTPS traffic, communicate to mothership**

**8) Exploring Options for Encrypting Reverse shells with SSL (ex: ncat or manually with SSL)**

**9) DNS Tunneling:** A technique that uses the Domain Name System (DNS) protocol to send and receive data covertly, by encoding the data in the DNS queries and responses. This way, the data can bypass the firewall and other network security measures, as DNS is usually allowed and trusted. You will learn how to use the dnspython module to create and parse the DNS messages, and use the socket module to send and receive them over the network. 


# **Part 6: Advanced Command & Control aka The Mothership Connection**

---

## **Command Control**


**Mitre / CKC:** Actions on Objectives > Collection > C&C > Exploitation

Tasting notes:

>**WE ARE THE BORG. YOU WILL BE ASSIMILATED. YOUR UNIQUENESS WILL BE ADDED TO OUR COLLECTIVE. RESISTANCE IS FUTILE.**

-The Collective

---

**1) Routes for OS Specific Malware hosting**

**2) Command Center - Issue commands** / class WorkerRAT.call_parents() = update = self.phone_home: int = {change_frequency_of_callbacks}

**3) SQLAlchemy Bot DB**

**4) DNS Server for DNS Tunnelling**

**5) DNS Server for Rogue DNS**

**6) Certificate Authority (forking C2)**

**7) Drive By Downloads for droppers (OS Specific)**

**8) MalSpammer with GPT scripted phishing emails**

**9) Flask with NGINX HTTP server in Docker container - backend web-server** 

**10) Dynamic JavaScript front-end with command center**

**11) Arch Linux Server OS**

**12) Server Hardening (SNORT, IPtables-NFT, Implement Authentication logic to prevent abuse of botnet communication channels)**

**13) Crypting payloads (AV Evasion)**

___
