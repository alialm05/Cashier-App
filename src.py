from time import sleep
import random
from tkinter import*
#from PySimpleGUI import*
#from easygui import*
from PIL import Image, ImageTk
from fontTools.ttLib import TTFont

# Author :_______ Ali Almaamouri________ #

# -- import a downloade font
#font = TTFont(r"C:\Users\ilikt\OneDrive\Documents\Fonts\grobold\GROBOLD.ttf")
#font.save(file=r"C:\Users\ilikt\OneDrive\Documents\Fonts\grobold\GROBOLD.ttf")
    
Fooditems = {
    "Donut": 2,
    "Bagel": 3,
    "Timbit": 0.5
         }
Drinks = {
    "Smoothie" : 4,
    "Tea": 3.50,
    "Coffee":2.50
}

orderPrice = 0
order = {}
checkingOut = False

window = Tk()
windowSizeX = '1440'
windowSizeY= '1080'
window.geometry(windowSizeX+"x"+windowSizeY)
window.config(t="Cashier Program by Ali Almaamouri")
window.title("Cashier Program by Ali Almaamouri")

windowIcon = PhotoImage(file="cashierIcon.png")
window.iconphoto(False, windowIcon)

#window.attributes('-fullscreen', True)
title = Label(window, text="Cashier Control", font=("GROBOLD", 30),)
title.pack()

menuFrame = Frame(window, bg="#FAFAEB", width=300, height=700)
menuFrame.pack(fill="both", expand=True, side="left")

operationsFrame = Frame(window, bg="#F0F0FF", width=250, height=700)
operationsFrame.pack(fill="both",  side="right")
orderTitle = Label(operationsFrame, text="Current Order:", font=("GROBOLD", 15), width=15)
orderTitle.pack(side="top")

subTotal = Label(operationsFrame, text="Subtotal: "+ str(orderPrice*0.00)+" $", font=("GROBOLD", 14))
Total = Label(operationsFrame, text="Total: "+ str(orderPrice+(orderPrice*0.13))+" $", font=("GROBOLD", 17))
checkoutButton = Button(operationsFrame, text="Check Out", font=("GROBOLD",13), fg="white", activebackground="gray", background="gray63", width=16, height=2, anchor="center",command= lambda: checkOut())
checkoutButton.pack(side="bottom", pady=5)
Total.pack(side="bottom",pady=5)
subTotal.pack(side="bottom", pady=5)

checkOutFrame = Frame(window, bg="#F0F0FF", width=400, height=300)
coFL = Label(checkOutFrame, text="Choose Payment Type", font=("GROBOLD", 10))
coFL.pack(side="top")
debtButton = Button(checkOutFrame, text="Debit/Credit", font=("GROBOLD",12), fg="black", activebackground="forest green", background="lime green", width=14, height=3, anchor="center",command= lambda: debitTransaction())
debtButton.pack(side="top")
cashBtn = Button(checkOutFrame, text="Cash", font=("GROBOLD",12), fg="black", activebackground="forest green", background="lime green", width=14, height=3, anchor="center",command= lambda: cashTransaction())
cashBtn.pack(side="top")
gCBtn = Button(checkOutFrame, text="Gift Card", font=("GROBOLD",12), fg="black", activebackground="forest green", background="lime green", width=14, height=3, anchor="center",command= lambda: gCTransaction())
gCBtn.pack(side="top")

menuSubFrame = Frame(menuFrame, bg="#EEEED5", width=40, height=180)

drinksMenu = Frame(menuFrame, bg="#EEEED5", width=40, height=250)
foodMenu = Frame(menuFrame, bg="#EEEED5", width=40, height=250)

closedMenu = False

buttonWidht = "30"
buttonHeight = "5"

