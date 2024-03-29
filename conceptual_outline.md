# **Areas of Focus:**

RTCBb posts will focus on 6 areas of focus: 

---

### **1) Preparation**

Python libraries, programmatic techniques, and tools that I'll use to build a fully functioning exploit kit and command center from scratch with OOP design patterns

---

### **2) Reconnaissance** 

In this section I will conduct a deep dive into the different options for network programming using Python, including sockets, SSL, SocketServer, Scapy, Twisted, Requests, Flask, and more. I'm going to produce posts on how to use Scapy to craft and send various network packets and perform different network attacks, such as ARP scanning, ICMP scanning, port scanning, OS fingerprinting, service discovery, ARP poisoning, and man-in-the-middle (MITM). Furthermore, how to use socket programming to create network connections between remote devices and a C2 server.

---

## **3) Arsenal**

### 3a) Potentiall Unwanted Programs (PUPs)

The Arsenal is dedicated to building an arsenal of red-teaming tools, or potentially unwanted programs (PUPs). PUPs will be featured in C and Python, and will represent a variety of methods for accomplishing the programmatic function of each on both Windows & Linux.

### 3b) Destroy, Alter, Deny, & Mine

This section focuses on tools that are specifically designed to cause damage on networks and hosts. I believe that the only difference between a full disk encryption (FDE) tool and ransomware is its creator's intent when they developed the program. So generally speaking, don't do bad things. 

### 3c) Remote Access Tool

This section will focus on developing an OOP WorkerRAT. The WorkerRAT employs a few object-oriented design patterns to enable easy extension and customization.

---

### **4) Encryption & Covert Communications**


This section will focus on encrypting communications like an APT. I will explore manually securing data with RSA-wrapped-AES encryption, embedding a public key into the RAT. And add an additional layer of encryption by homebrewing TLS to become a root Certificate Authority. I'm also going to develop the code for a server side DNS capable of extracting information from networks stealthily via a DNS Tunnel. 

___

### **5) Advanced Command & Control**


Blog posts in this section will focus on a larger C2 project, using a Flask backend with NGINX HTTP server in a Docker Container, implementing SQLAlchemy ORM for botnet databasing, implementing a DNS server for Rogue DNS & tunneling, encrypt & package payloads for drive-by-downloads, and many more features. Front-end development will feature JavaScript and Jinja templates to create a botnet admin console.

---

### **6)  Using AI to Become Significantly More Dangerous**


I use AI everyday in my workflow. I consider GPT my proof reader, super Google, and coding co-pilot. I intend of developing posts regarding the tools and techniques so that they can incorporate AI into their red-teaming and penetration testing workflow, to significantly boost their productivity and effectiveness. Areas of focus will include strategies for implementing AI into your research process, how to obtain the best results, an introduction to some  useful tools, and an overview of prompt-engineering.

___

### **Remember:**


**1) The world is full of fascinating problems to solve.**

**2) Attitude is no substitute for competence**

**3) No problem solved well should need to be solved a second time**

**4) Drugery and boredom are evil**

**5) Freedom is good**

---

# **Blog/Project Outline:**

---

# **1) Preparation**

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

**17) **Payloads All Things:** https://github.com/swisskyrepo/PayloadsAllTheThings

---

# **2) Reconnaissance**

**MITRE / CKC:** Reconnaissance > Resource Development

Tasting notes:

>All Your Base Are Belong To Us:**

- Cats

---

## **While Network-Programming, Do Bad Stuff**

**1) Scapy** 

   - A Python module that allows you to manipulate network packets and perform various network attacks.

**2) Arp Scaning** 

   - A technique that uses the Address Resolution Protocol (ARP) to discover the IP and MAC addresses of devices on a local network.

**3) ICMP Scanning** 

   - A technique that uses the Internet Control Message Protocol (ICMP) to ping devices on a network and check their availability.

**4) Port Scan** 

   - A technique that scans the ports of a target device and identifies the services running on them.

**5) OS Fingerprinting**: 

   - A technique that analyzes the network packets of a target device and determines its operating system and version.

**6) Service Discovery**: 
   
   - A technique that probes the services running on a target device and determines their version and configuration.

**7) ARP Poisoning & MITM**: 
   
   - A technique that spoofs the ARP cache of devices on a local network and redirects their traffic to an attacker-controlled device, allowing the attacker to intercept and modify the data.

