import socket
from IPy import IP

def scan(target):
    converted_ip = checkIP(target)
    print("\n","Scanning Targets...", str(target))
    for port in range(1, 85):
        scanPort(converted_ip, port)

def checkIP(ip):
    try:
        IP(ip)
        return(ip)
    except ValueError:
        #permet une recherche par nom de domaine
        return socket.gethostbyname(ip)

def get_banner(s):
    return s.recv(1024)


def scanPort(ip, port):
    try:
        s = socket.socket()
        #Empêcher lenteur
        s.settimeout(0.5)
        s.connect((ip, port))
        try:
            banner = get_banner(s)
            print("[+] Open Port", str(port),":",str(banner.decode().strip('\n')))
        except:
            print("[+] Open Port", str(port))
    except:
        pass

#On détecte si le programme est importé, dans ce cas ce n'est pas importé
if __name__ == "__main__":
    targets = input("Target/s: ")

    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))
    else:
        scan(targets)

