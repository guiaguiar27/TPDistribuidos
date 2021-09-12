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
cursor = con.cursor(MySQLdb.cursors.DictCursor)
#for row in cursor:
    #print("* {Name}".format(Name=row['Name']))




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
        #index = self.listSOCK.index(cliente)
        while True:
            mensagem = cliente.recv(1024).decode()
            print("a mensagem é: " + mensagem) 
            
            if(mensagem == 'iniciar'):
                index = self.listSOCK.index(cliente)
                server.comandoSOCK(index, "insira o próximo comando")

            
            elif(mensagem == 'insere'): 
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
                sqlQuery = "SELECT id FROM COLLECTOR WHERE email = %s AND password = %s"
                cursor.execute(sqlQuery,(testeLogin, testeSenha))
                # cursor.execute("SELECT id FROM COLLECTOR WHERE email = %s AND senha %s" % (testeLogin, testeSenha))
                
                id = cursor.fetchall()
                self.listID.append(str(id[0].get('id'))) 
                userID = str(id[0].get('id')) 
                
                print(id)
                teste = json.dumps(id, indent =4)
                #teste = 'O id do usuário é '
                index = self.listSOCK.index(cliente)
                server.comandoSOCK(index, teste) 
                
                qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (testeLogin))
                if(qtdRows > 0):
                    passwordDB = cursor.excute("SELECT password FROM Collector WHERE Collector.id = %s" % (userID))
                    if(testeSenha == testeSenha): 
                        mensagem  = "Login feito com sucesso"
                        server.comandoSOCK(index, mensagem)
                elif(qtdRows == 0):  
                    mensagem = "Usuário não cadastrado"
                    server.comandoSOCK(index, mensagem)



            elif(mensagem == 'printInventario'):  
                user = self.listSOCK.index(cliente)
                sqlQuery = "SELECT * FROM INVENTORY_CARDS\
                    JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
                    JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = COLLECTOR.id\
                    WHERE INVENTORY_CARDS.idCollector = %s"
                cursor.execute(sqlQuery, (user)) 
                teste = cursor.fetchall()
                teste = json.dumps(teste, indent =4)
                server.comandoSOCK(index,teste)
            
            elif(mensagem == 'printAlbum'):
                index = self.listSOCK.index(cliente) 
                user = self.listId[index]
                sqlQuery = "SELECT * FROM Album A JOIN Collection_Cards B ON A.id = B.idAlbum\
                    JOIN Card C ON C.id = B.idCard\
                    JOIN Collector D ON A.id = D.idAlbum\
                    JOIN Collector E ON E.idAlbum = A.id WHERE E.id = %s"
                cursor.execute(sqlQuery, (user))
                teste = cursor.fetchall() 
                teste = json.dumps(teste, indent =4) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)

            elif(mensagem == 'printLoja'): 
                sqlQuery = "SELECT A.price, (SELECT C.name FROM Collector C WHERE A.idCollector = C.id) AS Vendedor,\
                    B.name AS Carta, B.description, B.picture\
                    FROM Store_Cards A JOIN Card B ON A.idCards = B.id"
                cursor.execute(sqlQuery)
                teste = cursor.fetchall() 
                teste = json.dumps(teste, indent =4) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)
                idUser = self.listID[index]
                
                print('o id do usuario é: ' + str(idUser))
                idOferta = cliente.recv(1024).decode()
                    #sqlQuery = "SELECT"
                sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
                cursor.execute(sqlQuery, (idUser))
                consulta = cursor.fetchall()
                qtdCoins = consulta[0].get('coins')
                sqlQuery = "SELECT * FROM Store_Cards WHERE id = %s"
                cursor.execute(sqlQuery, (idOferta))
                consulta2 = cursor.fetchall()
                precoOferta = consulta2[0].get('price')
                if(precoOferta <= qtdCoins):
                    qtdCoins = qtdCoins = precoOferta
                    sqlQuery = "UPDATE Collector SET coins = %s WHERE id = %s"
                    cursor.execute(sqlQuery, (qtdCoins, idUser))
                    sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCard = %s"
                    qtdCards = cursor.execute(sqlQuery, (consulta2[0].get('idCards')))
                    inventoryCardInfo = cursor.fetchAll()
                    if(qtdCards > 0):
                        sqlQuery = "UPDATE Inventory_Cards SET quantity = %s"
                        cursor.execute(sqlQuery, str(inventoryCardInfo[0].get('quantity')+1))
                    else:
                        sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)" #tem que checar se já tem cartas no inventário do usuario desse tipo, se tiver apenas é necessário atualizar a quantidade
                        cursor.execute(sqlQuery, (consulta2[0].get('idCards') ,idUser))

                        #falta adicionar o dinheiro ao usuário que estava vendendo caso o campo idCollector seja != NULL
                    cursor.commit()
                    
                print(consulta[0].get('coins'))
                print(json.dumps(consulta, indent = 4))


            elif(mensagem == 'catalogo'):
                sqlQuery = "SELECT * FROM Card"
                cursor.execute(sqlQuery)
                teste = cursor.fetchall()   
                teste = json.dumps(teste, indent =4) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)
            elif(mensagem == 'cadastrar'):
                print('bora cadastrar')
                #pedir nome
                index = self.listSOCK.index(cliente)
                userName = cliente.recv(1024).decode()
                #pedir email
                userEmail = cliente.recv(1024).decode()
                #pedir senha
                password = cliente.recv(1024).decode()
                #pedir confirmação de senha
                passwordValidation = cliente.recv(1024).decode()
                qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (userEmail))
                if(qtdRows > 0):
                    mensagem = "Email ja cadastrado"
                    server.comandoSOCK(index, mensagem)
                    #return "email ja existente"
                elif(password == passwordValidation):
                    sqlQuery = "INSERT INTO album (quantityCards, quantityStickeredCards) VALUES (0,0);"
                    cursor.execute(sqlQuery)
                                #SET @last_id_in_album = LAST_INSERT_ID();\
                    sqlQuery = "INSERT INTO collector (name, email, password, coins, idAlbum) VALUES (%s, %s, %s, 10, %s);"
                    print(cursor.lastrowid)
                    #sqlQuery = "INSERT INTO Collector (name, email, password, coins) VALUES (%s, %s, %s, 10)"
                    cursor.execute(sqlQuery, (userName, userEmail, password, cursor.lastrowid))
                    con.commit()
                    print('usuario inserido')
                    #cursor.commit()
                else:
                    mensagem = "as senhas não coincidem"
                    server.comandoSOCK(index, mensagem) 

            elif(mensagem == "ColarFigura"):  
                
                # get figure id  
                figure_id = '1'    
                user = self.listSOCK.index(cliente)
                
                # obtem a quantidade de figuras coladas no album
                quantityStickeredFromAlbum = "SELECT quantityStickeredCards JOIN Album ON Album.id = Collector.idAlbum WHERE id = %s" 
                cursor.execute(quantityStickeredFromAlbum, (user))  
                # atualiza 
                sqlQuery = """ UPDATE Album SET quantityStickeredCards = %s JOIN Album ON Album.id = Collector.idAlbum\ 
                WHERE (SELECT idAlbum JOIN Collector ON Album.id = Collector.id  
                WHERE Album.id = Collector.idalbum) = %s """
                # atualiza  
                # inserir  no collection cards  (indicando o id da carta e o id do album )
                cursor.execute(sqlQuery,(quantityStickeredFromAlbum, user))
                # 
                delete = "DELETE FROM tabela WHERE JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
                    JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = %s\
                WHERE INVENTORY_CARDS.idCard = %s" 
                cursor.execute(delete,(user,figure_id))
                                
                
            # elif(mensagem == 'comprar'):
            #     index = self.listSOCK.index(cliente)
            #     idUser = self.listID[index]
            #     ofertas = "SELECT * FROM Store_Cards"
            #     idOferta = cliente.recv(1024).decode()
            #     sqlQuery = "SELECT"
            #     sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
            #     cursor.execute(sqlQuery, (idUser))
            #     consulta = cursor.fetchall()

                
                #pass




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