**8) Socket Programming & SSL** 

   - A technique that allows you to create and manage network connections and encrypt them using the Secure Sockets Layer (SSL) protocol.

**9) Threaded Sockets, and ThreadPoolExecutor, and SocketServer**:

   - A technique that allows you to handle multiple network connections concurrently using threads.

**10) Basic command and control (C2)**:

   - A server that allows you to manage and control multiple compromised devices remotely by setting commands.

**13) HTTP callbacks**:

   - A technique that allows the compromised devices to communicate with the C2 server using HTTP requests and responses.

---

# **3) Arsenal**

Tasting note:

>Your rifle is only a tool. It is a hard heart that kills. 

-Gunnery Sergeant Hartman

---

**MITRE / CKC:** Initial Access > Weaponization > Delivery > Exploitation > Installation > Command & Control > Actions on Objectives > Persistence > Privilege Escalation > Execution > Credential Access > Discovery > Lateral Movement > Collection 

---

## **3a) Potentially Unwanted Programs (PUPs)**

**1) Droppers**
     
**1) Stealers:**
   - Programs that steals sensitive information from the target system, such as tokens, passwords, databases, or files. 

**2) Key Loggers**
   - Programs that record the keystrokes of the user and save them to a file or send them to a C2.

**3) Clippers**
   - Programs that monitors the clipboard of the user and replaces any copied text with a predefined text, such as a malicious URL or a cryptocurrency address.

**4) Screen Grabbers**
   - Programs that capture the screen of the user and save it to a file or send it to a C2. 

**5) Microphone Recording & Streaming**
   - Programs that record or stream the microphone of the user to a C2, to spy on the user’s activities and surroundings. 

**6) Webcam Streaming**
   - Programs that streams the webcam of the user to a C2, to spy on the user’s activities and surroundings.

**7) Reverse Shell(s)**
   - A technique that allows you to execute commands on a compromised device remotely, using a shell program that connects back to the C2 server.
everse Shells
 
---

## **3b) Remote Access Tool**

Tasting notes:

>The enemy does not want you to know anything about them, just as you will jealously guard your own information and plans.

>If you cannot get the knowledge by fair means, it must be gained by subterfuge, including the employment of spies and double agents.

- Sun Tzu

**1) Worker-Slave OOP RAT Skeleton**

**2) Simple Command-Server**  # All code client-side code extends RAT, all server-side code extends C2 server

**3) Download a File and Execute it**

**4) Download and install a new Slave Module**
**5) Automated Vulnerability Scanning & Reporting**

**6) Install Python with C dropper to run .py as modules without compiling**

**7) Use UPNP to open a public facing port on a router**

**8) Windows Persistence 3 Ways**

**8) Linux Persistence 3 Ways**

---

## **3c) Deny, Destroy, Alter, & Mine**


Tasting notes:

>Oh, I'm gonna hit you so hard, your children will be born bruised!

-Tank Girl

---

**MITRE:** Impact


**1) DoS Modules**

**2) Ransomware Module**  
- Generates Session keys
- In-memory Encryption
- Multiprocessing pool for Linux
- Spawn processes for Windows (or use Threads)
- Appends encrypted AES keys to the ends of files


**3) XMRrig:**  

---

# 4) Encryption and Covert Communications

**MITRE / CKC:** Reconnaissance > Resource Development > Defense Evasion > Collection > Command and Control > Exfiltration

Tasting notes:

>'536868682E204265207665777920766577792071756965742C2049276D2068756E74696E672077616262697473'

-EF


---

**1) Base64 for binary data transfers:**

**2) RSA Wrapped AES for communications:** 

**3) Become Your Own Root CA & Implement Homebrewed TLS Connections**

**4) Hardcoded Public Key Encryption**

**6) Mini-VPN-Chat**

**7) Update C2 & RAT to use HTTPS Callbacks via SSL**

**8) Modifying Certificate Chains on Windows & Linux**

**9) Hiding Traffic in the Clear - if HTTPS traffic, communicate to mothership**

**10) Exploring Options for Encrypting Reverse shells with SSL (ex: ncat or manually with SSL)**

**11) DNS Tunneling:** 

---

# **4) Advanced Command & Control**

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
