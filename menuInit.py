import sys   
#sys.path.insert(0, '/Users/Macbook/Documents/TPDistribuidos/Client')  
sys.path.insert(0, '../src')  

#from client import Client 
from src.collector import collector 
import ast


class menuinit:
    def __init__(self,ip,port): 

        self._ip = ip
        self._port = port  
    
    def colar(self,client):   
        client.sock.send("ColarFigura".encode()) 
          
        print("Colada")

    def exchange(self, client): 
        tr = "troca"
        client.sock.send(tr.encode())  
         
        print("Digite 1 para ativar troca\n 2 para analisar trocas pendentes") 
        ans = int(input())   
        if ans == 1:  
            # criar oferta 
            client.sock.send(str(ans).encode())       
            idCardTrade = input("Entre com o id da carta que deseja trocar:") 
            client.sock.send(idCardTrade.encode())   
            idCardReceive = input("Entre com o id da carta que deseja receber: ")
            client.sock.send(idCardReceive.encode()) 

            print(client.sock.recv(1024).decode()) 
        else:  
            client.sock.send(str(ans).encode())        
            response = client.sock.recv(1024).decode()  
            if response != None:   
                
                l = ast.literal_eval(response) 
                for i in range(len(l)):
                    print(l[i].get('exId'))

                ex = input(("Digite o id da troca que deseja operar:")) 
                ex = int(ex) - 1 

                client.sock.send(str(ex).encode())   
                
                response = client.sock.recv(1024).decode() 
                print(response) 

                ans = int(input("")) 
                client.sock.send(str(ans).encode()) 

                finalResponse = client.sock.recv(1024).decode() 
                print(finalResponse)
                        
            # analisar ofertas pendentes 

    def shop(self,client): 
        req = "loja" 
        
        client.sock.send(req.encode())  
        FirstResponse = client.sock.recv(1024).decode()  
        if FirstResponse != None:   
                
                response = ast.literal_eval(FirstResponse)
                for i in range(len(response)):
                    price  =  response[i].get('price')
                    description = response[i].get('description') 
                    nameCard = response[i].get('name') 
                    print("----Informacoes da carta----")
                    print("{} - {} - {} - {}".format(i,nameCard,price,description)) 
                    print("----------------------------")

        oferta = int(input("Entre com o valor da oferta:")) 
        client.sock.send(str(oferta).encode()) 
        response = client.sock.recv(1024).decode() 
        
        if response == "quantidade de moedas insuficiente": 
            print("Quantidade de moedas insuficiente\nAs cartas não foram adcionadas ao seu inventario") 
        else: 
            print("Compra bem sucedida\nAs cartas foram adcionadas ao seu inventario")

    def login(self,client): 

        print("---------------LOGIN------------------")  
        
        #client.mensagemThread() 
        #client.threadHandler()    

        firstRequisition = "login"
        client.sock.send(firstRequisition.encode()) 

        email = str(input("email:"))  
        client.sock.send(email.encode()) 
        
        password = str(input("Password:")) 
        client.sock.send(password.encode()) 
        
        mensagem = client.sock.recv(1024).decode()
        if mensagem == "Login feito com sucesso": 
            print("Login efetuado com sucesso") 
            User = collector()  
            User.NewUser(email, password,email)
            return User 
        else: 
            User = None
        return User

    def register(self,client):  

        print("---------------REGISTRO------------------")  
        #client = Client(self._ip,self._port) 

        firstRequisition = "cadastrar"  

        client.sock.send(firstRequisition.encode())
        
        user = str(input("User:"))    
        client.sock.send(user.encode())
        
        email = str(input("Email: "))  
        client.sock.send(email.encode())
        
        password = str(input("Senha:"))
        client.sock.send(password.encode()) 
        
        password2 = str(input("Digite a senha novamente:"))
        client.sock.send(password2.encode()) 
        
        returnMessage = client.sock.recv(1024).decode() 
        if returnMessage == "usuario inserido": 
            print("Usuario cadastrado")
            NewUser = collector() 
            NewUser.NewUser(email, password,user) 
            NewUser.show_collector()              
            return NewUser  
        elif returnMessage == "Email ja cadastrado":  
            print("Email ja cadastrado")
            self.login(self,client)
        else: 
            return None
    # pagina de acesso do usuario  



    def menu(self, User,client): 
        print("---------------MENU------------------")  
        opion = 0  
        while opion != 6:
            print("Pagina menu - User: {}".format(User.name)) 
            option = int(input("1 - Acessar perfil \n2 - Acessar album \n3 - Acessar inventario \n4 - Acessar Loja \n 5 - Troca \n 6 - Colar No Album\n")) 
            if option == 1:
                User.show_collector()
            elif option == 2:   
                print("---------------ALBUM------------------")  
                User.show_album(client)   

            elif option == 3: 
                print("---------------INVENTARIO------------------")     
                #User.inventory.showInventory()
                User.inventory.getInventory(client) 

            elif option == 4:  
                print("---------------LOJA------------------")   
                self.shop(client)

            elif option == 5:  
                print("---------------TROCA------------------")  
                self.exchange(client) 
            elif option == 6:   
                print("---------------TROCA------------------")  
                self.colar(client)

                #sys.exit()


    #pagina inicial
    def init(self,client): 
        
        print("Entre com 1 para login ou 2 para cadastro:") 
        First = int(input())  
        if First == 1:  
            User = self.login(client)
            if User != None: 
                self.menu(User,client)
            else: 
                print("Login invalido") 
                self.init(client)

        else: 
            User = self.register(client)
            if User != None:
                self.menu(User,client) 
            else: 
                sys.exit("Usuario nao autenticado")  
    

if __name__ == '__main__':  
    pass
    # address = input("Insira o enderesço de conexão: ")
    # garbage, dataAdress = address.split("//") 
    # global _ip 
    # global _port
    # _ip, _port = dataAdress.split(":") 
    #init()
