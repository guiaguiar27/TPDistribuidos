import json  

class inventory: 
    def __init__(self): 
        self.quantity = 0 
        self.Cards = []  

    def showCardFI(self,name, idC, description,quantity): 
        print("----Informacoes da carta----")
        print("ID: ",idC) 
        print("Nome: ",name)
        print("descricao: ",description)  
        print("Quantidade: ",quantity)
        print("----------------------------") 
        
    def getInventory(self,client): 
        print("---------------INVENTARIO------------------")  
        FirstResponse = client.printInventario()  
        response = FirstResponse.replace("'", "\"")  
        FinalResponse = json.loads(response) 
        
        for dictionary in FinalResponse:
            idc  =  dictionary.get('CARD.id') 
            description = dictionary.get('description') 
            name = dictionary.get('name')  
            quantity = dictionary.get('quantity')
            self.showCardFI(name, idc, description,quantity)

