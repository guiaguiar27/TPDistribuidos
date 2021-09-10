import socket
import threading
import os
import subprocess
import multiprocessing
import queue
import signal
import MySQLdb # para o MySQL
from pyngrok import ngrok
import json

# host = "seu ip" 
# port = 9001

#-------------------------------- API de cadastro do usuario --------------------------------
#INSERT INTO album (quantityCards, quantityStickeredCards) VALUES (0,0);
#SET @last_id_in_album = LAST_INSERT_ID();
#INSERT INTO collector (name, email, password, coins, idAlbum) VALUES ("Arthur Lenda", "arthur@lendario.com", "descontoemmoveis", 0, @last_id_in_album);
#-------------------------------- API de cadastro do usuario --------------------------------


_ip = "127.0.0.1"
_port = 90


con = MySQLdb.connect(host="localhost", user="root", passwd="123root123", db="albumdb")
cursor = con.cursor()
#con.select_db('banco de dados')

class Server:

    def __init__(self,ip,port):
        self.listSOCK = []
        self.listHOST = []
        self.listID = []
        self.hosts = 0
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip,port))
        self.server.listen(5)
        os.system("cls")
        # ngrok.set_auth_token("1xpAWGP6d7gV2rjQNkWUetuLtl3_3h6dZyk7gvYkDCpHWdMY")
        public_url = ngrok.connect(port, "tcp", options={"remote_addr": "{}:{}".format(ip, port)})
        print("Tunnel \"{}\"".format(public_url))
        print("\n\033[1;35m[*] On: {} - {}\033[0;0m\n".format(ip,port))

    def handler(self):
        while True:
            cliente, addr = self.server.accept()
            self.mensagemThread(cliente)
            print("\n\033[1;94m[*] Conexao recebida de: {} - {} ID:{} \033[0;0m\n".format(addr[0],addr[1],len(self.listSOCK)))
            self.listSOCK.append(cliente)
            self.listHOST.append(addr[0])
            #server.comandoSOCK()
            #server.vivoThread(str(len(self.listSOCK) - 1))


    def mensagem(self, cliente):
        while True:
            mensagem = cliente.recv(1024).decode()
            print("a mensagem é: " + mensagem) 
            
            if(mensagem == 'insere'): 
                cursor.execute("SELECT * FROM COLLECTOR")
                teste = cursor.fetchall()
                teste = json.dumps(teste, indent=4)
                index = self.listSOCK.index(cliente)
                #res = [tuple(map(lambda x: x.encode('utf-8'), tup)) for tup in teste]
                server.comandoSOCK(index, teste) 

            elif(mensagem == 'login'):
                print('insira o email: ')
                testeLogin = cliente.recv(1024).decode()
                print('insira a senha: ')
                testeSenha = cliente.recv(1024).decode()
                cursor.execute("SELECT id FROM COLLECTOR WHERE email = %s AND senha %s" % (testeLogin, testeSenha))
                id = cursor.fetchall()
                self.listID.append(id)
                print('o id é: ')
                print(id)
                #teste = 'O id do usuário é '
                index = self.listSOCK.index(cliente)
                server.comandoSOCK(index,teste)


            elif(mensagem == 'printInventario'):  
                user = 'gi' # getUser() usa com listID recebe o usuario #var a = select id from collector where username = 'guilherme'
                cursor.execute("SELECT * FROM INVENTORY_CARDS\
                    JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
                    JOIN COLLECTOR ON  INVENTORY_CARDS.idCard = COLLECTOR.idCollector\
                    WHERE INVENTORY_CARDS.idCollector = '%s'" % (user)) 
                teste = cursor.fetchall()
                teste = json.dumps(teste, indent =4)
                index = self.listSOCK.index(cliente)
                server.comandoSOCK(index,teste)
            
            elif(mensagem == 'printAlbum'):  
                cursor.execute("SELECT * FROM ALBUM\
                    JOIN COLLECTION_CARDS ON COLLECTION_CARDS.idAlbum = ALBUM.id\
                          JOIN COLLECTOR ON ALBUM.ID = COLLECTOR.idAlbum")
                teste = cursor.fetchall() 
                teste = json.dumps(teste, indent =4) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)

            elif(mensagem == 'printLoja'): 
                cursor.execute("") 
                teste = cursor.fetchall() 
                teste = json.dumps(teste, indent =4) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)

            elif(mensagem == 'cadastra'): 
                pass
            #self.sock.send(sendar.encode())
            # if (mensagem == ''):
            #     self.off = 1
            #     break
            # else:
            #     print(mensagem)
            #     self.listMensagem.append(mensagem)

    def mensagemThread(self, cliente):
        thread = threading.Thread(target=self.mensagem, args=(cliente,)) #passo como parametro um ponteiro para a função mensagem, assim a thread irá chamar a função mensagem ao start()
        thread.start()


    def threadHandler(self):
        thread = threading.Thread(target=server.handler)
        thread.start()
    
    def comandoSOCK(self, id, comando):
        print(comando)
        self.listSOCK[int(id)].send(comando.encode())


def main():
    while True:
        try:
            id = input()
            comando = input()
            server.comandoSOCK(id, comando)
        except:
            pass

try:
    server = Server(_ip, _port)
    server.threadHandler()
    main()
except KeyboardInterrupt:
    print('teste')
    subprocess.call(['taskkill', '/F', '/T', '/PID',  str(threading.get_ident())])
    # os.kill(os.getpid(), signal.SIGKILL)
except IndexError:
    main()
except ValueError:
    main()



cursor.close()
con.close()



