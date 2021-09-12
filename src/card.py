class card: 
    def __init__(self, name, description):
        super().__init__() 
        self.name = name
        self.description = description 
         
    def  showCard(self) :
        print(self.name)
        print(self.description) 