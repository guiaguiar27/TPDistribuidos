from .album import album 
from .inventory import inventory  

class collector:  

    def __init__(self):   

        self.inventory  = None
        self.coins = 0
        self.email = None  
        self.password  = None
        self.album = None


    def addCard(self, card: Card): 
        pass
    def login(self): 
        pass  
    def logou(self): 
        pass 
    
    def NewUser(self):  

        self.inventory = inventory()
        self.album = album()
        self.email = getEmail() # graphical input 
        self.password = getPassword() # graphical input 
        self.coins = 0    
        
      
    def addCoins(self): 
        pass 
    def PutSticker(self): 
        pass 

