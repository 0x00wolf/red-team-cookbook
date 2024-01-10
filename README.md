# **Red-Team Cookbook**

---

### **Learn to emulate the programmatic methods high-level adversaries employ to wage cyber-warfare.**

---

## **Introduction**

---

The Red Team Cookbook (RTCB) is a guide to programmatically emulate the methods and techniques APTs employ at every stage of an attack. From enumeration & initial compromise, to establishing an advanced botnet command infrastructure, the author's goal is to amalgamate a comprehensive guide for performing techniques used by APTs in such a way that readers will be able to understand and emulate them in whatever legitimate application their job may require.

The RTCB will focus on using object oriented Python and procedural C to provide programmatic solutions for the techniques malicious actors use to develope malware intended to target enterprise organizations. Readers will develop the ability to explain, execute, and automate a comprehensive array of techniques utilized in cyber-warfare. 

RTCB features a number of tutorials, which are all Arch Linux centric. Readers can use individual components for their learning process, or follow along from cover to cover and be left with a strong comprehension of how APTs do bad things in a sophisticated manner. The RTCB assumes a solid understanding of programming - including OOP, as well as comfortable Linux administration. This is not intended to be a stockpile for script kiddies, but a method of learning and developing FUD tooling for red-team operators and penetration testers.

Finally, RTCB's final section is devoted to demonstrating how you can use AI to kick your Red-Teaming into hyperdrive.

---

## **Format**

The RTCB is broken into six parts: 

---

#### **Part 1: Preparation & Discovery** 


Part one contains tutorials explaining how to use the Python libraries, programmatic techniques, and tools that will be required to build a fully functioning exploit kit and Command Center from the sockets up with OOP design patterns. Some example content: Learning how to code your own DNS server, which readers will later use to create a Rogue DNS, and exfiltrate data with a DNS Tunel. You'll also learn how to become your own root Certificate Auhtority and implement your own PKI, which you'll use to mask traffic to-and-from your C2 via TLS, hiding your communications among regular HTTPS traffic. 

In Part 1 readers will also be guided through setting up a virtual-lab to test their exploits and command servers as they progress through the RTCB.

---

#### **Part 2: Reconnaissance - While Network Programming, Do Bad Stuff** 


Part 2 features a deep dive into dfferent options for network programming using Python, including Sockets, SSL, SocketsServer, Twisted, Requests, Flask, Scapy and more. You will manually create servers to receive Reverse Shells, learn to craft packets layer by layer, and enumerate networks - discovering devices that won't respond to ICMP requests. You will also learn how to automate encrypting and decrypting data you send across insecure networks with RSA-Wrapped-AES and TLS.

**Example from Part 2 included below:** Mini-VPN-Chat, a manual implementation of an encrypted two way secure communication channel to connect devices across insecure networks. MiniVPN-Chat uses both TLS and an manually AES encrypted payload (double double). 

---

#### **Part 3: Exploitation, Obfuscation, & Basic Tooling**


In Part 3 you will begin to develop standalone versions different common PUPs (Potentially Unwanted Programs), as well as start developing the skeleton of your exploit kit. Part 3 will introduce a wide variety of tools for surveillance and data exfiltration - learning how to encrypt & mask traffic. 

Introduce in Part 3, and central to the exploit kit, is the OOP WorkerRAT and C2 framework (the Mothership Connection). Moving forward,, every component will be constructed as a standalone tool, and then used to extend these basic models. 

The WorkerRAT employs three object-oriented design patterns covered in Part 1: Worker-Slave, Consumer-Producer, and Factory. The implmentation of these patterns enables easy extension and customization of the WorkerRAT. 

RTCB readers will begin by building simple and flexible C2 Servers, each accomplishing a singular functions (multithreaded file hosting for droppers, a command issuer, etc). In Part 5 the C2 servers will fork, and become a signifcantly more complex singular entity. 

---

#### **Part 4: Privilege Escalation, Lateral Movement, & Exfiltration**



---

#### **Part 5: Deny, Destroy, Alter** 


Part 4 introduces readers to tooling specifically designed to cause damage on networks and hosts. RTCB readers will gain a deep understanding of the programmatic elements employed in the development of ransomware, as well as learn how to build network stress-test tooling in C and Python (DoS). Part 4 concludes with automating and installing XMRminer to hijack hosts and turn them into crypter miners for malicious actors.

The principal of Part 4 is to introduce the programmatic components of these tools to develop a better understanding. I believe that the only difference between a FDE tool and ransomware was the author's intent when they developed the program.

___

#### **Part 6: Command & Control / Advanced Exfiltration**


Part 5 will focus on expanding and improving the C2 Framework. At this point a well developed exploit kit is in place, and the next step is improving the delivery, control, & exfiltration mechanisms.

The Mothership Connection is the author's solution. Featuring a Flask backend, SQLAlchemy for botnet databasing, DNS servers for data exfiltration and Rogue DNS, a home grown certificate authority, the ability to crypt and package payloads for drive-by-downloads,and many more features. Front-end development will feature JavaScript and Jinja templates to create a Botnet admin console. The ultimate goal of Part 5 is to leave readers with a robust and full featured Command & Control server, and the knowlege to go out and build there own unique C2s.nto a fully fledged Flask server using an NGINX HTTP server running in a Docker container, featuring drive-by-downloads, Rogue DNS, DNS Tunelling, and SQLAlchemy to maintain a SQLite3 botnet database as well as log exfiltrated data from clients. 

---

#### **Part 7:  Using AI to Become Significantly More Dangerous**


Part 6 intends to provide RTCB readers with the tools and techniques to incorporate AI into their red-teaming and penetration testing workflow, to significantly boost their productivity and in turn effectiveness. Areas of focus will include strategies for implementing AI into your research process, an introduction to some incredibly useful tools, & an overview of prompt-engineering.

