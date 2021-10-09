
import os
import subprocess
import signal
import threading
import time 
import sys   
import Pyro4 
import json
import ast
import numpy as np 
from copy import deepcopy 
import MySQLdb # para o MySQL

HOST = 'localhost' 
PORT = 0000

con = MySQLdb.connect(host="localhost", user="root", passwd="123root123", db="albumdb")
cursor = con.cursor(MySQLdb.cursors.DictCursor)

@Pyro4.behavior(instance_mode="session")
@Pyro4.expose
class AlbumConnection(object):
    def __init__(self) -> None:
        super().__init__() 
        self.states = States()    
    
    
    def login(self, email, senha):
        print('insira o email: ')
        print('insira a senha: ')
        print(str(email))
        print(str(senha))
        
        qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (email))
        ReturnDB = cursor.fetchall() 

        if(qtdRows > 0):
            passFromDb =  ReturnDB[0].get('password')
            if(senha == passFromDb):
                self.states.idUser = ReturnDB[0].get('id')
                mensagem  = "Login feito com sucesso"
                return mensagem
            elif(qtdRows == 0):  
                mensagem = "Usuário não cadastrado"
                return mensagem
    def checkUserFrequency(self):

        print('o tamanho da lista é: ' + str(len(self.listID)))
        print('o usuario é: ' + str(self.states.idUser) )
        #================================= Checar se a frequencia deve ser mantida e premiar =================================
        sqlQuery = "SELECT DATE(lastConnection) AS lastConnectionYesterday FROM COLLECTOR WHERE id = %s"
        print('o id do usuário é: ' + (self.states.idUser))
        cursor.execute(sqlQuery, [self.states.idUser])
        oldDateResponse = cursor.fetchall()
        oldLastConnection = oldDateResponse[0].get('lastConnectionYesterday')
        sqlQuery = 'SELECT DATE(DATE_SUB(NOW(), INTERVAL 1 DAY)) AS newLastConnection'
        cursor.execute(sqlQuery)
        newDateResponse = cursor.fetchall()
        newLastConnection = newDateResponse[0].get('newLastConnection')
        print(str(oldLastConnection) + '     ' + str(newLastConnection))
        if(oldLastConnection == newLastConnection):
            sqlQuery = 'UPDATE COLLECTOR SET coins = coins + accessFrequency+2, accessFrequency = accessFrequency+1, lastConnection = %s WHERE id = %s'
            cursor.execute(sqlQuery, (newLastConnection, [self.states.idUser]))
        else:
            sqlQuery = 'UPDATE COLLECTOR SET accessFrequency = 0 WHERE id = %s'
            cursor.execute(sqlQuery, [self.states.idUser])

        con.commit()
        #================================= Checar se a frequencia deve ser mantida e premiar =================================




    def printInventario(self): 
        sqlQuery = "SELECT * FROM INVENTORY_CARDS\
            JOIN CARD ON INVENTORY_CARDS.idCard = CARD.id\
            JOIN COLLECTOR ON  INVENTORY_CARDS.idCollector = COLLECTOR.id\
            WHERE INVENTORY_CARDS.idCollector = %s"
        cursor.execute(sqlQuery, [self.states.idUser]) 
        teste = cursor.fetchall()
        teste = json.dumps(teste, indent =4, sort_keys=True, default=str)
        return teste
    
    def printAlbum(self):
        sqlQuery = "SELECT C.id, C.name, C.description FROM Album A JOIN Collection_Cards B ON A.id = B.idAlbum\
            JOIN Card C ON C.id = B.idCard\
            JOIN Collector D ON A.id = D.idAlbum\
            JOIN Collector E ON E.idAlbum = A.id WHERE E.id = %s"
        cursor.execute(sqlQuery, [self.states.idUser])
        mensagem = cursor.fetchall() 
        mensagem = json.dumps(mensagem, indent =4, sort_keys=True, default=str) 
        return mensagem

    def loja(self):#após executar esta função devemos, através do front, pedir para que o usuario insira o id da oferta
            
            sqlQuery = "SELECT A.id, A.price, (SELECT C.name FROM Collector C WHERE A.idCollector = C.id) AS Vendedor,\
                B.name AS Carta, B.description, B.picture\
                FROM Store_Cards A JOIN Card B ON A.idCards = B.id" 

            cursor.execute(sqlQuery)
            mensagem = cursor.fetchall() 
            mensagem = json.dumps(mensagem, indent =4) 
            return mensagem 
    
    def realizarCompra(self, idOferta):
            print("id da oferta é: " + str(idOferta))
            sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
            cursor.execute(sqlQuery, [self.states.idUser])
            print("id da oferta é: " + str(idOferta))
            consulta = cursor.fetchall()
            qtdCoins = consulta[0].get('coins')
            sqlQuery = "SELECT * FROM Store_Cards WHERE id = %s"
            print("id da oferta é: " + str(idOferta))
            cursor.execute(sqlQuery, [idOferta])
            consulta2 = cursor.fetchall()
            precoOferta = consulta2[0].get('price')
            if(precoOferta <= qtdCoins):
                qtdCoins = qtdCoins - precoOferta
                sqlQuery = "UPDATE Collector SET coins = %s WHERE id = %s" #debita a quantidade de moedas pagas na oferta
                cursor.execute(sqlQuery, ([qtdCoins], [self.states.idUser]))
                sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCard = %s" #pega a quantidade de cartas desse tipo no inventário do comprador
                print("o id da carta é: " + str(consulta2[0].get('idCards')))
                qtdCards = cursor.execute(sqlQuery, [str(consulta2[0].get('idCards'))])
                inventoryCardInfo = cursor.fetchall()
                if(qtdCards > 0):
                    sqlQuery = "UPDATE Inventory_Cards SET quantity = %s" #aumenta a quantidade de cartas do mesmo tipo caso o comprador ja possua a carta no inventário
                    cursor.execute(sqlQuery, [str(inventoryCardInfo[0].get('quantity')+1)])
                else:
                    sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)" #insere a carta no inventário do comprador caso ele não possua uma instancia dela no inventário
                    cursor.execute(sqlQuery, ([consulta2[0].get('idCards')] ,[self.states.idUser]))
                
                if(consulta2[0].get('idCollector') != None):
                    sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s" #pega a quantidade de moedas do vendedor, para calcular o novo valor
                    print("aquiiii: " + str(consulta2[0]))
                    cursor.execute(sqlQuery, ([consulta2[0].get('idCollector')]))
                    consultaCoins = cursor.fetchall()
                    coinsVendedor = consultaCoins[0].get('coins')
                    coinsVendedor = coinsVendedor + precoOferta
                    sqlQuery = "UPDATE COLLECTOR SET coins = %s WHERE id = %s" #paga o vendedor da oferta
                    cursor.execute(sqlQuery, ([coinsVendedor], [consulta2[0].get('idCollector')]))

                sqlQuery = "DELETE FROM Store_Cards WHERE Store_Cards.id = %s" #remove a oferta da loja, pois ela ja foi consumida
                cursor.execute(sqlQuery, ([idOferta]))
                con.commit()
                mensagem = 'Compra realizada com sucesso!'
                return mensagem
            else:
                mensagem = 'quantidade de moedas insuficiente'
                return mensagem 


    def catalogo(self):
        sqlQuery = "SELECT * FROM Card"
        cursor.execute(sqlQuery)
        teste = cursor.fetchall()   
        teste = json.dumps(teste, indent =4) 
        return teste 
                    
    def cadastrar(self, userName, userEmail, password, passwordValidation):
        qtdRows = cursor.execute("SELECT * FROM Collector WHERE email = '%s'" % (userEmail))
        if(qtdRows > 0):
            mensagem = "Email ja cadastrado" 
            return mensagem
        elif(password == passwordValidation):
            sqlQuery = "INSERT INTO album (quantityCards, quantityStickeredCards) VALUES (0,0);"
            cursor.execute(sqlQuery)
            sqlQuery = "INSERT INTO collector (name, email, password, coins, idAlbum) VALUES (%s, %s, %s, 10, %s);"
            print(cursor.lastrowid)
            cursor.execute(sqlQuery, ([userName], [userEmail], [password], [cursor.lastrowid]))
            con.commit() 

            print('usuario inserido') 
            mensagem =  "usuario inserido" 
            return mensagem 
        else:
            mensagem = "as senhas não coincidem" 
            return mensagem


               
            
        
                


    def colarFigurinha(self):
        sqlQuery = "Select idAlbum FROM Collector WHERE id = %s"
        cursor.execute(sqlQuery, [self.states.idUser])
        response = cursor.fetchall()
        print(str(response))
        self.states.idAlbum = response[0].get('idAlbum')
        sqlQuery = "SELECT * FROM Card A WHERE A.id NOT IN (SELECT idCard FROM Collection_cards WHERE idAlbum = %s)"
        cursor.execute(sqlQuery, [str(self.states.idAlbum)])
        response = cursor.fetchall()
        requiredCards = response
        requiredCards = json.dumps(requiredCards, indent =4, sort_keys=True, default=str)
        return requiredCards


    # no front quando o usuario chamar a opcao de colar figurinha  
    # apos o retorno das opçõs de figuras restantes  
    # a funcão colarfigurasDefined é chamada com a mensagem do id da carta  

    def ColarFiguraDefined(self, idCardToSticker):  
        sqlQuery = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
        cardExist = cursor.execute(sqlQuery, ([self.states.idUser], [idCardToSticker]))
        if cardExist > 0: 
            sqlQuery2 = "SELECT * FROM Collection_Cards WHERE idAlbum = %s and idCard = %s" 
            cardInAlbum = cursor.execute(sqlQuery2, ([self.states.idAlbum],[idCardToSticker])) 
            if  cardInAlbum == 0: 
            
                if cardExist > 1:
                    sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                    cursor.execute(sqlQuery, (self.states.idAlbum, [idCardToSticker]))
                    sqlQuery = "UPDATE Inventory_Cards Set quantity = quantity - 1 WHERE idCard = %s AND idCollector = %s"
                    cursor.execute(sqlQuery, (idCardToSticker, [self.states.idUser]))

                else:
                    sqlQuery = "INSERT INTO Collection_Cards (idAlbum, idCard) Values (%s,%s)"
                    cursor.execute(sqlQuery, (self.states.idAlbum, [idCardToSticker]))
                    sqlQuery = "DELETE FROM Inventory_Cards WHERE idCard = %s AND idCollector = %s"
                    cursor.execute(sqlQuery, (idCardToSticker, [self.states.idUser]))
                con.commit()   

                return "Sucesso!" 
            else: 
                mensagem = "Carta já colada" 
                return mensagem
                
        else:
            mensagem = "Quantidade de cartas insuficiente" 
            return mensagem

    def getColecionadores(self):
        ColecionadoresInfoQuery = """SELECT id, email FROM Collector"""
        cursor.execute(ColecionadoresInfoQuery)
        collectors = cursor.fetchall() 
        collectors = json.dumps(collectors, indent =4, sort_keys=True, default=str)
        return collectors


    
    # definido no front quando o usuario deseja criar uma nova oferta 
    def trocaCriarOferta(self, idCardtoSend, idCardToReceive, idColecionador): #if choice == "1": 
        #criar oferta  
        # criação de uma nova oferta
        hasCardQuery = """SELECT quantity FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"""
        qtdRows = cursor.execute(hasCardQuery, ([self.states.idUser], [idCardtoSend])) 
        
        card = cursor.fetchall() 
        if qtdRows > 0: 
            hasCard = card[0].get('quantity')
            if(hasCard > 0):
                if(hasCard == 1): #igual a 1
                    deleteCardQuery = """DELETE FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"""
                    cursor.execute(deleteCardQuery, ([self.states.idUser], [idCardtoSend]))
                else:
                    decreaseCardQuery = """UPDATE Inventory_Cards Set quantity = quantity - 1 WHERE idCollector = %s AND idCard = %s"""
                    cursor.execute(decreaseCardQuery, ([self.states.idUser], [idCardtoSend]))
                firstSQL = """INSERT INTO Exchanges (idCollectorOwner, idCollectorTarget, idCard, idCardReceived) 
                                VALUES (%s, %s, %s, %s)""" 
                cursor.execute(firstSQL, ([self.states.idUser],[idColecionador],[idCardtoSend], [idCardToReceive]))  
                con.commit()
                send = "Oferta criada" 
                return send
        else:
            send = "Impossível criar oferta. Quantidade de cartas insuficiente!"
            return send


    
    # definido no front quando o usuario deseja criar uma observar uma oferta 
    def trocaObservarOferta(self): 
        # observar a troca 
        # o usuario podera aceitar ou negar uma oferta de troca  caso seja o solicitado  
        # o usuario podera manter ou cancelar uma oferta de troca caso seja o solicitante 

        
        showExchange = """SELECT B.id AS OwnerId,  
                                C.id AS collectorID,  
                                B.email AS CollectorOwnerEmail,  
                                C.email AS CollectorTargetEmail,  
                                D.name AS CardTraded,  
                                E.name AS CardReceived,  
                                D.id AS CardTradedId,  
                                E.id AS CardReceivedId,  
                                A.id AS exId   
                    FROM Exchanges A  
                    JOIN Collector B ON B.id = A.idCollectorOwner  
                    JOIN Collector C ON C.id = A.idCollectorTarget 
                    JOIN CARD D ON D.id = A.idCard  
                    JOIN CARD E ON E.id = A.idCardReceived  
                    WHERE A.idCollectorOwner = %s OR A.idCollectorTarget = %s """
        cursor.execute(showExchange,([self.states.idUser], [self.states.idUser]))  
        showExchangeReturn = cursor.fetchall() 
        showExchangeReturn = json.dumps(showExchangeReturn, indent =4, sort_keys=True, default=str)
        self.states.availableExchanges = deepcopy(showExchangeReturn)
        return showExchangeReturn 

        
    # depois de observar as ofertas o usuario escolhe se aceita/nega (solicitado) mantem/retira(solicitante) 
    # no front o usuario passa o id da oferta que deseja trabalhar  

    def trocaAceitarOferta(self, indexOferta):

        print('cheguei no aceitar oferta')
        print(str(self.states.availableExchanges))
        idOwner = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('OwnerId') 
        idCollector = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('collectorID')

        print('O id exchange é: ' + str(indexOferta))
        print('antes do if')
        print(str(self.states.idUser) + " o outro id é " + str(idOwner))
        if str(self.states.idUser) == str(idOwner):   
            print('entrei no if')
            # caso o cliente no momento seja o solicitante da troca 
            # colocar no front para manter ou não a proposta  
            
            send = "Retirar proposta - 1\nManter proposta - 2\n"
            print(send)
            return send  
            #vai ter if no front pra chamar trocaDecision 
        elif str(self.states.idUser) == str(idCollector):    
            # caso o cliente no momento seja o solicitado da troca  
            #vai ter if no front pra chamar AvaliarOferta 
            send = "Aceitar troca - 1\nNegar troca - 2\n"
            return send
        
    # ator:  solicitante da troca 
    def TrocaDecision(self, ans, indexOferta): 
        idCollector = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('collectorID')
        idCardTraded = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('CardTradedId')
        idCardReceived = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('CardReceivedId') 
        idExchange = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('exId') 
        print(str(ans))
        if ans == '1':

            print('entramos no if')
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, ([self.states.idUser], [idCardTraded]))
            print('o cardExist tem valor ' + str(cardExist)) 
            
            if cardExist > 0: # Se número de linhas > 0
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                cursor.execute(sqlQuery, ([self.states.idUser], [idCardTraded]))
                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                cursor.execute(sqlQuery, ([str(idExchange)]))
            else:# Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery, ([str(idCardTraded)], [self.states.idUser]))
                sqlQuery= "DELETE FROM Exchanges WHERE id = %s"
                cursor.execute(sqlQuery, ([str(idExchange)]))
            
            con.commit() 
            send = "Proposta Retirada!"
            return send
            
        else:    
            send = "Proposta Mantida!"
            return send
            
            
    # ator: colecionador solicitado para a troca             
    def avaliarOfertas(self,ans, indexOferta): 
        idOwner = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('OwnerId') 
        idCollector = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('collectorID')
        idCardTraded = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('CardTradedId')
        idCardReceived = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('CardReceivedId') 
        idExchange = ast.literal_eval(self.states.availableExchanges)[indexOferta].get('exId') 

        if ans == '1':
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, ([self.states.idUser], [idCardTraded]))
            #insercao 
            if cardExist > 0: # Se número de linhas > 0
                print(str(idCardTraded) + " eeeeeee ")
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                cursor.execute(sqlQuery, ([self.states.idUser], [idCardTraded]))
            else: # Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery,([idCardTraded], [self.states.idUser]))
                
            #faltando perder a carta 
            hasCardQuery = """SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"""
            cursor.execute(hasCardQuery, ([self.states.idUser], [idCardReceived])) 
            card = cursor.fetchall()
            hasCard = card[0].get('quantity')
            if(hasCard > 0):
                if(hasCard == 1): #igual a 1
                    deleteCardQuery = """DELETE FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"""
                    cursor.execute(deleteCardQuery, ([self.states.idUser], [idCardReceived]))
                else:
                    decreaseCardQuery = """UPDATE Inventory_Cards Set quantity = quantity - 1 WHERE idCollector = %s AND idCard = %s"""
                    cursor.execute(decreaseCardQuery, ([self.states.idUser], [idCardReceived]))
                    
            #criador da oferta
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, ([idOwner], [idCardReceived]))
            if cardExist > 0: # Se número de linhas > 0
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                cursor.execute(sqlQuery, ([idOwner], [idCardReceived]))
            else: # Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery, ([idCardReceived], [idOwner]))
            sqlQuery = "DELETE FROM Exchanges WHERE id = %s"
            cursor.execute(sqlQuery, ([idExchange]))
            con.commit()  
            
            send = "Troca feita!"
            return send
        else:
            # devolver idOwner 
            sqlCheckCardInInventory = "SELECT * FROM Inventory_Cards WHERE idCollector = %s AND idCard = %s"
            cardExist = cursor.execute(sqlCheckCardInInventory, ([idOwner], [idCardTraded]))
            if cardExist > 0: # Se número de linhas > 0
                sqlQuery = "UPDATE Inventory_Cards SET quantity = quantity+1 WHERE idCollector = %s AND idCard = %s"
                cursor.execute(sqlQuery, ([idOwner], [idCardTraded]))
            else: # Se número de linhas = 0
                sqlQuery = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, 1, %s)"
                cursor.execute(sqlQuery, ([idCardTraded], [idOwner]))
            con.commit()  
            send = "Troca Negada!"

            return send


    def comprarPacote(self):            
        # 1 pacote
        pcktPrice = 10.0 
        sqlQuery = "SELECT coins FROM collector WHERE id = %s" 
        cursor.execute(sqlQuery, [self.states.idUser]) 
        currentCoinCollector = cursor.fetchall()  
        cur = currentCoinCollector[0].get("coins")
        if (cur  >= pcktPrice): 
            for i in range(4): 
                idRandom = np.random.randint(1,12)  
                verify  = "SELECT quantity FROM inventory_cards WHERE idCard = %s AND idCollector = %s" 
                QtRows = cursor.execute(verify, ([idRandom],[self.states.idUser]))  
                
                if QtRows > 0:
                    print('tem a carta')
                    update = "UPDATE inventory_CARDS SET quantity = quantity + 1 WHERE idCollector = %s and idCard = %s" 
                    cursor.execute(update, ([self.states.idUser],[idRandom])) 
                    print('tinha a carta')
                else:
                    print('não tem a carta')
                    print(str(idRandom))
                    insertInventory = "INSERT INTO Inventory_Cards (idCard, quantity, idCollector) VALUES (%s, %s, %s)" 
                    cursor.execute(insertInventory, ([idRandom], 1, [self.states.idUser]))
                    print('não tinha a carta')
            
            dis = "UPDATE Collector SET coins = coins - %s WHERE id = %s" 
            cursor.execute(dis,([pcktPrice],[self.states.idUser]))  
            con.commit()

            return "Compra efetuada com sucesso!"
        else: 
            return "Saldo insuficiente!" 
    def getCoins(self): 
        sqlQuery = "SELECT coins FROM COLLECTOR WHERE id = %s"
        cursor.execute(sqlQuery, [self.states.idUser])
        coins = cursor.fetchall()
        coins = json.dumps(coins, indent =4, sort_keys=True, default=str) 
        return coins
        


@Pyro4.behavior(instance_mode="session")
@Pyro4.expose
class States:
    def __init__(self):
        self.availableExchanges = []
        self.idUser = 0
        self.idAlbum = 0
        self.idInventory = 0 




#self.states = States()
daemon = Pyro4.Daemon()                # Faz um Pyro daemon
uri = daemon.register(AlbumConnection)   # Registra uma instancia de objeto como  um Pyro object

print("Ready. Object uri: ")      # printa uri para que o cliente possa acessar
print(uri)
daemon.requestLoop()                    # start the event loop of the server to wait for calls
#threading.Thread(target=daemon.requestLoop).start()

