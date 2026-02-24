import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as tsd
from functools import partial
from time import sleep
from pathlib import Path

selfpath = Path().resolve()

if(selfpath/"info.yummy" not in (selfpath).iterdir()):
    jank = open("info.yummy","w")
    knaj = open(selfpath/"info.yum")
    jank.write(knaj.read())
    jank.close()
    knaj.close()
    (selfpath/"info.yum").unlink()
    print("check indent")
    (selfpath.parent/"saves"/"default").mkdir()

storage = open(selfpath/"info.yummy")
halfway = storage.read().split(",\n")
data = dict(item.split(": ") for item in halfway)
storage.close()
erstring = "paste the path to your appdata copy of the saves for this game\nIt prolly looks like ~/.renpy/NAME OF RENPY GAME PLUS A BUNCH OF NUMBERS HERE\nThis is much nicer than the windows version"
while(data['pathdata']=="I don't know, that's scary"):
    pappdatath = tsd.askstring("Wheres appdata", erstring)
    if(os.path.exists(pappdatath)):
        data['pathdata'] = Path(pappdatath)
        os.makedirs(data['pathdata']/"default")

    else:
        erstring = "python says that directory doesn't exist\nIt prolly looks like ~/.renpy/NAME OF RENPY GAME PLUS A BUNCH OF NUMBERS HERE"
del erstring
data['pathdata'] = Path(data['pathdata'])
orcpath = [selfpath.parent/"saves",data['pathdata']]

data["profiles"]=data['profiles'][1:-1].replace("'",'').split(", ")


def changeactive(activechanged):   
    changeto=activechanged.get()
    if(data['active']==changeto):
        return()
    throbber = tk.Toplevel()
    throbber.configure(bg="#000000",width=300,height=80)
    thext = tk.StringVar()
    thext.set("Moving files...\nDon't have a gif because python is mean :(")
    lapel = tk.Label(throbber,
            textvariable=thext,
            bg="#00ff99")
    lapel.place(x=10,y=25)

    # throbbers = os.listdir("./throbbers")
    # random.shuffle(throbbers)
    # infoe = Image.open("./throbbers/"+throbbers[0])
    # frames = infoe.n_frames
    # photoimage_objects=[]
    # for i in range(frames):
    #     obj = tk.PhotoImage(file ="./throbbers/"+throbbers[0],format=f"gif -index {i}")
    #     photoimage_objects.append(obj   )
    
    # gif_label =tk.Label(throbber,image="")
    # gif_label.place(x=100,y=100)
    # def animation(current_frame=0):
    #     global loop
    #     image = photoimage_objects[current_frame]

    #     gif_label.configure(image = image)
    #     current_frame = current_frame + 1

    #     if current_frame == frames:
    #         current_frame = 0 # reset the current_frame to 0 when end is reached

    #     loop = root.after(50, lambda: animation(current_frame))
    # animation()



    throbber.update()
    putFilesAway()
    takeFilesOut(changeto)
    sleep(2)
    throbber.destroy()

    data['active'] = changeto

def putFilesAway():
    for elfpath in orcpath:

        flies = elfpath.iterdir()
        persist=False
        for fly in flies:
            if fly.suffix==".save":
                (fly).rename(elfpath/data["active"]/fly.name)
            if fly.suffix==".Σ":
                persist=True
        if(persist):
            (elfpath/"persistent").rename(elfpath/data["active"]/"persistent")
            (elfpath/"persistent.Σ").rename(elfpath/"persistent")

def takeFilesOut(folder):
    for elfpath in orcpath:
        flies = (elfpath/folder).iterdir()
        for fly in flies:
            if(fly.name=="persistent"):
                (elfpath/"persistent").rename(elfpath/"persistent.Σ")
            (fly).rename(elfpath/fly.name)    

def makeprof(name,persistent,top="Don't worry about it"):

    ame = name()
    ersistent = persistent()
    for elfpath in orcpath:
        try:
            Path(elfpath/ame).mkdir()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("something went wrong","Probalbly the name for your profile already exits or is an invalid file name")
            return()
        if(ersistent):
            pers = open(elfpath/ame/"persistent","w")
            pers.close()
            
    data['profiles'].append(ame)
    
    if __name__=="__main__":
       top.destroy()

def unmakeprof(name):
    ame = name()
    data["profiles"].pop(data["profiles"].index(ame))

def addprof():
    top = tk.Toplevel()
    top.configure(bg="#000000",width=300,height=100)
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
            command=partial(makeprof,lambda:name.get(),lambda:pers.get(),top),
            bg="#00ff99",
            activebackground="#ff004f")
    persistent.place(x=95,y=15)
    ent.place(x=90,y=50)
    out.place(x=10,y=30)

root = tk.Tk(screenName=None, baseName=None, className='Tk')
root.configure(bg="#000000",width=280,height=250)

add = tk.Button(root,
                text ="add new profile",
                width=15,
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
fieldbackground=[("readonly","#00ff99")],
selectbackground=[("readonly","#00ff99")],
selectforeground=[("readonly","#000000")])

activeprof = tk.StringVar(root)
proflies = ttk.Combobox(root,values=data['profiles'],
            textvariable=activeprof,
            width=12,
            style="ad.TCombobox",
            postcommand=lambda: proflies.configure(values=data['profiles']),
            state="readonly")

proflies.current(data['profiles'].index(data['active']))

change = tk.Button(root,
                   text="change active profile",
                   command= partial(changeactive,activeprof),
                   width=15,
                   bg="#ff004f",
                   activebackground="#00ff99")

change.place(x=10,y=15)
proflies.place(x=160,y=30)

# input("?")
# a ="a: 1, b: 2"

root.mainloop()
storage = open(selfpath/"info.yummy","w")
storage.write(f"pathdata: {data['pathdata']},\nprofiles: {data['profiles']},\nactive: {data['active']}")
storage.close()
