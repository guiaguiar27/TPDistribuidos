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
import ast

#============================================ criar troca ============================================
# INSERT INTO Exchanges (idCollectorOwner, idCollectorTarget, idCard, idCardReceived) VALUES ('IdDoUsuarioQueCriouATroca', 'IdDoUsuarioQueVaiReceberAOferta', 'IdDoCardASerTrocado', 'idDoCardDesejadoEmTroca')
#============================================ criar troca ============================================


#============================================ Listar trocas criadas e trocas pendentes ============================================
# SELECT B.email AS CollectorOwnerEmail, C.email AS CollectorTargetEmail, D.name AS CardTraded, E.name AS CardReceived  FROM Exchanges A JOIN Collector B ON B.id = A.idCollectorOwner JOIN Collector C ON C.id = A.idCollectorTarget JOIN CARD D ON D.id = A.idCard JOIN CARD E ON E.id = A.idCardReceived WHERE A. idCollectorOwner = 'idUsuarioNoMenu' OR A.idCollectorTarget = 'idUsuarioNoMenu'

#vamos pegar tudo e checar se o id do usuario está no idCollectorOwner ou no idCollectorTarget
    #se estiver no collector owner
        #opção de retirar a proposta de troca
        #Executar a parte de 'troca aceita' tanto para target quanto para oferta, sem a parte dos deletes
        #DELETE FROM Exchange WHERE id = 'idDaProposta Negada'
    #se estiver no collector target
        #opção de aceitar a troca
#============================================ Listar trocas criadas e trocas pendentes ============================================

#============================================ Troca Aceita ============================================

#se target
#SELECT * FROM Inventory_Cards WHERE idCollector = 'idDoUsuario' AND idCard = 'idCardDaOfertaAceita'
    # Se número de linhas > 0
        # UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = 'idDoUsuario' AND idCard = 'idCardDaOfertaAceita'
    # Se número de linhas = 0
        # INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES ('idCardDaOfertaAceita', 1, 'idDoUsuario')
    
#SELECT quantity FROM Inventory_Cards WHERE idCollector = 'idDoUsuario' AND idCard = 'idDaCartaGiven'
    #Se quantity = 1
        # DELETE FROM Inventory_Cards WHERE idCollector = 'idDoUsuario' AND idCard = 'idDaCartaGiven'
    #Se quantity > 1
        # UPDATE Inventory_Cards SET quantity = quantity-1 WHERE idCollector = 'idDoUsuario' AND idCard = 'idDaCartaGiven'


#se criador da oferta
#SELECT id FROM COLLECTOR WHERE email = 'emailOwner'
#pega o id da seleção acima e
#SELECT * FROM Inventory_Cards WHERE idCollector = 'idDoOwner' AND idCard = 'idCardDaRecebida'
    # Se número de linhas > 0
        # UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = 'idDoOwner' AND idCard = 'idCardDaRecebida'
    # Se número de linhas = 0
        # INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES ('idCardDaRecebida', 1, 'idDoOwner')
        
#SELECT quantity FROM Inventory_Cards WHERE idCollector = 'idDoOwner' AND idCard = 'idDaCartaGiven'
    #Se quantity = 1
        # DELETE FROM Inventory_Cards WHERE idCollector = 'idDoOwner' AND idCard = 'idDaCartaGiven'
    #Se quantity > 1
        # UPDATE Inventory_Cards SET quantity = quantity-1 WHERE idCollector = 'idDoOwner' AND idCard = 'idDaCartaGiven'




#Pegar email do collectorOwner
#SELECT A.id FROM Inventory_Cards A JOIN Collector B ON A.idCollector = B.id WHERE A.idCollector = 'idCollectorOwner' AND B.email = 'emailCollectorOwner'
#pego ele e
#SELECT * FROM 

#============================================ Troca Aceita ============================================


#============================================ Ver email dos Usuários ====================================
#Retorna todos os dados mas só mostra para o cliente o email dos jogadores
#SELECT * FROM COLLECTOR
#Quando email de usuario for selecionado vai aparecer a opção "ver album"
#A query abaixo vai exibir as cartas faltantes no album do usuário selecionado pelo email
#SELECT name, description FROM CARD A JOIN Collection_Card B Where B.idAlbum = 'IdDoAlbumArmazenadoNoSelectDeCima' AND A.id != B.idCard

