from card import card 

class inventory: 
    def __init__(self): 
        self.quantity = 0 
        self.Cards = []  

    def addCardsOnInventory(self, Card): 
        self.Cards.append(Card) 
        self.quantity += 1 
    def showInventory(self): 
        for i in self.Cards: 
            i.showCard()