Included in this chapter will also be the final module for the C2 Framework, an AI automated MalSpammer, however the code is intentionally broken to prevent misuse. This is a tool intended for Red-Team engagements that include phishing attacks on corporate emails. If it's a tool you'd find a legitimate use for at work, by all means find the bug!

___

#### **Remember:**


**1) The world is full of fascinating problems to solve.**

**2) Attitude is no substitute for competence**

**3) No problem solved well should need to be solved a second time**

**4) Drugery and boredom are evil**

**5) Freedom is good**

---

# **Part 1: Preparation & Discovery**

---

### **Necessary Python Libraries**


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


### **Necessary C Libraries**


**1) Socket programming**  # https://www.ibm.com/docs/en/zos/2.2.0?topic=interface-sample-c-socket-programs

**2) Execv**  # https://www.qnx.com/developers/docs/6.5.0SP1.update/com.qnx.doc.neutrino_lib_ref/e/execv.html

**3) System**  # https://www.ibm.com/docs/en/zos/2.1.0?topic=functions-system-execute-command

**4) LibCurl**  # https://curl.se/

**5) windows.h**  # https://learn.microsoft.com/en-us/windows/win32/api/winbase/

---

### **Additional Knowledge**


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

---

# **Part 2: Reconnaissance - While Network-Programming, Do Bad Stuff**

---

### **Discovery - All Your Base Are Belong To Us:**


**1) Scapy**

**2) Arp Scan  # In case set to not be discoverable by network devices**

**3) ICMP Scan # If host already discovered do not ping**

**4) Port Scan Discovered Devices  # TCP Half Open common ports**

**5) ARP Poisoning & MITM**

---

# **Part 3: Exploitation, Obfuscation & Basic Tooling**


**MITRE / CKC:** Initial Access > Weaponization > Delivery > Exploitation > Installation > Command & Control > Actions on Objectives > Persistence > Privilege Escalation > Execution


## **Attack Vector - All warfare is based on deception**


**1) Droppers  # C + Python**

**2) Worker-Slave OOP RAT skeleton & Simple Command-Server**  # All code client-side code extends RAT, all server-side code extends C2 server

**3) Download and install a new Slave Module**

**4) Download a File and Execute it**

**5) Automated Vulnerability Scanning & Reporting**

**6) Bonus: Install Python with C dropper to run .py as modules without compiling**

**7) Bonus: Use UPNP to open a public facing port on a router**

**8) Windows Persistence**
- Window's Service 
- Startup Folder
- Scripts to Run When Browser is Open (if infected, pass)

**9) Linux Persistence**
- Systemd service
- Modifying Bashrc script
- cronjob

---


## **Encrypting Communication** 

**MITRE / CKC:** Defense Evasion -> Command & Control -> Exfiltration
>'536868682E204265207665777920766577792071756965742C2049276D2068756E74696E672077616262697473'


Tasting notes:
```
input_string = '53 68 68 68 2E 20 42 65 20 76 65 77 79 20 76 65 77 79 20 71 75 69 65 74 2C 20 49 27 6D 20 68 75 6E 74 69 6E 67 20 77 61 62 62 69 74 73'
output_string = ''.join([chr(int(x, 16)) for x in input_string.split()])
print(output_string)
```


**1) Implement Base64 for binary data transfers**

**2) Implement RSA Wrapped AES for communications**

**3) Become Your Own Root CA & Implement TLS Connections**

**4) Update C2 & RAT to use HTTPS Callbacks via SSL**

**5) Modifying Certificate Chains on Windows & Linux**

**6) Hiding Traffic in the Clear - if HTTPS traffic, communicate to mothership**

**7) Explore Options for Encrypting Reverse shells with SSL (ex: ncat or manually with SSL)**

---

# **Part 4: Privilege Escalation, Lateral Movement, & Exfiltration**

**MITRE / CKC:** Credential Access > Discovery > Lateral Movement > Collection Reconnaisscance

##  **Spy-craft - Data Exfiltration:**

Tasting notes:

>The enemy does not want you to know anything about them, just as you will jealously guard your own information and plans.

>If you cannot get the knowledge by fair means, it must be gained by subterfuge, including the employment of spies and double agents.


**1) Stealer:**
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
   - Python: PynPut
   - C Variations: 
     - set Windows Hook
     - async key state loop

**3) Clippers & Crypto Clippers**

**4) Screen Grabbers**

**5) Microphone Recording & Streaming**

**6) Webcam Streaming**

**7) RSA-Wrapped-AES**
   - Hardcode Attacker Public Key into RAT

**8) Update WorkerRAT to encrypt all data with RSA wrapped AES before relaying to mothership**

**9) DNS Tunnelling (DNS Headers module for WorkerRAT phoning home)**

---

# **Part 5: DoS - Deny, Destroy, & Alter**

---

## **Blowing Stuff Up & Mining Crypto For Fun and Profit** 

**MITRE:** Impact


**1) DoS Modules**


**2) Ransomware Module**  # Pathbyter v2.0 Update

- Generates Session keys
- In-memory Encryption
- Multiprocessing pool for Linux
- Spawn processes for Windows (or use Threads)
- Appends encrypted AES keys to the ends of files


**3) XMRrig:**  
- Scripted Installation and Configuration (maybe monitor and stop when task manager is open to hide usage)

---

# **Part 6: Advanced Command & Control aka The Mothership Connection**

---

## **Command Control**


**Mitre / CKC:** Actions on Objectives > Collection > C&C > Exploitation

Tasting notes:
>**WE ARE THE BORG. YOU WILL BE ASSIMILATED. YOUR UNIQUENESS WILL BE ADDED TO OUR COLLECTIVE. RESISTANCE IS FUTILE.**


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
