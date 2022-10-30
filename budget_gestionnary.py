from tkintertable import *
import tkinter as tk
from tkinter import ttk, filedialog
import os
import sys
import fileinput
import time
from datetime import date
def rgb_to_hex(r,g,b):
    return("#"+"0"*(2-len(hex(r)[2:]))+hex(r)[2:]+"0"*(2-len(hex(g)[2:]))+hex(g)[2:]+"0"*(2-len(hex(b)[2:]))+hex(b)[2:])

#File Loading
user = os.getlogin()
dir = "/home/"+str(user)
os.chdir(dir)
dir = dir + "/.budgetGestionnary"
if not os.path.exists(dir):
    os.system("mkdir .budgetGestionnary ")
os.chdir(dir)
dir = dir + "/.savedata.txt"
if not os.path.exists(dir):
    os.system("touch .savedata.txt")
with open('.savedata.txt') as f:
    lines = f.readlines()
dir = "/home/" + str(user) +"/.budgetGestionnary/.removedMoney"
if not os.path.exists(dir):
    os.system("mkdir .removedMoney")
os.chdir(dir)
dir = dir + "/.removedMoney.txt"
if not os.path.exists(dir):
    os.system("touch .removedMoney.txt")
with open('.removedMoney.txt') as f:
    lines2 = f.readlines()
currentMoney = 0
def str_to_list(arg):
    arg = arg.split()
    return arg
def list_to_string(arg):
    strl1 = ""
    for ele in arg:
        strl1 += str(ele) + " "
    return strl1
moneyComingCategory = lines[0]
moneyComingCategory = str_to_list(moneyComingCategory)
moneyAvailableComingCategory = lines[1]
moneyAvailableComingCategory = str_to_list(moneyAvailableComingCategory)
moneyAvailableComingCategory = [eval(i) for i in moneyAvailableComingCategory]
removedMoney =[]
for i in lines2:
    removedMoney.append(str_to_list(i))
#Rewrite the RemovedMoney list in order to add spaces for the argument: transform [[Date,Category,Money,a,b,c]] into [[Date,Category,Money,a b c]]
try:
    for k in removedMoney:
        tempList = []
        for i in range(4):
            if i <= 1:
                tempList.append(k[i])
            elif i == 2:
                tempList.append(str(k[i]+" €"))
            else:
                l = ""
                for v in range(3,len(k)):
                    l += k[v] + " "
                    tempList.append(l)
        removedMoney[removedMoney.index(k)] = tempList
except:
    None

root = tk.Tk()
root.resizable(True,True)
root.title("budgetGestionnary.th")
root.minsize(600,400)
root.config(background=(rgb_to_hex(100,100,100)))

space = "                                                                                                                                                                                                                        "
#Table for the actual money

def reload_treeview(list):
    actualMoney.delete(*actualMoney.get_children())
    for row in list:
        actualMoney.insert("", "end", values=row)
def reloadRemovedMoney(list):
    removedMoneyTree.delete(*removedMoneyTree.get_children())
    for row in list:
        removedMoneyTree.insert("", "end", values=row)
actualMoneyList = []
total = 0
for i in range(len(moneyComingCategory)):
    tempList = []
    tempList.append(moneyComingCategory[i])
    tempList.append(str(moneyAvailableComingCategory[i])+" €")
    total += moneyAvailableComingCategory[i]
    actualMoneyList.append(tempList)
actualMoneyList.append(["TOTAL",str(total) + " €"])

actualMoneyFrame = tk.LabelFrame(root, text="                    ActualMoney                    ")
actualMoneyFrame.grid(padx=30,pady=30 ,ipady=60,row =0)
actualMoneyFrame.config(background=(rgb_to_hex(100,100,100)),bd = 3)

actualMoney = ttk.Treeview(actualMoneyFrame)  # This is tmaphe Treeview Widget

column_list_account = ["Category", "Money"]  # These are our headings
actualMoney['columns'] = column_list_account  # We assign the column list to the widgets columns
actualMoney["show"] = "headings"  # this hides the default column.

for column in column_list_account:  # foreach column
    actualMoney.heading(column, text=column)  # let the column heading = column name
    actualMoney.column(column, width=50)  # set the columns size to 50px

actualMoney.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (actualMoneyFrame).
treescroll = tk.Scrollbar(actualMoneyFrame)  # create a scrollbar
treescroll.configure(command=actualMoney.yview)  # make it vertical
actualMoney.configure(yscrollcommand=treescroll.set)  # assign the scrollbar to the Treeview Widget
treescroll.pack(side="right", fill="y")  # make the scrollbar fill the yaxis of the Treeview widget

reload_treeview(actualMoneyList)

