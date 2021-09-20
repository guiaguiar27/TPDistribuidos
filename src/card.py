class card: 
    def __init__(self, name, description):
        super().__init__() 
        self.name = name
        self.description = description
        self.id = None  
        self.FileAddress = None #1.png - 2.png

    def  showCard(self):
        print(self.name)
        print(self.description) 

