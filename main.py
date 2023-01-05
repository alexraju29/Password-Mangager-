from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import sending


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 's', 'r', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website_name = website_entry.get()
    email_id = email_entry.get()
    password = password_entry.get()
    new_data = {
        website_name: {
            "email": email_id,
            "password": password
        }
    }
    if len(website_name) <= 0 or len(password) <= 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website_name, message=f"These are the details entered: \nEmail: {email_id}"
                                                                   f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

        yes = messagebox.askokcancel(title=website_name, message=f"Do you want to send it to your mobile")
        if yes:
            sending.sending_password(website_name, email_id, password)


# ---------------------------- Find Password -------------------------- #


def find_password():
    website_to_search = website_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            result_data = data[website_to_search]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    except KeyError:
        messagebox.showinfo(title="Error", message=f"No details for the {website_to_search} website exists.")
    else:
        yes = messagebox.askyesno(title="Yes Or No",
                                  message=f"Website: {website_to_search}"
                                          f"\n\nEmail Id: {result_data['email']} "
                                          f"\nPassword: {result_data['password']}"
                                          f"\n\nDo you want to send the Password to phone?")
        if yes:
            sending.sending_password(website_to_search, result_data['email'], result_data['password'])

    finally:
        website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, pady=2)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, pady=2)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, pady=2)

# Entries
website_entry = Entry(width=23)
website_entry.grid(row=1, column=1, pady=2)
website_entry.focus()
email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2, pady=2)
email_entry.insert(0, "alexraju29@gmail.com")
password_entry = Entry(width=23)
password_entry.grid(row=3, column=1, pady=2)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2, pady=2)
generate_password = Button(text="Generate Password", width=13, command=generate_password)
generate_password.grid(row=3, column=2, pady=2)
add_button = Button(text="Add", width=38, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, pady=2)

window.mainloop()
