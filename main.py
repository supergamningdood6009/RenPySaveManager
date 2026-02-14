import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as tsd
from functools import partial

selfpath = os.path.abspath(__file__)[:-7]

if("info.yummy" not in os.listdir(selfpath)):
    jank = open("info.yummy","w")
    knaj = open(selfpath+"info.yum")
    jank.write(knaj.read())
    jank.close()
    knaj.close()
    os.remove(selfpath+"info.yum")
    os.makedirs(selfpath[:-17]+"saves\\default")

storage = open(selfpath+"info.yummy")
halfway = storage.read().split(",\n")
data = dict(item.split(": ") for item in halfway)
storage.close()

erstring = "paste the path to your appdata copy of the saves for this game\nIt prolly looks like C:\\Users\\YOUR USER HERE\\AppData\\Roaming\\RenPy\\NAME OF RENPY GAME PLUS A BUNCH OF NUMBERS HERE"
while(data['pathdata']=="I don't know, that's scary"):
    pappdatath = tsd.askstring("Wheres appdata", erstring)
    if pappdatath[-1] != "\\":
        pappdatath.append("\\")
    if(os.path.exists(pappdatath)):
        data['pathdata'] = pappdatath
            os.makedirs(pappdatath+"\\default")

    else:
        erstring = "python says that directory doesn't exist\nIt prolly looks like C:\\Users\\YOUR USER HERE\\AppData\\Roaming\\RenPy\\NAME OF RENPY GAME PLUS A BUNCH OF NUMBERS HERE"
del erstring

orcpath = [selfpath[:-17]+"saves\\",data['pathdata']]

data["profiles"]=data['profiles'][1:-1].replace("'",'').split(", ")


def changeactive(activechanged):   
    changeto=activechanged.get()
    if(data['active']==changeto):
        return()
    
    putFilesAway()
    takeFilesOut(changeto)

    data['active'] = changeto

    data['profiles'].index(data['active'])
    #proflies.current(data['profiles'].index(data['active']))

def putFilesAway():
    for elfpath in orcpath:

        flies = os.listdir(elfpath)
        for fly in flies:
            if not fly in data['profiles']:
                os.rename(elfpath+fly,elfpath+data["active"]+"\\"+fly)

def takeFilesOut(folder):
    for elfpath in orcpath:
        flies = os.listdir(elfpath+folder)
        for fly in flies:
                os.rename(elfpath+folder+"\\"+fly,elfpath+fly)    

def makeprof(name,persistent,top):
    for elfpath in orcpath:
        try:
            os.makedirs(elfpath+name.get())
        except Exception as e:
            print(e)
            tk.messagebox.showerror("something went wrong","Probalbly the name for your profile already exits or is an invalid file name")
            return()
        if(not persistent.get()):
            shutil.copy2(elfpath+"persistent",elfpath+name.get()+"\\persistent")
    data['profiles'].append(name.get())
    
    top.destroy()

def addprof():
    top = tk.Toplevel()
    top.configure(bg="#000000",width=210,height=100)
    pers = tk.BooleanVar(top)
    name = tk.StringVar(top)
    ent=tk.Entry(top,
            textvariable = name,
            width=22,
            bg="#ff004f")

    persistent = tk.Checkbutton(top,
            text="New persistent data?",
            variable = pers,
            bg="#ff004f",
            activebackground="#00ff99")

    out = tk.Button(top, 
            text ="done",
            width=5,
            command=partial(makeprof,name,pers,top),
            bg="#00ff99",
            activebackground="#ff004f")
    persistent.place(x=60,y=15)
    ent.place(x=60,y=50)
    out.place(x=10,y=30)

root = tk.Tk(screenName=None, baseName=None, className='Tk')
root.configure(bg="#000000",width=250,height=250)

add = tk.Button(root,
                text ="add new profile",
                width=16,
                height=1,
                command=addprof,
                bg= "#ff004f",
                activebackground="#00ff99")
add.place(x=10,y=45)

adnasty = ttk.Style()
adnasty.theme_use("clam")

adnasty.configure("ad.TCombobox",
                  fieldbackground="#00ff99",
                  background="#000000",
                  bordercolor="#ff004f",
                  lightcolor="#ff004f",
                  darkcolor="#ff004f",
                  arrowcolor="#ff004f",
                  borderwidth=2,
                  relief="solid")

root.option_add("*TCombobox*Listbox.background", "#00ff99")
root.option_add("*TCombobox*Listbox.foreground", "#000000")
root.option_add("*TCombobox*Listbox.selectBackground", "#11eeaa")
root.option_add("*TCombobox*Listbox.selectForeground", "#000000")

adnasty.map('ad.TCombobox',
fieldbackground=[("readonly","#00ff99")])

activeprof = tk.StringVar(root)
proflies = ttk.Combobox(root,values=data['profiles'],
            textvariable=activeprof,
            width=14,
            style="ad.TCombobox",
            postcommand=lambda: proflies.configure(values=data['profiles']),
            state="readonly")

proflies.current(data['profiles'].index(data['active']))

change = tk.Button(root,
                   text="change active profile",
                   command= partial(changeactive,activeprof),
                   bg="#ff004f",
                   activebackground="#00ff99")

change.place(x=10,y=15)
proflies.place(x=137,y=30)

# input("?")
# a ="a: 1, b: 2"

root.mainloop()
storage = open(selfpath+"info.yummy","w")
storage.write(f'pathdata: {data['pathdata']},\nprofiles: {data['profiles']},\nactive: {data['active']}')
storage.close()




