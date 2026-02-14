import os
import tkinter as tk
from tkinter import ttk
from functools import partial
selfpath = os.path.abspath(__file__)[:-7]
print(selfpath)
if("info.yummy" not in os.listdir(selfpath)):
    jank = open("info.yummy","w")
    knaj = open(selfpath+"info.yum")
    jank.write(knaj.read())
    jank.close()
    knaj.close()
    os.remove(selfpath+"info.yum")

selfpath = os.path.abspath(__file__)[:-7]
storage = open(selfpath+"info.yum")
halfway = storage.read().split(",\n")
data = dict(item.split(": ") for item in halfway)
storage.close()
data["profiles"]=data['profiles'][1:-1].replace("'",'').split(", ")
print(data["profiles"])

def changeactive(activechanged):    
    print(activechanged.get())

def makeprof(name,persistent,top):
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
storage = open(selfpath+"info.yum","w")
storage.write(f'pappdatath: {data['pappdatath']},\nprofiles: {data['profiles']}')
storage.close()