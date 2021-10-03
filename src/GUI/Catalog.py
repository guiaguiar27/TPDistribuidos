from tkinter import *  
from PIL import Image, ImageTk 
def printf(): 
    print("asdfasdf")


# otimizar essa funcao esta printando uma carta embaixo da outra 
def infoCard(): 
     pass
def catalog():  
    
    root = Tk()
    root.geometry("500x500") 
    Label(root,text = "Exemplo de catalogo").pack()  
    Label(root,text = "").pack() 
    

    image = Image.open("1.png")
    image = image.resize((100, 100), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    imagetest = ImageTk.PhotoImage(image) 

    button_qwer = Button(root, text="House Bulwer", width=100, height=100,image=imagetest, command = printf)
    button_qwer.pack() 
    button_qwer.place(x= 100, y = 30)  

    image = Image.open("2.png")
    image = image.resize((100, 100), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    imagetest2 = ImageTk.PhotoImage(image) 

    button_qwer = Button(root, text="House Bulwer", width=100, height=100,image=imagetest2, command = printf)
    button_qwer.pack() 
    button_qwer.place(x = 300, y = 30)  

    image = Image.open("3.png")
    image = image.resize((100, 100), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    imagetest3 = ImageTk.PhotoImage(image) 
    
    button_qwer = Button(root, text="House Bulwer", width=100, height=100,image=imagetest3, command = printf)
    button_qwer.pack() 
    button_qwer.place(x= 100, y = 230)  

    image = Image.open("4.png")
    image = image.resize((100, 100), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    imagetest4 = ImageTk.PhotoImage(image) 

    button_qwer = Button(root, text="House Bulwer", width=100, height=100,image=imagetest4, command = printf)
    button_qwer.pack()  
    button_qwer.place(x= 300, y = 230)
    root.mainloop() 


catalog()