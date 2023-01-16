import tkinter
from tkinter import messagebox, PhotoImage
import customtkinter
from customtkinter import CTkEntry, CTkLabel, CTkButton, CTkFrame
import cryptography
from cryptography.fernet import Fernet
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

#Checking Paths

if os.path.exists("./color_mode.txt"):
    pass
else:
    text = open("./color_mode.txt", "w")
    text.write("Dark")
    text.close()
if os.path.exists("./password_list.mortlist"):
    pass
else:
    text = open("./password_list.mortlist", "w")
    text.write("")
    text.close()
if os.path.exists("./.env"):
    pass
else:
    text = open("./.env", "w")
    text.write("")
    text.close()
    #check for key or generate new one
if os.path.exists("./key.mortkey"):
    pass
else:
    if os.path.exists("./key.mortkey.backup"):
        pass
    else:
        messagebox.showinfo(title="Generating New Key", message="If This Is Your First Time Running This Program Please Ignore This Message. \n\nLast Encryption Key Was Lost Or Deleted, Generating New Key, This Makes Your Old Passwords Unusable.")
        key = Fernet.generate_key()
        keyfile = open("key.mortkey", "wb")
        keyfile.write(key)
        keyfile.close()
        key_backup = open("key.mortkey.backup", "wb")
        key_backup.write(key)
        key_backup.close()

    # restore original from backup
if os.path.exists("./key.mortkey.backup") and os.path.exists("./key.mortkey") == False:
    with open("./key.mortkey.backup", "rb") as the_key:
        key = the_key.read()
        restore = open("key.mortkey", "wb")
        restore.write(key)
        restore.close()
    # create bakcup in case it was deleted
if os.path.exists("./key.mortkey") and os.path.exists("./key.mortkey.backup") == False:
    with open("./key.mortkey", "rb") as the_key:
        key = the_key.read()
        restore = open("key.mortkey.backup", "wb")
        restore.write(key)
        restore.close()

with open("color_mode.txt", 'r') as mode:
    color = mode.read()
    customtkinter.set_appearance_mode(color)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("Password Manager")
app.geometry("600x500")
if os.path.exists("./icon.png"):
    photo = PhotoImage(file = "./icon.png")
    app.iconphoto(False, photo)
else:
    pass
#functions

def encrypt_username(username):
    username = bytes(username, 'utf-8')
    try:
        with open("key.mortkey", "rb") as the_key:
            key = the_key.read()
        encrypted = Fernet(key).encrypt(username)
        encrypted = encrypted.decode('utf-8')
        return encrypted
    except:
        with open("key.mortkey.backup", "rb") as the_key:
            key = the_key.read()
        encrypted = Fernet(key).encrypt(username)
        encrypted = encrypted.decode('utf-8')
        return encrypted

def decrypt_username(username):
    try:
        with open("key.mortkey", "rb") as the_key:
            key = the_key.read()
        username = username.replace("\n", "")
        load_dotenv()
        #the_password = os.environ[f"{username}_password"]
        decrypted = Fernet(key).decrypt(os.environ[f"{username}_username"])
        return decrypted
    except:
        with open("key.mortkey.backup", "rb") as the_key:
            key = the_key.read()
        password = password.replace("\n", "")
        load_dotenv()
        the_password = os.environ[f"{password}_password"]
        decrypted = Fernet(key).decrypt(os.environ[f"{password}_username"])
        return decrypted

def encrypt_pass(password):
    password = bytes(password, 'utf-8')
    try:
        with open("key.mortkey", "rb") as the_key:
            key = the_key.read()
        encrypted = Fernet(key).encrypt(password)
        encrypted = encrypted.decode('utf-8')
        return encrypted
    except:
        with open("key.mortkey.backup", "rb") as the_key:
            key = the_key.read()
        encrypted = Fernet(key).encrypt(password)
        encrypted = encrypted.decode('utf-8')
        return encrypted
        
