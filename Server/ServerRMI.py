
import os
import subprocess
import signal
import threading
import time 
import sys   
import Pyro4 
from rmiechoserver import RMIEchoServer 
import json
import ast
import numpy as np 
from copy import deepcopy

HOST = 'localhost' 
PORT = 0000
# @Pyro4.expose
# class GreetingMaker(object):
#     def get_fortune(self, name):
#         return "Hello, {0}. Here is your fortune message:\n" \
#                "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)


con = MySQLdb.connect(host="localhost", user="root", passwd="123root123", db="albumdb")
cursor = con.cursor(MySQLdb.cursors.DictCursor)

@Pyro4.expose
class AlbumConnection(object):
        
    
    def mensagem(self, cliente):
    #index = self.listSOCK.index(cliente)
        while True:
            mensagem = cliente.recv(1024).decode()
            print("a mensagem é: " + mensagem) 
            
            # if(mensagem == 'iniciar'):
            #     index = self.listSOCK.index(cliente)
            #     return  "insira o próximo comando"

            
            # elif(mensagem == 'insere'): 
            #     cursor.execute("SELECT * FROM COLLECTOR")
            #     teste = cursor.fetchall()
            #     teste = json.dumps(teste, indent=4)
            #     index = self.listSOCK.index(cliente)
            #     #res = [tuple(map(lambda x: x.encode('utf-8'), tup)) for tup in teste]
            #     return teste 

    def login(self, email, senha):#elif(mensagem == 'login'):
        print('insira o email: ')
        #email = cliente.recv(1024).decode()
        print('insira a senha: ')
        #senha = cliente.recv(1024).decode()
        #index = self.listSOCK.index(cliente)
        #print("o index é: " + str(index))
        #sqlQuery = "SELECT id FROM COLLECTOR WHERE email = %s AND password = %s"
        #cursor.execute(sqlQuery,(testeLogin, testeSenha))
        # cursor.execute("SELECT id FROM COLLECTOR WHERE email = %s AND senha %s" % (testeLogin, testeSenha))
        print(str(email))
        print(str(senha))
        
        qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (email))
        ReturnDB = cursor.fetchall() 

        if(qtdRows > 0):
            #passwordDB = cursor.excute("SELECT password FROM Collector WHERE Collector.id = %s" % (userID))
            passFromDb =  ReturnDB[0].get('password')
            if(senha == passFromDb):
                states.idUser = ReturnDB[0].get('id')
                mensagem  = "Login feito com sucesso"
                return mensagem
            elif(qtdRows == 0):  
                mensagem = "Usuário não cadastrado"
                return mensagem
    def checkUserFrequency(self):
        #self.listID.append(str(states.idUser))

        print('o tamanho da lista é: ' + str(len(self.listID)))
        #user = self.listID[index]
        print('o usuario é: ' + str(user) )
        #================================= Checar se a frequencia deve ser mantida e premiar =================================
        sqlQuery = "SELECT DATE(lastConnection) AS lastConnectionYesterday FROM COLLECTOR WHERE id = %s"
        print('o id do usuário é: ' + (user))
        cursor.execute(sqlQuery, [states.idUser])
        oldDateResponse = cursor.fetchall()
        oldLastConnection = oldDateResponse[0].get('lastConnectionYesterday')
        sqlQuery = 'SELECT DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) AS newLastConnection'
        cursor.execute(sqlQuery)
        newDateResponse = cursor.fetchall()
        newLastConnection = newDateResponse[0].get('newLastConnection')
        print(str(oldLastConnection) + '     ' + str(newLastConnection))
        if(oldLastConnection == newLastConnection):
            sqlQuery = 'UPDATE COLLECTOR SET coins = coins + accessFrequency+2, accessFrequency = accessFrequency+1, lastConnection = %s WHERE id = %s'
            cursor.execute(sqlQuery, (newLastConnection, [states.idUser]))
            # sqlQuery = 'UPDATE collector SET coins = coins + 2*accessFrequency, accessFrequency = accessFrequency + 1 WHERE email = new.email;'
        else:
            sqlQuery = 'UPDATE COLLECTOR SET accessFrequency = 0 WHERE id = %s'
            cursor.execute(sqlQuery, [states.idUser])

        con.commit()
        #================================= Checar se a frequencia deve ser mantida e premiar =================================




    def printInventario(self):
    #elif(mensagem == 'printInventario'):  
        user = self.listID[index]
        sqlQuery = "SELECT * FROM INVENTORY_CARDS\
            JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
            JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = COLLECTOR.id\
            WHERE INVENTORY_CARDS.idCollector = %s"
        cursor.execute(sqlQuery, [user]) 
        teste = cursor.fetchall()
        teste = json.dumps(teste, indent =4, sort_keys=True, default=str)
        return teste
    
    def printAlbum(self):  #elif(mensagem == 'printAlbum'):
        index = self.listSOCK.index(cliente) 
        user = self.listID[index]
        sqlQuery = "SELECT C.id, C.name, C.description FROM Album A JOIN Collection_Cards B ON A.id = B.idAlbum\
            JOIN Card C ON C.id = B.idCard\
            JOIN Collector D ON A.id = D.idAlbum\
            JOIN Collector E ON E.idAlbum = A.id WHERE E.id = %s"
        cursor.execute(sqlQuery, [user])
        teste = cursor.fetchall() 
        teste = json.dumps(teste, indent =4, sort_keys=True, default=str) 
        index = self.listSOCK.index(cliente) 
        return mensagem

    def loja(self):#    elif(mensagem == 'loja'):  
            
            sqlQuery = "SELECT A.price, (SELECT C.name FROM Collector C WHERE A.idCollector = C.id) AS Vendedor,\
                B.name AS Carta, B.description, B.picture\
                FROM Store_Cards A JOIN Card B ON A.idCards = B.id" 

            cursor.execute(sqlQuery)
            teste = cursor.fetchall() 
            teste = json.dumps(teste, indent =4) 
            index = self.listSOCK.index(cliente) 
            return teste
            idUser = self.listID[index]
            
            print('o id do usuario é: ' + str(idUser))
            idOferta = cliente.recv(1024).decode()
            #sqlQuery = "SELECT"
            sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
            cursor.execute(sqlQuery, (idUser))
            consulta = cursor.fetchall()
            qtdCoins = consulta[0].get('coins')
            sqlQuery = "SELECT * FROM Store_Cards WHERE id = %s"
            print("id da oferta é: " + str(idOferta))
            cursor.execute(sqlQuery, (idOferta))
            consulta2 = cursor.fetchall()
            precoOferta = consulta2[0].get('price')
            if(precoOferta <= qtdCoins):
                qtdCoins = qtdCoins - precoOferta
                sqlQuery = "UPDATE Collector SET coins = %s WHERE id = %s" #debita a quantidade de moedas pagas na oferta
                cursor.execute(sqlQuery, (qtdCoins, idUser))
                sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCard = %s" #pega a quantidade de cartas desse tipo no inventário do comprador
                print("o id da carta é: " + str(consulta2[0].get('idCards')))
                qtdCards = cursor.execute(sqlQuery, str(consulta2[0].get('idCards')))
                inventoryCardInfo = cursor.fetchall()
                if(qtdCards > 0):
                    sqlQuery = "UPDATE Inventory_Cards SET quantity = %s" #aumenta a quantidade de cartas do mesmo tipo caso o comprador ja possua a carta no inventário
                    cursor.execute(sqlQuery, str(inventoryCardInfo[0].get('quantity')+1))
                else:
                    sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)" #insere a carta no inventário do comprador caso ele não possua uma instancia dela no inventário
                    cursor.execute(sqlQuery, (consulta2[0].get('idCards') ,idUser))
                
                if(consulta2[0].get('idCollector') != None):
                    sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s" #pega a quantidade de moedas do vendedor, para calcular o novo valor
                    print("aquiiii: " + str(consulta2[0]))
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
                mensagem = 'Compra realizada com sucesso!'
                return mensagem
            else:
                mensagem = 'quantidade de moedas insuficiente'
                return mensagem 
            print(consulta[0].get('coins'))
            print(json.dumps(consulta, indent = 4))


    def catalogo(self):
        sqlQuery = "SELECT * FROM Card"
        cursor.execute(sqlQuery)
        teste = cursor.fetchall()   
        teste = json.dumps(teste, indent =4) 
        #index = self.listSOCK.index(cliente) 
        return teste 
                    
    def cadastrar(self, userName, userEmail, password, passwordValidation):
        print('bora cadastrar')
        #pedir nome
        #index = self.listSOCK.index(cliente)
        #userName = cliente.recv(1024).decode()
        #pedir email
        #userEmail = cliente.recv(1024).decode()
        #pedir senha
        #password = cliente.recv(1024).decode()
        #pedir confirmação de senha
        #passwordValidation = cliente.recv(1024).decode()
        qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (userEmail))
        if(qtdRows > 0):
            mensagem = "Email ja cadastrado" 
            return mensagem
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
            mensagem =  "usuario inserido" 
            return mensagem 

            # qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (userEmail)) era pra colocar o usuario na listIds na conexão de sockets
            # ReturnDB = cursor.fetchall() 
            # if(qtdRows > 0):
            #     self.listID.append(str(ReturnDB[0].get('id')))
            #cursor.commit()
        else:
            mensagem = "as senhas não coincidem" 
            return mensagem


               
            
        
                


    def colarFigurinha(self):#        elif(mensagem == "ColarFigura"):  
        # get figure id   
        #index = self.listSOCK.index(cliente) 
        #user = self.listID[index]
        sqlQuery = "Select idAlbum FROM Collector WHERE id = %s"
        #print(str(user))
        cursor.execute(sqlQuery, [states.idUser])
        response = cursor.fetchall()
        print(str(response))
        states.idAlbum = response[0].get('idAlbum')
        sqlQuery = "SELECT * FROM Card A WHERE A.id NOT IN (SELECT idCard FROM Collection_cards WHERE idAlbum = %s)"
        cursor.execute(sqlQuery, str(states.idAlbum))
        response = cursor.fetchall()
        requiredCards = response
        requiredCards = json.dumps(requiredCards, indent =4, sort_keys=True, default=str)
        return requiredCards


    # no front quando o usuario chamar a opcao de colar figurinha  
    # apos o retorno das opçõs de figuras restantes  
    # a funcão colarfigurasDefined é chamada com a mensagem do id da carta  

    def ColarFiguraDefined(self, idCardToSticker):  
        sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
        cardExist = cursor.execute(sqlQuery, ([states.idUser], idCardToSticker))
        if cardExist > 0:
            if cardExist > 1:
                sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                cursor.execute(sqlQuery, (states.idAlbum, idCardToSticker))
                sqlQuery = "UPDATE Inventory_Cards Set quantity quantity - 1 WHERE idCard = %s AND idCollector = %s"
                cursor.execute(sqlQuery, (idCardToSticker, [states.idUser]))

            else:
                sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                cursor.execute(sqlQuery, (states.idAlbum, idCardToSticker))
                sqlQuery = "DELETE FROM Inventory_Cards WHERE idCard = %s AND idCollector = %s"
                cursor.execute(sqlQuery, (idCardToSticker, [states.idUser]))
            con.commit()   

            return "Sucesso!"
            
        else:
            mensagem = "Quantidade de cartas insuficiente" 
            return mensagem

               
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

    def troca(self):
        print('entrei na troca') 
        # index = self.listSOCK.index(cliente) 
        # user = self.listID[index]
        
        # choice = cliente.recv(1024).decode()
        print("o choice é: " + str(choice))


    # definido no front quando o usuario deseja criar uma nova oferta 
    def trocaCriarOferta(self, idCardtoSend, idCardToReceive): #if choice == "1": 
        #criar oferta  
        print('entrei no if')
        # usuario envia o id da carta que quer enviar
        #idCardtoSend = cliente.recv(1024).decode() 
        #usuario envia id da carta que quer receber
        #idCardToReceive = cliente.recv(1024).decode()   
        # criação de uma nova oferta
    
        print('entrei no if')
        firstSQL = """INSERT INTO Exchanges (idCollectorOwner, idCollectorTarget, idCard, idCardReceived) 
                        VALUES (%s, %s, %s, %s)""" 
        idTeste = 3 
        cursor.execute(firstSQL, ([states.idUser],idTeste,idCardtoSend, idCardToReceive))  
        con.commit()
        send = "Oferta criada" 
        print(send)
        return send


    
    # definido no front quando o usuario deseja criar uma observar uma oferta 
    def trocaObservarOferta(self): 
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
        cursor.execute(showExchange,([states.idUser], [states.idUser]))  
        showExchangeReturn = cursor.fetchall() 
        showExchangeReturn = json.dumps(showExchangeReturn, indent =4, sort_keys=True, default=str)
        states.availableExchanges = deepcopy(showExchange)
        return showExchangeReturn 

        
    # depois de observar as ofertas o usuario escolhe se aceita/nega (solicitado) mantem/retira(solicitante) 
    # no front o usuario passa o id da oferta que deseja trabalhar  

    def trocaAceitarOferta(self, indexOferta):


        idOwner = ast.literal_eval(states.availableExchanges)[indexOferta].get('OwnerId') 
        idCollector = ast.literal_eval(states.availableExchanges)[indexOferta].get('collectorID')

        print('O id exchange é: ' + str(indexOferta))
        print('antes do if')
        print(str([states.idUser]) + " o outro id é " + str(idOwner))
        if str([states.idUser]) == str(idOwner):   
            print('entrei no if')
            # caso o cliente no momento seja o solicitante da troca 
            # colocar no front para manter ou não a proposta  
            
            send = "Retirar proposta - 1\nManter proposta - 2"
            print(send)
            return send  
            #vai ter if no front pra chamar trocaDecision 
        elif str([states.idUser]) == str(idCollector):    
            # caso o cliente no momento seja o solicitado da troca  
            #vai ter if no front pra chamar AvaliarOferta 
            send = "Aceitar troca - 1\nNegar troca - 2"
            return send
        
    # ator:  solicitante da troca 
    def TrocaDecision(self, ans, indexOferta): 
        idCollector = ast.literal_eval(states.availableExchanges)[indexOferta].get('collectorID')
        idCardTraded = ast.literal_eval(states.availableExchanges)[indexOferta].get('CardTradedId')
        idCardReceived = ast.literal_eval(states.availableExchanges)[indexOferta].get('CardReceivedId') 
        idExchange = ast.literal_eval(states.availableExchanges)[indexOferta].get('exId') 

        if ans == '1':

            # 
            # tem que implementar a remoção da carta do inventario na hora da criação da oferta 
            #

            print('entramos no if')
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, (states.idUser, idCardTraded))
            print('o cardExist tem valor ' + str(cardExist)) 
            
            if cardExist > 0: # Se número de linhas > 0
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                cursor.execute(sqlQuery, (states.idUser, idCardTraded))
                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                cursor.execute(sqlQuery, (str(idExchange)))
                    # UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = 'idDoUsuario' AND idCard = 'idCardDaOfertaAceita'
            else:# Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery, (str(idCardTraded), [states.idUser]))
                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                cursor.execute(sqlQuery, (str(idExchange)))
            
            con.commit() 
            send = "Proposta Retirada!"
            return send
            
        else:    
            send = "Proposta Mantida!"
            return send
            
            
    # ator: colecionador solicitado para a troca             
    def avaliarOfertas(self,ans, indexOferta): 
        idCollector = ast.literal_eval(states.availableExchanges)[indexOferta].get('collectorID')
        idCardTraded = ast.literal_eval(states.availableExchanges)[indexOferta].get('CardTradedId')
        idCardReceived = ast.literal_eval(states.availableExchanges)[indexOferta].get('CardReceivedId') 
        idExchange = ast.literal_eval(states.availableExchanges)[indexOferta].get('exId') 

        if ans == '1': 
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, (states.idUser, idCardTraded))
            #insercao 
            if cardExist > 0: # Se número de linhas > 0
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 Where idCollector = %s AND idCard = '%s"
                cursor.execute(sqlQuery, (states.idUser, str(idCardTraded)))
            else: # Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery,(idCardTraded, [states.idUser])) 
                
            #faltando perder a carta 
        
            #criador da oferta
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
            return send
        else:    
            send = "Troca Negada!"

            return send
            



    

    # no caso de não prender a carta na oferta (tirando do inventario)
    # sqlinventarioUpdate2 = """SELECT quantity  
    #                         FROM Inventory_Cards  
    #                         WHERE idCollector = %s AND idCard = %s """   
    # # se eu tenho a carta que eu vou mandar 
    # cursor.execute(sqlinventarioUpdate2,(user, str(idCardTraded))) 
    # response = cursor.fetchall() 
    # quantity = response[0].get('quantity') 

    # if quantity == 1: 
    #     deleteNoInventario = """DELETE FROM Inventory_Cards  
    #                             WHERE idCollector = %s AND idCard = %s """ 
    #     cursor.execute(deleteNoInventario,(user, idCardTraded)) 
    # elif quantity > 1: 
    #     updateInventario = """UPDATE Inventory_Cards SET quantity = quantity-1 WHERE idCollector = %s AND idCard = %s """ 
    #     cursor.execute(updateInventario,(user, idCardTraded))
            





    def comprarPacote(self):            
        # 1 pacote
        print('entrou para comprar pacote')
        pcktPrice = 10.0 
        sqlQuery = "SELECT coins FROM collector WHERE id = %s" 
        cursor.execute(sqlQuery, [states.user]) 
        currentCoinCollector = cursor.fetchall()  
        cur = currentCoinCollector[0].get("coins")
        if (cur  >= pcktPrice): 
            for i in range(4): 
                idRandom = np.random.randint(12)  
                verify  = "SELECT * FROM inventory_cards WHERE idCard = %s AND idCollector = %s" 
                QtRows = cursor.execute(verify, ([idRandom],[states.user])) 
                if QtRows > 0:
                    update = "UPDATE inventory_CARDS SET quantity = quantity + 1 WHERE idCollector = %s and idCard = %s" 
                    cursor.execute(update, ([states.user],[idRandom])) 
                    print('tinha a carta')
                else:
                    insertInventory = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, %s, %s)" 
                    cursor.execute(insertInventory, ([idRandom], 1, [states.user]))
                    print('não tinha a carta')
            
                dis = "UPDATE Collector SET coins = coins - %s WHERE id = %s" 
                cursor.execute(dis,([pcktPrice],[states.user]))  
                con.commit()

            return "Compra efetuada com sucesso!"
        else: 
            return "Saldo insuficiente!"



class States:
    def __init__(self):
        self.availableExchanges = []
        self.idUser = 0
        self.idAlbum = 0



states = States()
daemon = Pyro4.Daemon()                # make a Pyro daemon
uri = daemon.register(AlbumConnection)   # register the greeting maker as a Pyro object

print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
print('teste')