drinksBut = Button(menuSubFrame, text="Drinks", font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center",command=lambda: clickedCategory("Drinks"))
foodBut = Button(menuSubFrame, text="Food", font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center", command=lambda: clickedCategory("Food"))
backButton = Button(menuFrame, text="back", font=("GROBOLD",6), fg="black", activebackground="blue", background="#7F7FFF", width=6, height=3, anchor="center", command= lambda :  ShowMainOptions())

# -- Add Options to the food and drinks menu
buttons = {}

for itemName, itemPrice in Fooditems.items():
    def _addToList(newItem = itemName, newPrice = itemPrice):
        return addToList(newItem, newPrice)
    item = Button(foodMenu, text=itemName, font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center", command=_addToList)
    buttons[itemName] = item
    item.pack(padx=5, pady=5, side="top", fill="both")
    
for  itemName, itemPrice in Drinks.items():
    def _addToList(newItem = itemName, newPrice = itemPrice):
        return addToList(newItem, newPrice)
    item = Button(drinksMenu, text=itemName, font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center", command=_addToList)
    buttons[itemName] = item
    item.pack(padx=5, pady=5, side="top", fill="both")

def getOrderPriceTotal():
    p = orderPrice
    return (round((p+(p*0.13))*10)/10)


def completeOrder(action):
    global orderPrice
    global order
    print("current price: " + str(orderPrice))
    if action == "complete":     
        for i, v in order.items():
            v["Label"].destroy()
        
        orderPrice = 0       
        order = {}
        pop.destroy()
        subTotal.config(text="Subtotal: " +format(0, '.2f'))
        updatePrice(0)

        checkoutButton.config(fg="white", activebackground="gray", background="gray63",)
        ShowMainOptions()
        global checkingOut
        checkingOut = False
        
    else:
        pop.destroy()
        checkOutFrame.place(relx=.5, rely=.4,anchor= CENTER)
        checkOutFrame.focus_set()
        updatePrice(orderPrice)

    
def gCTransaction():
    global CardImage
    CardImage = Image.open("GiftCard.png")
    CardImage = ImageTk.PhotoImage(CardImage)
    gCamount = 15
    checkOutFrame.place_forget()
    
    global orderPrice
    orderPrice = getOrderPriceTotal()
    
    leftOverPrice = orderPrice - gCamount
    
    orderPrice = leftOverPrice
    print("left over price: " + str(orderPrice))

    global pop
    pop = Toplevel(window)
    pop.config(bg="#F0F0FF")
    pop.geometry("500x450")
    pop.title = "Checking Out"
    
    pop_label = Label(pop, text="Customer Has Used A Gift Card as a Payment Method", font=("GROBOLD", 9), width=60)
    pop_label.pack(padx=10, pady=10)
    popImg = Label(pop, image=CardImage)
    popImg.pack(padx=5, pady=5)
    #sleep(1)
    #pop_label.destroy()
    
       
    if leftOverPrice > 0:
        pop_label2 = Label(pop, text="Gift Card Purchase Approved!\n"+ format(leftOverPrice, '.2f')+ " left over needs to be paid" , font=("GROBOLD", 9), width=60)
        pop_label2.pack(padx=10, pady=10)
        Button(pop, text="Continue", command=lambda: completeOrder("incomplete")).pack(padx=10, pady=15)

    else:
        pop_label2 = Label(pop, text="Gift Card Purchase Approved!", font=("GROBOLD", 9), width=60)
        pop_label2.pack(padx=10, pady=10)
        Button(pop, text="Complete", command=lambda: completeOrder("complete")).pack(padx=10, pady=15)




def debitTransaction():
    
    global CardImage
    cardType = random.randint(1,2) == 2 and "Debit" or "Credit"
    rCardImg = Image.open("Card.png")
    rCardImg.resize((150, 150), Image.ADAPTIVE)
    CardImage = ImageTk.PhotoImage(rCardImg)
    checkOutFrame.place_forget()
    
    global pop
    pop = Toplevel(window)
    pop.config(bg="#F0F0FF")
    pop.geometry("500x450")
    pop.title = "Checking Out"
    
    pop_label = Label(pop, text="Customer Has Used A " + cardType +" Card as a payment Method", font=("GROBOLD", 9), width=60)
    pop_label.pack(padx=10, pady=10)
    popImg = Label(pop, image=CardImage)
    popImg.pack(padx=5, pady=5)
    #sleep(1)
    #pop_label.destroy()
    pop_label2 = Label(pop, text="Purchased Approved!", font=("GROBOLD", 9), width=60)
    pop_label2.pack(padx=10, pady=10)
    Button(pop, text="Complete", command=lambda: completeOrder("complete")).pack(padx=10, pady=15)
    #dialogWin1 = buttonbox("Customer Has Used A Debit Card as a payment Method", "Notice", ["Proceed"], image="Card.png",)
    #dialogWin2 = buttonbox("Card Payment Has Been Approved!", "Notice", ["Complete"], image="Card.png",)
    



def cashTransaction():
    bills = [0, 5, 10, 20, 50, 100]
    billUsed = 0
    orderPriceTotal = getOrderPriceTotal()

    global CardImage
    rCardImg = Image.open("Cash.png")
    rCardImg.resize((150, 150), Image.ADAPTIVE)
    CardImage = ImageTk.PhotoImage(rCardImg)
    checkOutFrame.place_forget()
    enteredCash = StringVar()

    global pop
    pop = Toplevel(window)
    pop.config(bg="#F0F0FF")
    pop.geometry("500x450")
    pop.title = "Checking Out"
    popImg = Label(pop, image=CardImage)
    popImg.pack(padx=5, pady=5)
    
    def getChange(p):
        nonlocal pop_label2
        nonlocal enteredCash
        nonlocal orderPriceTotal
        nonlocal b
        
        p = enteredCash.get()
        
        pop_label2.destroy()
        ent.destroy()
        b.destroy()
        print("price: "+ str(p)+", " + str(orderPriceTotal))
        change = int(p) - orderPriceTotal

        pop_label2 = Label(pop, text="You Gave them " + str((format(change, '.2f')))+ " $ in change", font=("GROBOLD", 9), width=60)
        pop_label2.pack(padx=10, pady=10)
        b = Button(pop, text="Complete", command=lambda: completeOrder("complete")).pack(padx=10, pady=15)

    
    for i in range(len(bills)):
        if i+1 > len(bills):
            billUsed = bills[i]
            break
        if orderPriceTotal > bills[i] and orderPriceTotal <= bills[i+1]:
            billUsed = bills[i+1]
            break
    
    
    # dialouge 1
    pop_label = Label(pop, text="Customer Has Used Cash as a payment Method", font=("GROBOLD", 9), width=60)
    pop_label.pack(padx=10, pady=10)

    #sleep(1)
    #pop_label.destroy()
    
    # dialouge 2
        
    pop_label2 = Label(pop, text="The Amount They Paid with: ", font=("GROBOLD", 9), width=60)
    pop_label2.pack(padx=10, pady=10)
    ent = Entry(pop, textvariable=enteredCash,font=("GROBOLD", 9), width=50)
    ent.pack(padx=10, pady=10)
    
    b = Button(pop, text="Proceed", command=lambda: getChange(billUsed))
    b.pack(padx=10, pady=15)
    
    # dialouge 3        

def checkOut():
    checkOutFrame.place(relx=.5, rely=.4,anchor= CENTER)
    checkOutFrame.focus_set()
    global checkingOut
    checkingOut = True
    


def updatePrice(orderPrice):
 
    subTotal.config(text="Subtotal: "+ str(format(orderPrice, '.2f'))+" $")
    Total.config(text="Total: "+ str(format((round((orderPrice+(orderPrice*0.13))*10)/10), '.2f'))+" $")




def ShowMainOptions():
    
    menuSubFrame.pack(padx=25, pady=100, fill="y")
    foodMenu.pack_forget()
    drinksMenu.pack_forget()
    backButton.place_forget()
    


    #drinksBut = Button(menuSubFrame, text="Drinks", font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center",command=clickedCategory)
    drinksBut.pack(padx=15, pady=10, side="left")
    #drinksBut.grid(row=5, column=10, padx=10, pady=10)

    #foodBut = Button(menuSubFrame, text="Food", font=("GROBOLD",12), fg="black", activebackground="blue", background="#7F7FFF", width=buttonWidht, height=buttonHeight, anchor="center", command=clickedCategory)
    foodBut.pack(padx=15, pady=50, side="right")
    #foodBut.grid(row=5, column=11, padx=0, pady=10)


def clickedCategory(category):
    drinksBut.pack_forget()
    foodBut.pack_forget()
    
    buttonWidht = "40"
    buttonHeight = "10"
    backButton.place(x=5,y=25)
    menuSubFrame.pack_forget()
    if category == "Food":
        foodMenu.pack(padx=25, pady=100, fill="y")
    else:
        drinksMenu.pack(padx=25, pady=100, fill="y")


def addToList(itemName, Price):
    
    if checkingOut == True:
        return
    
    alreadyOrdered = False
    itemLabel = None
    global order
        
    if itemName in order:
        order[itemName]["Quantity"] += 1
        num = order[itemName]["Quantity"]
             
        itemLabel = order[itemName]["Label"]
        itemLabel.config(text=itemName+" x"+str(num) + "       "+ str((format(num*Price, '.2f')))+ " $")
        
    else:
        itemLabel = Label(operationsFrame, text=itemName+ "       "+ str((format(Price, '.2f')))+ " $", font=("GROBOLD", 12),)
        itemLabel.pack(side="top", fill="x")
        order[itemName] = {}
        order[itemName]["Label"] = itemLabel
        order[itemName]["Quantity"] = 1
    
    global orderPrice
    orderPrice += Price
    updatePrice(orderPrice)
    print(orderPrice)
    checkoutButton.config(background="lime green", activebackground="forest green")


#menuFrame.bind( '<Configure>', maxsize )

ShowMainOptions()


window.mainloop()