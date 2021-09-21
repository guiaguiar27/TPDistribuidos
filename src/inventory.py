from .card import card  
import ast

class inventory: 
    def __init__(self): 
        self.quantity = 0 
        self.Cards = []  

    def addCardsOnInventory(self, Card): 
        self.Cards.append(Card) 
        self.quantity += 1  

    
    def showCardFI(self,name, idC, description): 
        print("----Informacoes da carta----")
        print("ID: ",idC) 
        print("Nome: ",name)
        print("descricao: ",description) 
        print("----------------------------") 
        
    def getInventory(self,client): 
        FirstRequest = "printInventario" 
        client.sock.send(FirstRequest.encode())
        FirstResponse = client.sock.recv(1024).decode() 
        #print(response.decode())  
        if FirstResponse != None:   
                response = ast.literal_eval(FirstResponse)
                for i in range(len(response)):
                    idc  =  response[i].get('CARD.id')
                    description = response[i].get('description') 
                    name = response[i].get('name') 
                    self.showCardFI(name, idc, description)

            
       


        # print(response.decode())  
        # ReturnDB = cursor.fetchall() 
        # id  =  ReturnDB[0].get('CARD.id')
        # description = ReturnDB[0].get('description') 
        # name = ReturnDB[0].get('name')
