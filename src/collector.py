from .album import album 

class collector:  

    def __init__(self, ColletctorAlbum): 
        self.cards = []  
        self.stickeredCards = [] 
        self.coins = 0
        self.email = None  
        self.password  = None
        self.album = ColletctorAlbum
    


    def addCard(self, card: Card): 
        pass 
    def login(self): 
        pass  
    def logou(self): 
        pass 
    
    def NewUser(self): 
        
        self.email = getEmail() # graphical input 
        self.password = getPassword() # graphical input 
        self.coins = 0   

      
    def addCoins(self): 
        pass 
    def PutSticker(self): 
        pass 

