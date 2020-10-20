import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tempfile import NamedTemporaryFile

import csv
import shutil

from win32api import GetSystemMetrics

weight=GetSystemMetrics(0)
hight=GetSystemMetrics(1)

LARGE_FONT = ("Verdana", 12)



class Main(tk.Tk):#Main part which controls and init the other pages

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "GUI")#title
        #size
        self.minsize(weight,hight)

        #main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.place(x=weight/2.5,y=hight/3)
        self.frames = {}


        #init the page
        for F in (Main_page,Parameter):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #first to show
        self.show_frame(Main_page)

    def show_frame(self, cont):#function to put a page in front
        frame = self.frames[cont]
        frame.tkraise()


class Parameter(tk.Frame):

    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Que voulez vous changer", font=LARGE_FONT).grid(row=1, column=0, pady=10, padx=10)
        # Selector
        OptionList = [
            "Grab",
            "Drop",
            "Main",
            "Pin"
        ]
        self.var = tk.StringVar(self)
        self.var.set("Grab")  # initial value

        option = tk.OptionMenu(self, self.var, *OptionList).grid(row=1, column=2)
        button = ttk.Button(self, text="Changer ce paramètre",
                            command=self.change).grid(row=1, column=3)
        button2 = ttk.Button(self, text="retour",
                            command=self.retour).grid(row=4, column=1)
    def change(self):
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            OptionList2 = []


            for row in reader:
                if row["Class"]==self.var.get() :
                    OptionList2.append(row["Nom"])
                    self.variable=row["valeur"]
            self.var2 = tk.StringVar(self)
            self.var2.set(OptionList2[0])  # initial value
            option = tk.OptionMenu(self, self.var2, *OptionList2).grid(row=2, column=2)
            button2 = ttk.Button(self, text="Changer cette variable",
                                command=self.change2).grid(row=2, column=3)


    def change2(self):
        with open('value.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            OptionList2 = []

            for row in reader:
                if row["Class"] == self.var.get() and row["Nom"]==self.var2.get():
                    self.variable = row["valeur"]
        self.value_texte = tk.StringVar()
        self.value_texte.set(self.variable)
        label = tk.Label(self, text="changer", font=LARGE_FONT).grid(row=3, column=1, pady=10, padx=10)

        entry2 = tk.Entry(self, textvariable=self.value_texte).grid(row=3, column=2)
        button2 = ttk.Button(self, text="OK",
                             command=self.valider).grid(row=3, column=3)
    def valider(self):
        filename = 'value.csv'
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        fields = ['Class', 'Nom', 'valeur']

        with open(filename, 'r') as csvfile, tempfile:

            reader = csv.DictReader(csvfile, fieldnames=fields)
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            for row in reader:
                if row["Class"] ==self.var.get():
                    if row["Nom"] ==self.var2.get():
                        row['Class'], row['Nom'], row['valeur'] = self.var.get(), self.var2.get(), self.value_texte.get()
                row2 = {'Class': row['Class'], 'Nom': row['Nom'], 'valeur': row['valeur']}

                writer.writerow(row2)
        shutil.move(tempfile.name, filename)

        label1 = tk.Label(self, text="Done", font=LARGE_FONT).grid(row=4, column=2, pady=10, padx=10)


    def retour(self):
        self.controller.show_frame(Main_page)
class Main_page(tk.Frame):#Page for the login

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller

        #text
        label = tk.Label(self, text="Selectionez votre côté", font=LARGE_FONT).grid(row=1, column=0, pady=10, padx=10)
        #Selector
        OptionList = [
            "Droit",
            "Gauche"
        ]
        self.var_side = tk.StringVar(self)
        self.var_side.set("Droit")  # initial value

        option = tk.OptionMenu(self, self.var_side,*OptionList).grid(row=1, column=2)
        #text
        label1 = tk.Label(self, text="Selectionez la première couleur", font=LARGE_FONT).grid(row=2, column=0, pady=10, padx=10)
        OptionList2 = [
            "Rouge",
            "Vert"
        ]
        self.var_col = tk.StringVar(self)
        self.var_col.set("Rouge")  # initial value
        option2 = tk.OptionMenu(self, self.var_col,*OptionList2).grid(row=2, column=2)
        ttk.Button(self, text="ok", command=self.quit).grid(row=3, column=3)


        button = ttk.Button(self, text="Changer les paramètres",
                            command=self.go_parameter).grid(row=3, column=2)
    def go_parameter(self):
        self.controller.show_frame(Parameter)
    def quit(self):  # functio to destroy
        global main,value_side,value_color
        value_side=self.var_side.get()
        value_color=self.var_col.get()
        print(self.var_col.get(),self.var_side.get())

        main.destroy()

value_color=""
value_side=""

main = Main()
main.mainloop()
change=False
if value_side=="Droit" :
    number=2
    number2=1
else :
    number=1
    number2=1

filename = 'value.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)
fields = ['Class', 'Nom', 'valeur']

with open(filename, 'r') as csvfile, tempfile:

    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    for row in reader:
        if row["Class"] == 'Grab'+str(number):
            change=True
    if change==True :
        for row in reader:
            if row["Class"] == 'Grab':
                row['Class'], row['Nom'], row['valeur'] = "Grab"+str(number2), row['Nom'], row['valeur']
            row2 = {'Class': row['Class'], 'Nom': row['Nom'], 'valeur': row['valeur']}

            writer.writerow(row2)
        for row in reader:
            if row["Class"] == 'Grab'+str(number):
                row['Class'], row['Nom'], row['valeur'] = "Grab", row['Nom'], row['valeur']
            row2 = {'Class': row['Class'], 'Nom': row['Nom'], 'valeur': row['valeur']}

            writer.writerow(row2)
        shutil.move(tempfile.name, filename)