#============================================ Ver email dos Usuários ====================================















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
            print('estou aqui no append')
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
                index = self.listSOCK.index(cliente)
                print("o index é: " + str(index))
                #sqlQuery = "SELECT id FROM COLLECTOR WHERE email = %s AND password = %s"
                #cursor.execute(sqlQuery,(testeLogin, testeSenha))
                # cursor.execute("SELECT id FROM COLLECTOR WHERE email = %s AND senha %s" % (testeLogin, testeSenha))
                print(str(testeLogin))
                print(str(testeSenha))
                
                qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (testeLogin))
                ReturnDB = cursor.fetchall() 

                if(qtdRows > 0):
                    #passwordDB = cursor.excute("SELECT password FROM Collector WHERE Collector.id = %s" % (userID))
                    passFromDb =  ReturnDB[0].get('password')
                    if(testeSenha == passFromDb): 
                        mensagem  = "Login feito com sucesso"
                        server.comandoSOCK(index, mensagem) 
                        #id = cursor.fetchall()
                        self.listID.append(str(ReturnDB[0].get('id')))

                        print('o tamanho da lista é: ' + str(len(self.listID)))
                        user = self.listID[index]
                        print('o usuario é: ' + str(user) )
                        #================================= Checar se a frequencia deve ser mantida e premiar =================================
                        sqlQuery = "SELECT DATE(lastConnection) AS lastConnectionYesterday FROM COLLECTOR WHERE id = %s"
                        cursor.execute(sqlQuery, (user))
                        oldDateResponse = cursor.fetchall()
                        oldLastConnection = oldDateResponse[0].get('lastConnectionYesterday')
                        sqlQuery = 'SELECT DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) AS newLastConnection'
                        cursor.execute(sqlQuery)
                        newDateResponse = cursor.fetchall()
                        newLastConnection = newDateResponse[0].get('newLastConnection')
                        print(str(oldLastConnection) + '     ' + str(newLastConnection))
                        if(oldLastConnection == newLastConnection):
                            sqlQuery = 'UPDATE COLLECTOR SET coins = coins + accessFrequency+2, accessFrequency = accessFrequency+1, lastConnection = %s WHERE id = %s'
                            cursor.execute(sqlQuery, (newLastConnection, user))
                            # sqlQuery = 'UPDATE collector SET coins = coins + 2*accessFrequency, accessFrequency = accessFrequency + 1 WHERE email = new.email;'
                        else:
                            sqlQuery = 'UPDATE COLLECTOR SET accessFrequency = 0 WHERE id = %s'
                            cursor.execute(sqlQuery, (user))

                        con.commit()
                        #================================= Checar se a frequencia deve ser mantida e premiar =================================

                elif(qtdRows == 0):  
                    mensagem = "Usuário não cadastrado"
                    server.comandoSOCK(index, mensagem)



            elif(mensagem == 'printInventario'):  
                user = self.listID[index]
                sqlQuery = "SELECT * FROM INVENTORY_CARDS\
                    JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
                    JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = COLLECTOR.id\
                    WHERE INVENTORY_CARDS.idCollector = %s"
                cursor.execute(sqlQuery, (user)) 
                teste = cursor.fetchall()
                teste = json.dumps(teste, indent =4, sort_keys=True, default=str)
                server.comandoSOCK(index,teste)
            
            elif(mensagem == 'printAlbum'):
                index = self.listSOCK.index(cliente) 
                user = self.listID[index]
                sqlQuery = "SELECT * FROM Album A JOIN Collection_Cards B ON A.id = B.idAlbum\
                    JOIN Card C ON C.id = B.idCard\
                    JOIN Collector D ON A.id = D.idAlbum\
                    JOIN Collector E ON E.idAlbum = A.id WHERE E.id = %s"
                cursor.execute(sqlQuery, (user))
                teste = cursor.fetchall() 
                teste = json.dumps(teste, indent =4, sort_keys=True, default=str) 
                index = self.listSOCK.index(cliente) 
                server.comandoSOCK(index,teste)

            elif(mensagem == 'loja'):  
                
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
                    qtdCoins = qtdCoins - precoOferta
                    sqlQuery = "UPDATE Collector SET coins = %s WHERE id = %s" #debita a quantidade de moedas pagas na oferta
                    cursor.execute(sqlQuery, (qtdCoins, idUser))
                    sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCard = %s" #pega a quantidade de cartas desse tipo no inventário do comprador
                    qtdCards = cursor.execute(sqlQuery, (consulta2[0].get('idCards')))
                    inventoryCardInfo = cursor.fetchAll()
                    if(qtdCards > 0):
                        sqlQuery = "UPDATE Inventory_Cards SET quantity = %s" #aumenta a quantidade de cartas do mesmo tipo caso o comprador ja possua a carta no inventário
                        cursor.execute(sqlQuery, str(inventoryCardInfo[0].get('quantity')+1))
                    else:
                        sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)" #insere a carta no inventário do comprador caso ele não possua uma instancia dela no inventário
                        cursor.execute(sqlQuery, (consulta2[0].get('idCards') ,idUser))
                    
                    sqlQuery = "SELECT coins FROM COLLECTOR WHERE COLLECTOR.id = %s" #pega a quantidade de moedas do vendedor, para calcular o novo valor
                    cursor.execute(sqlQuery, (consulta2[0].get('idCollector')))
                    consultaCoins = cursor.fetchall()
                    coinsVendedor = consultaCoins[0].get('coins')
                    coinsVendedor = coinsVendedor + precoOferta
                    sqlQuery = "UPDATE COLLECTOR SET coins = %s WHERE id = %s" #paga o vendedor da oferta
                    cursor.execute(sqlQuery, (coinsVendedor, consulta2[0].get('idCollector')))

                    sqlQuery = "DELETE FROM Store_Cards WHERE Store_Cards.id = %s" #remove a oferta da loja, pois ela ja foi consumida
                    cursor.execute(sqlQuery, (idOferta))
                        #falta adicionar o dinheiro ao usuário que estava vendendo caso o campo idCollector seja != NULL
                    con.commit()
                else:
                    mensagem = 'quantidade de moedas insuficiente'
                    server.comandoSOCK(index,mensagem)
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
                    server.comandoSOCK(index, 'usuario inserido')
                    #cursor.commit()
                else:
                    mensagem = "as senhas não coincidem"
                    server.comandoSOCK(index, mensagem) 

            elif(mensagem == "ColarFigura"):  
                
                # get figure id  
                figure_id = '1'    
                user = self.listSOCK.index(cliente)
                sqlQuery = "Select idAlbum FROM Collector WHERE id = %s"
                cursor.execute(sqlQuery, str(user))
                response = cursor.fetchall()
                idAlbum = response[0].get('idAlbum')
                print("o id do album é: " + idAlbum)
                sqlQuery = "SELECT * FROM Card A WHERE A.id NOT IN (SELECT id FROM Collection_cards WHERE idAlbum = %s)"
                cursor.execute(sqlQuery, (idAlbum))
                response = cursor.fetchall()
                requiredCards = response

                idCardToSticker = cliente.recv(1024).decode()
                sqlQuery = "SELECT * FROM Inventory_Cards WHERE idColletor = %s AND idCard = %s"
                cardExist = cursor.execute(sqlQuery, (user, idCardToSticker))
                if cardExist > 0:
                    if cardExist > 1:
                        sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                        cursor.execute(sqlQuery, (idAlbum, idCardToSticker))
                        sqlQuery = "UPDATE Inventory_Cards Set quantity quantity - 1 WHERE idCard = %s AND idCollector = %s"
                        cursor.execute(sqlQuery, (idCardToSticker, user))

                    else:
                        sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                        cursor.execute(sqlQuery, (idAlbum, idCardToSticker))
                        sqlQuery = "DELETE FROM Inventory_Cards WHERE idCard = %s AND idCollector = %s"
                        cursor.execute(sqlQuery, (idCardToSticker, user))
                    con.commit()
                else:
                    print('Quantidade de cartas insuficiente')



                
                # # obtem a quantidade de figuras coladas no album
                # quantityStickeredFromAlbum = "SELECT quantityStickeredCards JOIN Album ON Album.id = Collector.idAlbum WHERE id = %s" 
                # cursor.execute(quantityStickeredFromAlbum, (user))  
                # # atualiza 
                # sqlQuery = """ UPDATE Album SET quantityStickeredCards = %s JOIN Album ON Album.id = Collector.idAlbum
                # WHERE (SELECT idAlbum JOIN Collector ON Album.id = Collector.id  
                # WHERE Album.id = Collector.idalbum) = %s """
                # # atualiza  
                # # inserir  no collection cards  (indicando o id da carta e o id do album )
                # cursor.execute(sqlQuery,(quantityStickeredFromAlbum, user))
                # # 
                # delete = "DELETE FROM tabela WHERE JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
                #     JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = %s\
                # WHERE INVENTORY_CARDS.idCard = %s" 
                # cursor.execute(delete,(user,figure_id)) 

            elif(mensagem == "troca"):  
                print('entrei na troca')
                user = self.listID[index]  
                index = self.listSOCK.index(cliente)
                
                choice = cliente.recv(1024).decode()
                print("o choice é: " + str(choice))
                if choice == "1": 
                    #criar oferta  
                    print('entrei no if')
                    # usuario envia o id da carta que quer enviar
                    idCardtoSend = cliente.recv(1024).decode() 
                    #usuario envia id da carta que quer receber
                    idCardToReceive = cliente.recv(1024).decode()   
                    # criação de uma nova oferta
                    
                    #Retorna todos os dados mas só mostra para o cliente o email dos jogadores
                    # getAllEmails = """SELECT * FROM COLLECTOR""" 
                    # cursor.execute(getAllEmails)  
                    # getAllEmails = cursor.fetchall() 
                    # getEmailReturn = json.dumps(getAllEmails, indent =4, sort_keys=True, default=str)
                    # server.comandoSOCK(index,getEmailReturn)

                    # emailSelected = cliente.recv(1024).decode()  
                    
                    
                    # idAlbum = list(filter(lambda d: d['email'] == emailSelected,getAllEmails))
                    #Quando email de usuario for selecionado vai aparecer a opção "ver album"
                    #A query abaixo vai exibir as cartas faltantes no album do usuário selecionado pelo email
                    #SELECT name, description FROM CARD A JOIN Collection_Card B Where B.idAlbum = 'IdDoAlbumArmazenadoNoSelectDeCima' AND A.id != B.idCard
                    
                    print('entrei no if')
                    firstSQL = """INSERT INTO Exchanges (idCollectorOwner, idCollectorTarget, idCard, idCardReceived) 
                                   VALUES (%s, %s, %s, %s)""" 
                    idTeste = 3 
                    cursor.execute(firstSQL, (user,idTeste,idCardtoSend, idCardToReceive))  
                    con.commit()
                    send = "Oferta criada" 
                    print(send)
                    server.comandoSOCK(index, send) 



                else: 
                    # observar a troca 
                    # o usuario podera aceitar ou negar uma oferta de troca  caso seja o solicitado  
                    # o usuario podera manter ou cancelar uma oferta de troca caso seja o solicitante 

                 
                    showExchange = """SELECT  B.id AS OwnerId,  
                                            C.id AS collectorID,  
                                            B.email AS CollectorOwnerEmail,  
                                            C.email AS CollectorTargetEmail,  
                                            D.name AS CardTraded,  
                                            E.name AS CardReceived,  
                                            D.id AS CardTradedId,  
                                            E.id AS CardReceivedId,  
                                            D.id AS CardTradedId, 
                                            A.id AS exId   
                                FROM Exchanges A  
                                JOIN Collector B ON B.id = A.idCollectorOwner  
                                JOIN Collector C ON C.id = A.idCollectorTarget 
                                JOIN CARD D ON D.id = A.idCard  
                                JOIN CARD E ON E.id = A.idCardReceived  
                                WHERE A. idCollectorOwner = %s OR A.idCollectorTarget = %s """
                    cursor.execute(showExchange,(user, user))  
                    showExchangeReturn = cursor.fetchall() 
                    showExchangeReturn = json.dumps(showExchangeReturn, indent =4, sort_keys=True, default=str)
                    server.comandoSOCK(index,showExchangeReturn)
                    
                    i = int(cliente.recv(1024).decode()) 
                    # o for vai estar no menu for i in range(len(showexchangeReturn)): 
                    # o usuario, por meio do menu, retorna em qual exchange irá retornar


                    idOwner = ast.literal_eval(showExchangeReturn)[i].get('OwnerId')
                    idCollector = ast.literal_eval(showExchangeReturn)[i].get('collectorID')

                    idCardTraded = ast.literal_eval(showExchangeReturn)[i].get('CardTradedId')
                    idCardReceived = ast.literal_eval(showExchangeReturn)[i].get('CardReceivedId') 
                    idExchange = ast.literal_eval(showExchangeReturn)[i].get('exId') 
                    print('O id exchange é: ' + str(idExchange))
                    print('antes do if')
                    print(str(user) + " o outro id é " + str(idOwner))
                    if str(user) == str(idOwner):   
                        print('entrei no if')
                        # caso o cliente no momento seja o solicitante da troca
                        send = "Retirar proposta - 1    Manter proposta - 2"
                        print(send)
                        server.comandoSOCK(index, send) 
                        ans = cliente.recv(1024).decode() 
                            
                        if ans == '1':
                            print('entramos no if')
                            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
                            cardExist = cursor.execute(sqlCheckCardInInventory, (user, idCardTraded))
                            print('o cardExist tem valor ' + str(cardExist)) 
                            
                            if cardExist > 0: # Se número de linhas > 0
                                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                                cursor.execute(sqlQuery, (user, idCardTraded))
                                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                                cursor.execute(sqlQuery, (str(idExchange)))
                                    # UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = 'idDoUsuario' AND idCard = 'idCardDaOfertaAceita'
                            else:# Se número de linhas = 0
                                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                                cursor.execute(sqlQuery, (str(idCardTraded), user))
                                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                                cursor.execute(sqlQuery, (str(idExchange)))
                            
                            con.commit() 
                            send = "Proposta Retirada!"
                            server.comandoSOCK(index, send)
                            
                        else:    
                            send = "Proposta Mantida!"
                            server.comandoSOCK(index, send)
                            
                            

                                
                    elif str(user) == str(idCollector):    

                                # caso o cliente no momento seja o solicitado da troca 
                        send = "Aceitar troca - 1\nNegar troca - 2"
                        server.comandoSOCK(index, send) 
                            
                        ans = cliente.recv(1024).decode() 
                            
                        if ans == '1':
                            #se target
                            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
                            cardExist = cursor.execute(sqlCheckCardInInventory, (user, idCardTraded))
                            if cardExist > 0: # Se número de linhas > 0
                                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = %s AND idCard = '%s"
                                cursor.execute(sqlQuery, (user, str(idCardTraded)))
                            else: # Se número de linhas = 0
                                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                                cursor.execute(sqlQuery,(idCardTraded, user)) 
                                
                            #se criador da oferta
                            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
                            cardExist = cursor.execute(sqlCheckCardInInventory, (str(idOwner), str(idCardReceived)))
                            if cardExist > 0: # Se número de linhas > 0
                                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                                cursor.execute(sqlQuery, (str(idOwner), str(idCardReceived)))
                            else: # Se número de linhas = 0
                                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                                cursor.execute(sqlQuery, (str(idCardReceived), str(idOwner)))
                            sqlQuery = "DELETE FROM Exchanges WHERE id = %s"
                            cursor.execute(sqlQuery, (str(idExchange)))
                            con.commit()  
                            
                            send = "Troca feita!"
                            server.comandoSOCK(index, send) 
                        else:    
                            send = "Troca Negada!"
                            server.comandoSOCK(index, send)
                            

                        sqlInventarioUpdate1 = """SELECT * FROM Inventory_Cards 
                                    WHERE idCollector = %s  AND idCard = %s """ 
                        qtRows = cursor.execute(sqlInventarioUpdate1, (user, str(idCardReceived))) 
                        if qtRows > 0: 
                            
                            update = """UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = %s AND idCard = %s """ 
                            cursor.execute(update,(user, str(idCardReceived) ))
                        else:  
                            
                            insert = """  INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES ( %s , 1, %s) """  
                            cursor.execute(insert,(str(idCardReceived), user)) 
                        
                        sqlinventarioUpdate2 = """SELECT quantity  
                                                FROM Inventory_Cards  
                                                WHERE idCollector = %s AND idCard = %s """  
                        qtRows = cursor.execute(sqlinventarioUpdate2,(user, str(idCardTraded))) 
                        
                        if qtRows == 1: 
                            deleteNoInventario = """DELETE FROM Inventory_Cards  
                                                    WHERE idCollector = %s AND idCard = %s """ 
                            cursor.execute(deleteNoInventario,(user, idCardTraded)) 
                        elif qtRows > 1: 
                            updateInventario = """UPDATE Inventory_Cards SET quantity = quantity-1 WHERE idCollector = %s AND idCard = %s """ 
                            cursor.execute(updateInventario,(user, idCardTraded))
                    
                    
                                
                
            # elif(mensagem == 'comprar'):
            #     index = self.listSOCK.index(cliente)
            #     idUser = self.listID[index]
            #     ofertas = "SELECT * FROM Store_Cards"
            #     idOferta = cliente.recv(1024).decode()
            #     sqlQuery = "SELECT"
            #     sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
            #     cursor.execute(sqlQuery, (idUser))
            #     consultaResponse = cursor.fetchall()
            #     quantityCoins =  consultaResponse[0].get('coins')
            #     if(quantityCoins >= )
                
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



