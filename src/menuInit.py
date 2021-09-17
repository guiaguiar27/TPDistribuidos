from collector import collector 

def login(): 
    name = str(input("User:")) 
    password = str(input("Password:")) 
        #collector =  vai receber infos do bd 
    # precisa do acesso ao bd
    User = None 
    if User != None: 
        return 1 
    else: 
        return 0 

def register(): 
    user = str(input("User:")) 
    email = str(input("Email: ")) 
    password = str(input("Password"))
    NewUser = collector() 
    NewUser.NewUser(email, password,user) 
    #NewUser.show_collector()  
    if NewUser: 
        return 1 
    else: 
        return 0 

# pagina de acesso do usuario 
def menu(): 
    print("---------------MENU------------------") 
    
#pagina inicial
def init(): 
    print("Entre com 1 para login ou 2 para cadastro:") 
    First = int(input()) 
    if First == 1: 
        if login() == 1 : 
            menu()  
        else: 
            print("Login invalido") 
            init()

    else:
        if register() == 1: 
            menu() 
        else: 
            sys.exit("Usuario nao autenticado")  
 

if __name__ == '__main__':
    init()
