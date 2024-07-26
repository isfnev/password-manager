import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from cryptography.fernet import Fernet
import os
from email_validator import validate_email, EmailNotValidError
import random
import string
import pyperclip

def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

def encrypt_message(message: str) -> str:
    return cipher_suite.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message: str) -> str:
    return cipher_suite.decrypt(encrypted_message.encode()).decode()

def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    if website and username and password:
        encrypted_password = encrypt_message(password)
        with open("passwords.txt", "a") as file:
            file.write(f"{website} | {username} | {encrypted_password}\n")
        clear_fields()
        messagebox.showinfo("Success", "Password saved successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

def view_passwords():
    view_window = tk.Toplevel(root)
    view_window.title("Saved Passwords")
    view_window.geometry("500x400+450+150")
    view_window.resizable(False, False)

    tree = ttk.Treeview(view_window, columns=("Website", "Username", "Password"), show='headings')
    tree.heading("Website", text="Website")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")

    tree.column("Website", width=150)
    tree.column("Username", width=150)
    tree.column("Password", width=200)

    if os.path.exists("passwords.txt"):
        with open("passwords.txt", "r") as file:
            records = file.readlines()
        for record in records:
            website, username, encrypted_password = record.strip().split(" | ")
            decrypted_password = decrypt_message(encrypted_password)
            tree.insert("", "end", values=(website, username, decrypted_password))
    else:
        messagebox.showinfo("No Records", "No passwords saved yet")

    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def forget_password():
    website = entry_website.get()
    if website:
        if os.path.exists("passwords.txt"):
            with open("passwords.txt", "r") as file:
                records = file.readlines()
            with open("passwords.txt", "w") as file:
                for record in records:
                    if not record.startswith(website + " |"):
                        file.write(record)
            messagebox.showinfo("Success", f"Password for {website} forgotten successfully!")
            clear_fields()
        else:
            messagebox.showinfo("No Records", "No passwords saved yet")
    else:
        messagebox.showwarning("Input Error", "Please enter the website to forget")

def generate_random_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    update_password_strength(password)

def copy_to_clipboard():
    password = entry_password.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Input Error", "No password to copy")

def clear_fields():
    entry_website.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    password_strength_label.config(text="")

def update_password_strength(password):
    strength = "Weak"
    if len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isupper() for c in password) and any(c in string.punctuation for c in password):
        strength = "Strong"
    elif len(password) >= 6:
        strength = "Medium"
    password_strength_label.config(text=f"Password Strength: {strength}")

def search_password():
    search_website = entry_website.get()
    if search_website and os.path.exists("passwords.txt"):
        with open("passwords.txt", "r") as file:
            records = file.readlines()
        for record in records:
            website, username, encrypted_password = record.strip().split(" | ")
            if website == search_website:
                decrypted_password = decrypt_message(encrypted_password)
                messagebox.showinfo("Search Result", f"Website: {website}\nUsername: {username}\nPassword: {decrypted_password}")
                return
        messagebox.showwarning("Not Found", f"No password found for {search_website}")
    else:
        messagebox.showwarning("Input Error", "Please enter a website to search")

def user_interface():
    global entry_website, entry_username, entry_password, password_strength_label, root
    key = load_key()
    global cipher_suite
    cipher_suite = Fernet(key)
    root = ThemedTk(theme="arc")
    root.title("Password Manager")
    root.geometry("415x360+450+150")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))

    frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
    frame.grid(sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)
    frame.rowconfigure(6, weight=1)
    frame.rowconfigure(7, weight=1)

    title_label = ttk.Label(frame, text="Password Manager", font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.N)

    label_website = ttk.Label(frame, text="Website:", style="TLabel")
    label_website.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    entry_website = ttk.Entry(frame, width=30)
    entry_website.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    label_username = ttk.Label(frame, text="Username:", style="TLabel")
    label_username.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    label_password = ttk.Label(frame, text="Password:", style="TLabel")
    label_password.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
    entry_password = ttk.Entry(frame, width=30)
    entry_password.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
    entry_password.bind("<KeyRelease>", lambda event: update_password_strength(entry_password.get()))

    password_strength_label = ttk.Label(frame, text="", style="TLabel")
    password_strength_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    button_frame = ttk.Frame(frame, style="TFrame")
    button_frame.grid(row=5, column=0, columnspan=2, pady=10)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.columnconfigure(3, weight=1)
    button_frame.rowconfigure(0, weight=1)
    button_frame.rowconfigure(1, weight=1)

    buttons = [
        ("Save", save_password),
        ("View", view_passwords),
        ("Delete", forget_password),
        ("Generate", generate_random_password),
        ("Copy", copy_to_clipboard),
        ("Search", search_password),
        ("Clear", clear_fields)
    ]

    for i, (text, command) in enumerate(buttons):
        
        button = ttk.Button(button_frame, text=text, command=command)
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky=(tk.W + tk.E))

    root.mainloop()

def main_window():
    global entry_login_email, entry_login_password, login_root
    login_root = ThemedTk(theme="arc")
    login_root.title("Login")
    login_root.geometry("350x220+450+200")
    login_root.resizable(False, False)

    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))

    frame = ttk.Frame(login_root, padding="10 10 10 10", style="TFrame")
    frame.grid(sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)

    title_label = ttk.Label(frame, text="Login", font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.N)

    label_email = ttk.Label(frame, text="Email:", style="TLabel")
    label_email.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    entry_login_email = ttk.Entry(frame, width=30)
    entry_login_email.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    label_password = ttk.Label(frame, text="Password:", style="TLabel")
    label_password.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
    entry_login_password = ttk.Entry(frame, width=30, show="*")
    entry_login_password.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    button_frame = ttk.Frame(frame, style="TFrame")
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    buttons = [
        ("Login", authenticate_user),
        ("Register", register_user)
    ]

    for i, (text, command) in enumerate(buttons):
        button = ttk.Button(button_frame, text=text, command=command)
        button.grid(row=0, column=i, padx=5, pady=5, sticky=(tk.W + tk.E))

    login_root.mainloop()

def authenticate_user():
    email = entry_login_email.get()
    password = entry_login_password.get()

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            records = file.readlines()
        for record in records:
            saved_email, saved_password = record.strip().split(" | ")
            if email == saved_email and password == saved_password:
                messagebox.showinfo("Success", "Login successful!")
                login_root.destroy()
                user_interface()
                return
        messagebox.showwarning("Error", "Invalid email or password")
    else:
        messagebox.showwarning("Error", "No registered users found")

def register_user():
    email = entry_login_email.get()
    password = entry_login_password.get()

    try:
        validate_email(email)
    except EmailNotValidError:
        messagebox.showwarning("Error", "Invalid email format")
        return

    if email and password:
        with open("users.txt", "a") as file:
            file.write(f"{email} | {password}\n")
        messagebox.showinfo("Success", "Registration successful! You can now login.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

if __name__ == "__main__":
    main_window()
