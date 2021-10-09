# saved as greeting-client.py
import Pyro4
import sys   
#sys.path.insert(0, '/Users/Macbook/Documents/TPDistribuidos/Client')  
sys.path.insert(0, '../')  
 
from src.collector import collector 
import json 
import random  
import os 


def buyPacket(client):  
    
    returnMessage = client.comprarPacote()
    print(returnMessage)
    
def showCatalogo(client):  
    response = client.catalogo() 

    response = response.replace("'", "\"") 
    FinalResponse = json.loads(response)  
    for Dictionary in FinalResponse: 
        print("------Informacoes da carta-----")
        print(" {} - {} - {}".format(Dictionary.get('id'),Dictionary.get('name'),Dictionary.get('description'))) 
        print("----------------------------")

def colar(client,User):    

    print("---------------COLAR------------------")    
    albumDec = int(input("1 - Visualizar inventario\n"))
    if albumDec == 1: 
         User.inventory.getInventory(client) 
      
    print("Cartas faltantes:")  
    response = client.colarFigurinha()
    response = response.replace("'", "\"") 
    FinalResponse = json.loads(response) 
    for Dictionary in FinalResponse: 
        print("------Informacoes da carta-----")
        print(" {} - {} - {}".format(Dictionary.get('id'),Dictionary.get('name'),Dictionary.get('description'))) 
        print("----------------------------")
    
    getId = int(input("Digite o ID da carta que deseja colar:")) 
    returnMessage = client.ColarFiguraDefined(getId) 
    if returnMessage == 'Sucesso!': 
        print("Colada")  
    else: 
        print('Carta não foi colada!') 

def showColecionadores(client): 
    response = client.getColecionadores() 
    response = response.replace("'", "\"") 
    FinalResponse = json.loads(response) 
    for Dictionary in FinalResponse: 
        print("--------USUARIO-------")
        print(" {} - {}".format(Dictionary.get('id'),Dictionary.get('email'))) 
        print("----------------------------")
    
def exchange(client,User):  

    print('---------------TROCA------------------')   
        
    print("Digite 1 para ativar troca\n2 para analisar trocas pendentes") 
    ans = int(input())   
    if ans == 1:  
        
        show = int(input("1 - Visualizar cartas do inventario\n2 - Para prosseguir\n"))  
        if show == 1:   
        
            print("Inventário") 
            User.inventory.getInventory(client) 
        
        idCardTrade = input("Entre com o id da carta que deseja trocar:") 
        
        show = int(input("1 - Visualizar cartas disponíveis\n2 - Para prosseguir\n"))  
        if show == 1:  
            print("Cartas disponiveis:")  
            showCatalogo(client)
        
        idCardReceive = input("Entre com o id da carta que deseja receber: ") 
        print("Usuarios disponíveis para troca:") 
        showColecionadores(client) 
        user = int(input("Entre com o id do colecionador que deseja barganhar:"))

        returnMessage = client.trocaCriarOferta(idCardTrade,idCardReceive,user)
        print(returnMessage) 
    
    else:  
        # observar ofertas  
        returnMessage = client.trocaObservarOferta()  

        #print(returnMessage) #DEBUG 
        if returnMessage != None:   
            
            returnMessage = returnMessage.replace("'", "\"") 
            FinalResponse = json.loads(returnMessage)
            if len(FinalResponse) > 0: 
                    
                for i in range(len(FinalResponse)):
                    print("Troca ativa - ID: ",FinalResponse[i].get('exId'))

                ex = int(input("Digite o id da troca que deseja operar:")) 
                for i in range(len(FinalResponse)):
                    if ex == FinalResponse[i].get('exId'):
                        ex = i

                returnToIf = client.trocaAceitarOferta(ex)  
                if returnToIf == "Retirar proposta - 1\nManter proposta - 2\n":
                    ans = input(returnToIf)     
                    print(client.TrocaDecision(ans, ex)) 
                else:  
                    ans = input(returnToIf) 
                    print(client.avaliarOfertas(ans, ex))  
            else: 
                print("Não há nenhuma troca ativa!") 
                return 

             

def shop(client): 
    

    print('---------------LOJA------------------')   
    FirstResponse = client.loja() 
    response = FirstResponse.replace("'", "\"") 
    FinalResponse = json.loads(response) 
   
    for i in FinalResponse:
        
        price  =  i.get('price')
        description = i.get('description') 
        nameCard = i.get('carta') 
        idCard = i.get('id')  
        
        print("----Informacoes da oferta----")
        print("{} - {} - {} - {}".format(idCard, nameCard,price,description)) 
        print("----------------------------")

    oferta = int(input("Entre com o id da oferta ou -2 para sair:")) 
    if oferta == -2: 
        return 
    
    response = client.realizarCompra(oferta) 
    
    if response == "quantidade de moedas insuficiente": 
        print("Quantidade de moedas insuficiente\nAs cartas não foram adicionadas ao seu inventario") 
    else: 
        print("Compra bem sucedida\nAs cartas foram adcionadas ao seu inventario")



def login(client): 
    print('---------------LOGIN------------------')  
    email = str(input("email:"))  
    password = str(input("Password:")) 
    mensagem = client.login(email,password)
    if mensagem == "Login feito com sucesso": 
        print("Login efetuado com sucesso") 
        User = collector()  
        User.NewUser(email, password,email) 
        #client.checkUserFrequency()
        return User 
    else: 
        User = None
    return User

def register(client):  

    print('---------------REGISTRO------------------')  
    firstRequisition = "cadastrar"  
    user = str(input("User:"))    
    email = str(input("Email: "))  
    password = str(input("Senha:"))
    password2 = str(input("Digite a senha novamente:"))
    
    returnMessage = client.cadastrar(user, email, password, password2)
    if returnMessage == "usuario inserido": 
        print("Usuario cadastrado")
        NewUser = collector() 
        NewUser.NewUser(email, password,user) 
        NewUser.show_collector()              
        return NewUser  
    elif returnMessage == "Email ja cadastrado":  
        print("Email ja cadastrado")
        login(client)
    else: 
        return None
# # pagina de acesso do usuario  



def menu(User,client): 
    print('---------------MENU------------------')  
    opion = 0  
    while opion != 6:
        print("Pagina menu - User: {}".format(User.name))  
        inputMessage = """   
        \n  
        1 -  Acessar perfil   
        2 -  Acessar album   
        3 -  Acessar inventario  
        4 -  Acessar Loja  
        5 -  Troca 
        6 -  Colar No Album 
        7 -  Comprar Pacotes 
        \n
        """
        option = int(input(inputMessage)) 
        if option == 1:
            User.show_collector(client)
        elif option == 2:   
            User.show_album(client)   
        elif option == 3:      
            User.inventory.getInventory(client) 
        elif option == 4:  
            shop(client)
        elif option == 5:  
            exchange(client,User) 
        elif option == 6:    
            colar(client,User)  
        elif option == 7:    
            buyPacket(client)

            #sys.exit()


#pagina inicial
def init(client): 
    
    print("Entre com 1 para login ou 2 para cadastro:") 
    First = int(input())  
    if First == 1:  
        User = login(client)
        if User != None: 
            menu(User,client)
        else: 
            print("Login invalido") 
            init(client)

    else: 
        User = register(client)
        if User != None:
            menu(User,client) 
        else: 
            sys.exit("Usuario nao autenticado")  


if __name__ == '__main__':   
    uri = input("What is the Pyro uri of the greeting object? ").strip() 
    greeting_maker = Pyro4.Proxy(uri)         # obtem um Pyro proxy para o objeto
    init(greeting_maker) 

