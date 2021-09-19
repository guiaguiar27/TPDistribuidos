from collector import collector 
import sys

def login(): 
    name = str(input("User:")) 
    password = str(input("Password:")) 
        #collector =  vai receber infos do bd 
    # precisa do acesso ao bd
    User = None 
    
    return User

def register(): 
    user = str(input("User:")) 
    email = str(input("Email: ")) 
    password = str(input("Password:"))
    NewUser = collector() 
    NewUser.NewUser(email, password,user) 
    #NewUser.show_collector()  
    
    return NewUser 

# pagina de acesso do usuario 
def menu(User): 
    print("---------------MENU------------------")  
    opion = 0  
    while opion != 5:
        print("Pagina menu - User: {}".format(User.name)) 
        option = int(input("1 - Acessar perfil \n2 - Acessar album \n3 - Acessar inventario \n4 - Acessar Loja \n 5 - Sair \n")) 
        if option == 1:
            User.show_collector()
        elif option == 2:  
            print("==Pagina album==") 
        elif option == 3: 
            print("==Inventario==") 
        elif option == 4: 
            print("==Pagina Loja==") 
        elif option == 5: 
            print("==Sair==") 
            sys.exit()


#pagina inicial
def init(): 
    print("Entre com 1 para login ou 2 para cadastro:") 
    First = int(input()) 
    if First == 1:  
        User = login()
        if User != None: 
            menu(User)  
        else: 
            print("Login invalido") 
            init()

    else: 
        User = register()
        if User != None:
            menu(User) 
        else: 
            sys.exit("Usuario nao autenticado")  
 

if __name__ == '__main__':
    init()
