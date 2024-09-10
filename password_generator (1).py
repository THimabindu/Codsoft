import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3


with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()


class GUI:
    def __init__(self, master):
        self.master = master
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()
        
        self.master.title('Password Generator')
        self.master.geometry('660x500')
        self.master.config(bg='#FF8000')
        self.master.resizable(False, False)

        self.label = Label(master, text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline')
        self.label.grid(row=0, column=1, pady=(10, 10))

        self.user = Label(master, text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.user.grid(row=1, column=0, pady=(10, 0))
        self.textfield = Entry(master, textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=1, column=1)
        self.textfield.focus_set()

        self.length = Label(master, text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.length.grid(row=2, column=0, pady=(10, 0))
        self.length_textfield = Entry(master, textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=2, column=1)

        self.generated_password = Label(master, text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.generated_password.grid(row=3, column=0, pady=(10, 0))
        self.generated_password_textfield = Entry(master, textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#DC143C')
        self.generated_password_textfield.grid(row=3, column=1)

        self.generate = Button(master, text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_pass)
        self.generate.grid(row=4, column=1, pady=(10, 0))

        self.accept = Button(master, text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields)
        self.accept.grid(row=5, column=1, pady=(10, 0))

        self.reset = Button(master, text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields)
        self.reset.grid(row=6, column=1, pady=(10, 0))

    def generate_pass(self):
        name = self.textfield.get().strip()
        length = self.length_textfield.get().strip()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must contain only alphabets")
            self.textfield.delete(0, END)
            return

        try:
            length = int(length)
        except ValueError:
            messagebox.showerror("Error", "Password length must be an integer")
            self.length_textfield.delete(0, END)
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.length_textfield.delete(0, END)
            return

        upper = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        chars = list("@#%&()\"?!")
        numbers = list(string.digits)

        # Password generation logic
        password = random.sample(upper, 1) + random.sample(lower, 1) + random.sample(chars, 1) + random.sample(numbers, 1)
        if length > 4:
            password += random.sample(upper + lower + chars + numbers, length - 4)
        
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_textfield.delete(0, END)
        self.generated_password_textfield.insert(0, gen_passwd)

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                insert = ("INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)")
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success", "Password generated and saved successfully")

    def reset_fields(self):
        self.textfield.delete(0, END)
        self.length_textfield.delete(0, END)
        self.generated_password_textfield.delete(0, END)


if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()