def decrypt_pass(password):
    try:
        with open("key.mortkey", "rb") as the_key:
            key = the_key.read()
        password = password.replace("\n", "")
        load_dotenv()
        the_password = os.environ[f"{password}_password"]
        decrypted = Fernet(key).decrypt(os.environ[f"{password}_password"])
        return decrypted
    except:
        with open("key.mortkey.backup", "rb") as the_key:
            key = the_key.read()
        password = password.replace("\n", "")
        load_dotenv()
        the_password = os.environ[f"{password}_password"]
        decrypted = Fernet(key).decrypt(os.environ[f"{password}_password"])
        return decrypted

# add new pwd window function 
def new_pwd_window():
    new_pass_window = customtkinter.CTkToplevel(app)
    new_pass_window.geometry("600x500")
    if os.path.exists("./icon.png"):
        photo = PhotoImage(file = "./icon.png")
        new_pass_window.iconphoto(False, photo)
    else:
        pass
    new_pass_window.title("Add New Password")
    pass_name = CTkLabel(new_pass_window, text="Site Name")
    pass_name.place(relx = 0.5, rely=0.1, anchor = tkinter.CENTER)
    name_entry = customtkinter.CTkEntry(master=new_pass_window,
                               placeholder_text="Site Name",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    name_entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
    username = CTkLabel(new_pass_window, text="Username")
    username.place(relx = 0.5, rely=0.3, anchor = tkinter.CENTER)
    username_entry = customtkinter.CTkEntry(master=new_pass_window,
                               placeholder_text="Username",
                               width=200,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    username_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    pass_name = CTkLabel(new_pass_window, text="Password")
    pass_name.place(relx = 0.5, rely=0.5, anchor = tkinter.CENTER)
    pass_entry = customtkinter.CTkEntry(master=new_pass_window,
                               placeholder_text="Password",
                               width=200,
                               height=25,
                               border_width=2,
                               corner_radius=10)
    pass_entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)


    # add new password function
    def add_new_pass():
        # get entries
        get_name = name_entry.get().lower()
        get_username = username_entry.get()
        get_pass = pass_entry.get()
        # adding name
        with open("password_list.mortlist", "r") as name_list:
            passwords_list = name_list.read()
            if str(get_name) in str(passwords_list):
                    name_error = CTkLabel(new_pass_window, text="This Password Name Already Exists In The list Please Choose A Different Name", text_color="red")
                    name_error.place(relx = 0.5, rely = 0.05, anchor = tkinter.CENTER)
            else:
                # dumbest thing i have ever done
                name_error = CTkLabel(new_pass_window, text="                                                                                                                                             ")
                name_error.place(relx = 0.5, rely = 0.05, anchor = tkinter.CENTER)
                # check first line
                first_line_names = open("password_list.mortlist", "r")
                name_line = first_line_names.readline()
                if not name_line:
                    with open("password_list.mortlist", "a+") as pwd_list:
                        pwd_list.write(f"{get_name}")
                        pwd_list.close()
                else:
                    with open("password_list.mortlist", "a+") as pwd_list:
                        pwd_list.write(f"\n{get_name}")
                        pwd_list.close()
                with open(".env", "a+") as pass_add:
                    encrypted_password = encrypt_pass(get_pass)
                    encrypted_username = encrypt_username(get_username)
                    # check first
                    first_line = open("password_list.mortlist", "r")
                    pass_line = first_line.readline()
                    if not pass_line:
                        with open(".env", "a+") as pass_add:
                            encrypted_password = encrypt_pass(get_pass)
                            encrypted_username = encrypt_username(get_username)
                            pass_add.write(f"{get_name.lower()}_username = {encrypted_username}")
                            pass_add.write(f"{get_name.lower()}_password = {encrypted_password}")
                    else:
                        pass_add.write(f"\n{get_name.lower()}_username = {encrypted_username}")
                        pass_add.write(f"\n{get_name.lower()}_password = {encrypted_password}")
                    name_error = CTkLabel(new_pass_window, text=f"{get_name} Login Info Was Added Successfully", text_color="green")
                    name_error.place(relx = 0.5, rely = 0.7, anchor = tkinter.CENTER)
                    refresh_list()


    add_button = CTkButton(new_pass_window, text="Add Login", command=add_new_pass)
    add_button.place(relx = 0.5, rely = 0.8, anchor = tkinter.CENTER)

# buttons

new_pass_button = customtkinter.CTkButton(app, text="Add New Login Info", command=new_pwd_window)
new_pass_button.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)