removedMoneyFrame = tk.LabelFrame(root, text="                 RemovedMoneyHistory                       ")
removedMoneyFrame.grid(padx=30,pady=30 ,ipady=60,column =1,row = 0)
removedMoneyFrame.config(background=(rgb_to_hex(100,100,100)),bd = 3)

removedMoneyTree = ttk.Treeview(removedMoneyFrame)  # This is tmaphe Treeview Widget

column_list_account = ["Date", "Category","Money","Cause"]  # These are our headings
removedMoneyTree['columns'] = column_list_account  # We assign the column list to the widgets columns
removedMoneyTree["show"] = "headings"  # this hides the default column.

for column in column_list_account:  # foreach column
    removedMoneyTree.heading(column, text=column)  # let the column heading = column name
    removedMoneyTree.column(column, width=50)  # set the columns size to 50px

removedMoneyTree.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (actualMoneyFrame).
treescrollY = tk.Scrollbar(removedMoneyFrame)  # create a scrollbar
treescrollY.configure(command=removedMoneyTree.yview)  # make it vertical
removedMoneyTree.configure(yscrollcommand=treescrollY.set)  # assign the scrollbar to the Treeview Widget
treescrollY.pack(side="right", fill="y")  # make the scrollbar fill the yaxis of the Treeview widget
treescrollX = tk.Scrollbar(removedMoneyFrame, orient = HORIZONTAL)  # create a scrollbar
treescrollX.configure(command=removedMoneyTree.xview)  # make it vertical
removedMoneyTree.configure(xscrollcommand=treescrollX.set)  # assign the scrollbar to the Treeview Widget
treescrollX.pack(side="bottom", fill="x")  # make the scrollbar fill the yaxis of the Treeview widget


removedMoneyTree.delete(*removedMoneyTree.get_children())
for row in removedMoney:
    removedMoneyTree.insert("", "end", values=row)

def saveRemovedMoney(list):
    dir = "/home/" + str(user) +"/.budgetGestionnary/.removedMoney"
    os.chdir(dir)
    with open(".removedMoney.txt","a") as file:
        file.write(list_to_string(list)+os.linesep)

#Dropdown to remove some money
clicked = StringVar()
clicked.set(moneyComingCategory[0])

moneyRemoveDropdown = tk.OptionMenu(root, clicked, *moneyComingCategory)
moneyRemoveDropdown.place(x=350,y=231)
var = tk.StringVar()
var2 = tk.StringVar()
digitsEntry = tk.Entry(root,textvariable=var)
digitsEntry.place(x=470,y=231,height = 33,width=30)
causeEntry = tk.Entry(root,textvariable = var2)
causeEntry.place(x=510,y=231,height = 33, width = 100)
def onClick():
    try:
        moneyToRemove = float(var.get())
        position = moneyComingCategory.index(clicked.get())
        moneyAvailableComingCategory[position] -= moneyToRemove

        actualMoneyList = []
        total = 0
        for i in range(len(moneyComingCategory)):
            tempList = []
            tempList.append(moneyComingCategory[i])
            tempList.append(str(moneyAvailableComingCategory[i])+" €")
            total += moneyAvailableComingCategory[i]
            actualMoneyList.append(tempList)
        actualMoneyList.append(["TOTAL",str(total) + " €"])
        reload_treeview(actualMoneyList)
        errorLabel = tk.Label(root,text=str(space))
        errorLabel.config(bg=rgb_to_hex(100,100,100))
        errorLabel.place(x=30,y=270)
        removedMoney.append([date.today(),clicked.get(),str(moneyToRemove) + " €",var2.get()])
        reloadRemovedMoney(removedMoney)
        saveRemovedMoney([date.today(),clicked.get(),moneyToRemove,var2.get()])
        time.sleep(1)
    except:
        errorLabel = tk.Label(root,text="Error: "+str(var.get())+" is not a number(euro.cents)"+str(space))
        errorLabel.config(bg=rgb_to_hex(100,100,100),fg=rgb_to_hex(255,0,0))
        errorLabel.place(x=30,y=270)
remove_button = Button(
    root,
    text="Remove",
    command = onClick
    )

remove_button.place(x=620,y=231,height = 33)



#Save the file when the window is closed
def save():
    dir = "/home/" + str(user) +"/.budgetGestionnary/"
    os.chdir(dir)
    file =open(".savedata.txt","a")
    l1 = list_to_string(moneyComingCategory)
    l2 = list_to_string(moneyAvailableComingCategory)
    file.writelines([l1+os.linesep, l2+os.linesep])

def on_closing():
    dir = "/home/" + str(user) +"/.budgetGestionnary/"
    os.chdir(dir)
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        f = open(".savedata.txt", "r+")
        # absolute file positioning
        f.seek(0)
        # to erase all data
        f.truncate()
    root.destroy()
    save()
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
