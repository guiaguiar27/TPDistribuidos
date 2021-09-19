import sys   
sys.path.insert(0, '/Users/Macbook/Documents/TPDistribuidos/Client')  
sys.path.insert(0, '/Users/Macbook/Documents/TPDistribuidos/src')  

from client import Client 
from src.collector import collector 


class menuinit:
    def __init__(self,ip,port): 

        self._ip = ip
        self._port = port 
    
    def login(self,client):  
        
        
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
            return User 
        else: 
            User = None
        return User

    def register(self,client): 
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
            
            NewUser = collector() 
            NewUser.NewUser(email, password,user) 
            NewUser.show_collector()              
            return NewUser  

        else: 
            return None
    # pagina de acesso do usuario 
    def menu(self, User): 
        print("---------------MENU------------------")  
        opion = 0  
        while opion != 5:
            print("Pagina menu - User: {}".format(User.name)) 
            option = int(input("1 - Acessar perfil \n2 - Acessar album \n3 - Acessar inventario \n4 - Acessar Loja \n 5 - Sair \n")) 
            if option == 1:
                User.show_collector()
            elif option == 2:  
                print("==Pagina album==")   
                User.show_album() 
            elif option == 3: 
                print("==Inventario==") 
            elif option == 4: 
                print("==Pagina Loja==") 
            elif option == 5: 
                print("==Sair==") 
                sys.exit()


    #pagina inicial
    def init(self): 
        
        print("Entre com 1 para login ou 2 para cadastro:") 
        First = int(input())  
        if First == 1:  
            User = login()
            if User != None: 
                self.menu(User)  
            else: 
                print("Login invalido") 
                self.init()

        else: 
            User = register()
            if User != None:
                self.menu(User) 
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