# Password List Menu 
passmenu_var = customtkinter.StringVar(value="Passwords")  # set initial value

    #menu function

def pwdmenu_callback(choice):
    passwords = refresh_list()
    ###
    pwd_combobox.configure(values = passwords)
    pwd_combobox.place(relx=0.5, rely=0.3, anchor = tkinter.CENTER)
    password_decrypted = bytes.decode(decrypt_pass(choice), "utf-8")
    username_decrypted = bytes.decode(decrypt_username(choice), "utf-8")
    textbox = customtkinter.CTkTextbox(app, width=400, height=150)
    textbox.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    textbox.insert("0.0", f"{choice}:")  # insert at line 0 character 0
    textbox.insert("2.0", "\n\nUsername: ") 
    textbox.insert("4.11", f"{username_decrypted}")
    textbox.insert("6.0", "\n\nPassword: ") 
    textbox.insert("8.10", f"{password_decrypted}")
    textbox.configure(state="disabled")

    # unused old version

    #pwd_name_label = CTkLabel(pwd_frame, text=f"Login Info For {choice} is:")
    #pwd_name_label.place(relx=0.05, rely=0.1)
    #pwd_pass_label = CTkLabel(pwd_frame, text="Password:")
    #pwd_pass_label.place(relx=0.05, rely=0.3)
    #pwd_pass_label = CTkLabel(pwd_frame, text=password_decrypted)
    #pwd_pass_label.place(relx=0.1, rely=0.5)


    #menu

pwd_list= open("password_list.mortlist", "r")
    #organise the menu
count = 0
pwds = []
while True:
    count += 1

    # Get next line from file
    line = pwd_list.readline()

    # if line is empty
    # end of file is reached
    if not line:
        break
    line = line.replace("\n", "")
    pwds.append(line)
passwords = pwds
###
pwd_combobox = customtkinter.CTkOptionMenu(master=app,
                                     values=passwords,
                                     command=pwdmenu_callback,
                                     variable=passmenu_var)
pwd_combobox.place(relx=0.5, rely=0.3, anchor = tkinter.CENTER)

def refresh_list():
    pwd_list= open("password_list.mortlist", "r")
    #organise the menu
    count = 0
    pwds = []
    while True:
        count += 1
    
        # Get next line from file
        line = pwd_list.readline()
    
        # if line is empty
        # end of file is reached
        line = line.replace("\n", "")
        if not line:
            break
        pwds.append(line)
    passwords = pwds
    ###
    pwd_combobox.configure(values=passwords)
    #pwd_combobox.place(relx=0.5, rely=0.3, anchor = tkinter.CENTER)
    return passwords
refresh_button = CTkButton(app, text="Refresh List", command=refresh_list)
refresh_button.place(relx=0.5, rely=0.7, anchor = tkinter.CENTER)



# color mode menu

    # Dropdown Menu 
with open("color_mode.txt", "r") as mode:
    color = mode.read()
    optionmenu_var = customtkinter.StringVar(value=color)  # set initial value

    #Program Color Mode

def optionmenu_callback(choice):
    with open("color_mode.txt", "w") as mode:
        mode.write(choice)
        customtkinter.set_appearance_mode(choice)
mode_combobox = customtkinter.CTkOptionMenu(master=app,
                                     values=["Dark", "Light", "System"],
                                     command=optionmenu_callback,
                                     variable=optionmenu_var)
mode_combobox.place(relx=0.5, rely=0.1, anchor = tkinter.CENTER)

app.mainloop()
