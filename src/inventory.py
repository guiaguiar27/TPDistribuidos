from .card import card  
import json  

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
        FirstResponse = client.sock.recv(6144).decode()  
        #print(FirstResponse) 

        response = FirstResponse.replace("'", "\"")  
        FinalResponse = json.loads(response) 
        
        for dictionary in FinalResponse:
            idc  =  dictionary.get('CARD.id') 
            description = dictionary.get('description') 
            name = dictionary.get('name') 
            self.showCardFI(name, idc, description)


        # for i in range(len(response)):
        #     idc  =  response[i].get('CARD.id') 
        #     print(idc)
        #     description = response[i].get('description') 
        #     print(description)
        #     name = response[i].get('name') 
        #     print(name)
        #     #self.showCardFI(name, idc, description)

            
       


        # print(response.decode())  
        # ReturnDB = cursor.fetchall() 
        # id  =  ReturnDB[0].get('CARD.id')
        # description = ReturnDB[0].get('description') 
        # name = ReturnDB[0].get('name')
