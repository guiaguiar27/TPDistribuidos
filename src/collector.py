from .inventory import inventory  
import json 



class collector:  

    def __init__(self):   
        self.inventory = None
        self.coins = 0
        self.email = None  
        self.password  = None
        self.name = None 
        self.ClientSocket = None


    def addCard(self, Card): 
        pass
    
    
    def NewUser(self,email,password, name):  

        self.inventory = inventory()
        self.email = email # graphical input 
        self.password = password # graphical input     
        self.name = name
        

    
    def show_collector(self,client):
        print("Collector: " + self.name)  
        
        response = client.getCoins() 
        response = response.replace("'", "\"") 
        FinalResponse = json.loads(response)  
        
        for c in FinalResponse: 
            coins = c.get('coins')
        print("Coins: " + str(coins))
        print("Email: " + self.email)
        print("Password: " + self.password) 


    def showCardFI(self,name, idC, description): 
        print("----Informacoes da carta----")
        print("ID: ",idC) 
        print("Nome: ",name)
        print("descricao: ",description) 
        print("----------------------------")  
        
    
    def show_album(self,client):  
        print("---------------ALBUM------------------")  
        
        response = client.printAlbum() 
        response = response.replace("'", "\"") 
        FinalResponse = json.loads(response) 

        for dictionary in FinalResponse:
            idc  =  dictionary.get('id')
            description = dictionary.get('description') 
            name = dictionary.get('name') 
            self.showCardFI(name, idc, description)
    