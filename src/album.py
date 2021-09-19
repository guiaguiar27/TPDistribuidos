class album: 
    def __init__(self):
        super().__init__() 
        self.album_id = None 
        self.stickeredCards = [] 
    def addCardsIndividual(self, card): 
        self.stickeredCards.append(card)
    def addCardsFromPack(self, pack): 
        for  i in pack: 
            self.stickeredCards.append(i)

    def showCards(self): 
        for i in self.stickeredCards: 
            i.showCard()   