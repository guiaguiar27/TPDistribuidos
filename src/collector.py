from .album import album 
from .inventory import inventory  
import json

class collector:  

    def __init__(self):   
        self.inventory = None
        self.coins = 0
        self.email = None  
        self.password  = None
        self.album = None 
        self.name = None 
        self.ClientSocket = None


    def addCard(self, Card): 
        pass
    
    
    def NewUser(self,email,password, name):  

        self.inventory = inventory()
        self.album = album()
        self.email = email # graphical input 
        self.password = password # graphical input     
        self.name = name
        
      
    def addCoins(self):   

        coins = input("How many coins do you want to add? ") 
        self.coins += coins 
    
    def removeCoins(self,coins): 
        self.coins -= coins 

    def PutSticker(self): 
        pass 
    
    def show_collector(self):
        print("Collector: " + self.name) 
        print("Coins: " + str(self.coins))
        print("Email: " + self.email)
        print("Password: " + self.password) 


    def showCardFI(self,name, idC, description): 
        print("----Informacoes da carta----")
        print("ID: ",idC) 
        print("Nome: ",name)
        print("descricao: ",description) 
        print("----------------------------")  
        
    def show_album(self,client):  

        firstRequest = "printAlbum" 
        client.sock.send(firstRequest.encode()) 
        
        response = client.sock.recv(6144).decode() 
        response = response.replace("'", "\"") 
        FinalResponse = json.loads(response) 

        for dictionary in FinalResponse:
            idc  =  dictionary.get('id')
            description = dictionary.get('description') 
            name = dictionary.get('name') 
            self.showCardFI(name, idc, description)
    