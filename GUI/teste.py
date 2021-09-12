from tkinter import *  

def registerUtil(): 
    usernameInfo = username.get() 
    emailInfo = email.get()
    passwordInfo = password.get() 
    
    print(emailInfo)
    print(usernameInfo) 
    print(passwordInfo)   

    Email_entry.delete(0, END)
    username_entry.delete(0, END) 
    password_entry.delete(0, END) 

    Result = Label(screen1, text = "Registro com sucesso", fg ="green").pack()
    #Result.delete(0,END) 



def register(): 
    print("register") 
    global screen1  
    screen1 = Toplevel(screen) 
    screen1.title("Register") 
    screen1.geometry("500x500") 
    Label(text = "").pack() 

    global username    
    global password     
    global email
    global username_entry 
    global password_entry 
    global Email_entry
    
    email = StringVar()
    username = StringVar()  
    password = StringVar()   

  

    Label(screen1,text = "Entre com os dados abaixo").pack() 
    # nome 
    Label(screen1, text= "").pack()
    Label(screen1, text = "Nome *").pack() 
    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack() 
    # email  
    Label(screen1,text = "").pack()  
    Label(screen1,text = "Email * ").pack()  
    Email_entry = Entry(screen1,textvariable = email) 
    Email_entry.pack() 
    # senha 

    Label(screen1,text = "Password * ").pack()  
    password_entry = Entry(screen1, textvariable = password) 
    password_entry.pack()  
    Label(screen1,text = "").pack()    
    Button(screen1, text = "Register",width="30", height="2",command = registerUtil).pack()  
   



def loginUtil():  
    emailInfo = Lemail.get()
    passwordInfo = Lpassword.get() 
    
    print("Login")
    print(emailInfo)
    print(passwordInfo)   

    LEmail_entry.delete(0, END)
    Lpassword_entry.delete(0, END) 

    Result = Label(screen2, text = "Login com sucesso", fg ="green").pack()
    #Result.delete(0,END) 



def login():  
    print("register") 
    global screen2  
    screen2 = Toplevel(screen) 
    screen2.title("Login") 
    screen2.geometry("500x500") 
    Label(text = "").pack() 
    
    global Lpassword     
    global Lemail 
    global Lpassword_entry 
    global LEmail_entry
    
    Lemail = StringVar()
    Lpassword = StringVar()   

  

    Label(screen2,text = "Entre com os dados abaixo").pack() 
    # nome 
    # email  
    Label(screen2,text = "").pack()  
    Label(screen2,text = "Email * ").pack()  
    LEmail_entry = Entry(screen2,textvariable = Lemail) 
    LEmail_entry.pack() 
    # senha 

    Label(screen2,text = "Password * ").pack()  
    Lpassword_entry = Entry(screen2, textvariable = Lpassword) 
    Lpassword_entry.pack()  
    Label(screen2,text = "").pack()    
    Button(screen2, text = "Login",width="30", height="2",command = loginUtil).pack()  
   

def  main_screen(): 
    global screen  
    screen = Tk() 
    screen.geometry("500x500") 
    screen.title("Notes 1.0") 
    Label(text = "Notes 1.0", bg="grey", width="500", height="2" ,font = ("Calibri", 18)).pack() 
    Label(text = "").pack()
    Button(text = "Login",width="30", height="2", command = login).pack()  
    Button(text = "").pack() 
    Button(text = "Register",width="30", height="2",command = register).pack()  
    
    screen.mainloop()

main_screen()