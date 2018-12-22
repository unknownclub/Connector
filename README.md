# Connector
Minify Python Dropper

# NOTE
- For education purpose only.
- Server and WooDoo only work on Linux.
- Client designed for compatible with Windows only.

# Feature
- execute target system commands
- persistence in system
- re-connect every 1 minute
- upload file to target
- download file from target
- multi-client C2 support
- execute payload
- using watchdog timer base for monitor connection between client and server (I call it "WooDoo").

# Command
- cd [path] ****change directory
- upload [filename] ****upload file to target
- download [filename] ****donwload file from target
- list ****display all client
- num_look [target_number] ****select target to control
- num_fetch ****show current target
- payload [payload] ****execute payload
- exit (when control target) ****shutdown target (back to re-connect mode)
- bye ****shutdown server

# How to build

- pip install pyinstaller
- C:\Python27\Scripts\pyinstaller.exe client.py --onefile --noconsole

# How to run
- Server: python -W ignore listener.py
- WooDoo: python woodoo.py (Enter woodoo port)

# Author
- Anuwat Khongchuai (un4ckn0wl3z)

# Contact
- un4ckn0wl3zatgmaildotcom
- https://hacked.un4ckn0wl3z.xyz/

# Full version contributors 
- Rudekitz (OPL Member)
- IOBOYZ (OPL Member)
