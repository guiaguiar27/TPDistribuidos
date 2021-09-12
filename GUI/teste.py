from tkinter import *  

def registerUtil(): 
    usernameInfo = username.get() 
    passwordInfo = password.get() 
    print(usernameInfo) 
    print(passwordInfo)

def register(): 
    print("register")  
    screen1 = Toplevel(screen) 
    screen1.title("Register") 
    screen1.geometry("500x250") 
    Label(text = "").pack() 

    global username    
    global password   
    
    username = StringVar()  
    password = StringVar()  
  

    Label(screen1,text = "Entre com os dados abaixo").pack()  
    Label(screen1,text = "").pack()  
    Label(screen1,text = "Email * ").pack()  
    Entry(screen1,textvariable = username).pack() 
    Label(screen1,text = "Password * ").pack()  
    Entry(screen1, textvariable = password).pack()  
    Label(screen1,text = "").pack()    
    Button(screen1, text = "Register",width="30", height="2",command = registerUtil).pack()  
   




def login(): 
    print("login")

def  main_screen(): 
    global screen  
    screen = Tk() 
    screen.geometry("500x250") 
    screen.title("Notes 1.0") 
    Label(text = "Notes 1.0", bg="grey", width="500", height="2" ,font = ("Calibri", 18)).pack() 
    Label(text = "").pack()
    Button(text = "Login",width="30", height="2", command = login).pack()  
    Button(text = "").pack() 
    Button(text = "Register",width="30", height="2",command = register).pack()  
    
    screen.mainloop()

main_screen()