from tkinter import *
from tkinter import ttk
import sqlite3
from random import randint

class aplication(object):
    def __init__(self, tk):

        self.label1 = Label(tk, text='Formulario de senhas', background='#dde')
        self.label1.place(x=80, y= 10)

        self.label2= Label(tk, text='Site', background='#dde', foreground='#009', anchor='w')
        self.label2.place(x=30, y=75 , width=100, height=20)

        self.site = Entry(tk)
        self.site.place(x=70, y=75, width= 200, height=20)

        self.label3 = Label(tk, text='Senha', background='#dde', foreground='#009', anchor='w')
        self.label3.place(x=25, y=100, width=100, height=20)
   
        self.senha = Entry(tk)
        self.senha.place(x=70, y=100, width= 200, height=20)

        self.botao = Button(tk, text='salvar', command=self.write)
        self.botao.place(x=220, y=130, width=40, height=30)

        self.botao1 = Button(tk, text='Banco de senhas', command=self.page_two)
        self.botao1.place(x=120, y=130, width=95, height=30)

        self.data = sqlite3.connect('banco_de_senha.db')
        self.cursor = self.data.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Cadastro(Id INTEGER, Site TEXT NOT NULL, Senha INTEGER NOT NULL) ''')


    def write(self):
        Id = randint(0,1000)
        site_text = self.site.get()
        senha_text = self.senha.get()
        if site_text != '':
            self.cursor.execute('''INSERT into Cadastro(Id, Site, Senha) VALUES(?, ?, ?)''', (Id, site_text, senha_text))
            self.data.commit()
            self.data.close()
            self.site.delete(0, END)
            self.senha.delete(0, END)


    def page_two(self):
        tk = Tk()
        tk.geometry('350x263')
        tk.title('lista de senhas')
        tk.configure(background='#dde')
        self.table = ttk.Treeview(tk, columns=('Id', 'Site', 'Senha'), show='headings')
        self.table.column('Id', minwidth=0, width=50)
        self.table.column('Site', minwidth=0, width=150)
        self.table.column('Senha', minwidth=0)
        self.table.heading('Id', text='Id')
        self.table.heading('Site', text='Site')
        self.table.heading('Senha', text='Senha')
        self.table.pack()
        botao = Button(tk, text='deletar', command=self.delete)
        botao.place(x=300, y=230, width=40, height=30)
 
        self.data = sqlite3.connect('banco_de_senha.db')
        self.cursor = self.data.cursor()
        self.cursor.execute("SELECT * FROM Cadastro")
        rows = self.cursor.fetchall()
        for row in rows:
            self.table.insert("", END, values=row)
            self.data.close()

        tk.mainloop()


    def delete(self):
        select_item = self.table.selection()[0]
        value = self.table.item(select_item, 'values')
        Id = value[0]
        data = sqlite3.connect('banco_de_senha.db')
        cursor = data.cursor()
        self.table.delete(select_item)
        cursor.execute('''DELETE FROM Cadastro WHERE Id='''+ Id)
        data.commit()
        data.close()


tk = Tk()
aplication(tk)

tk.title('Banco de senhas')

tk.geometry('290x200')

tk.configure(background='#dde')

tk.mainloop()
