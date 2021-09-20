import socket
import os
import subprocess
import signal
import threading
import time 
import sys   

sys.path.insert(0, '../')  
from menuInit import menuinit

address = input("Insira o endereço de conexão: ")
garbage, dataAdress = address.split("//") 
_ip, _port = dataAdress.split(":")



class Client:

    def __init__(self,ip,port):

# server_address = (host, port)
# sock.connect(server_address)
# sock.settimeout(None)
# fileobj = sock.makefile('rb', 0)
# print("Connected to {}:{}".format(host, port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("o ip é: " + _ip)
        #print("A porta é: " + _port)
        self.sock.connect((ip,int(port)))
        self.sock.settimeout(None)
        fileobj = self.sock.makefile('rb', 0)
        self.listMensagem = []
        self.off = 0 
        self.menu = None

    def handler(self):
        while True: 

            self.menu.init(self)
            #sendar = input()
            #self.sock.send(sendar.encode())
            # cliente, addr = self.server.accept()
            # self.mensagemThread(cliente)
            # print("\n\033[1;94m[*] Conexao recebida de: {} - {} ID:{} \033[0;0m\n".format(addr[0],addr[1],len(self.listSOCK)))
            # self.listSOCK.append(cliente)
            # self.listHOST.append(addr[0])


    def mensagem(self):
        while True:
            mensagem = self.sock.recv(1024).decode()
            
            if (mensagem == ''):
                self.off = 1
                break
            else:
                print(mensagem)
                self.listMensagem.append(mensagem)

    def mensagemThread(self):
        thread = threading.Thread(target=self.mensagem)
        thread.start()

    def threadHandler(self):
        thread = threading.Thread(target=self.handler)
        thread.start()

def main():
    client = Client(_ip,_port) 
    client.menu = menuinit(_ip,_port) 
    #client.mensagemThread()
    client.threadHandler()

main()