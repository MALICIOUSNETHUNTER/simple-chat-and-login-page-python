import os
import sqlite3
import getpass
from datetime import datetime

os.system('clear')

# Connect to DB
conn = sqlite3.connect('app.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    name TEXT,
    branch TEXT,
    reg_no TEXT,
    fav_sub TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    message TEXT,
    timestamp TEXT,
    is_read INTEGER DEFAULT 0
)''')
conn.commit()

class User:
    def __init__(self, id, username, password, name="", branch="", reg_no="", fav_sub=""):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.branch = branch
        self.reg_no = reg_no
        self.fav_sub = fav_sub

def find_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    return User(*row) if row else None

def showProfile(user):
    os.system('clear')
    print("Name:", user.name)
    print("Branch:", user.branch)
    print("Reg No:", user.reg_no)
    print("Favourite Subject:", user.fav_sub)
    print("username:", user.username)

def check_inbox(user):
    c.execute("SELECT * FROM messages WHERE receiver=? ORDER BY timestamp DESC", (user.username,))
    msgs = c.fetchall()
    if not msgs:
        print("📭 No messages")
        return

    print("\n=== INBOX ===")
    for msg in msgs:
        status = "✅ Read" if msg[5] else "📩 New"
        print(f"{status} | From: {msg[1]} | Time: {msg[4]}")
        print(f"Message: {msg[3]}")
        print("-"*30)
        if not msg[5]: # mark as read
            c.execute("UPDATE messages SET is_read=1 WHERE id=?", (msg[0],))
    conn.commit()

def send_message(sender):
    receiver = input("Enter receiver username: ")
    if not find_user(receiver):
        print("❌ User not found")
        return
    message = input("Enter your message: ")
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO messages(sender, receiver, message, timestamp) VALUES(?,?,?,?)",
              (sender.username, receiver, message, time))
    conn.commit()
    print("Message sent ✅")

print("===========================================")
print("\tWelcome to the Login Page")
print("===========================================")

while True:
    print("Select Option:\t 1. Login\n\t 2. Register\n\t 3. Forgot Password\n\t 4. exit")
    try:
        choice = int(input("Enter your choice: "))
    except:
        print("Enter numbers only")
        continue

    if choice == 4:
        break

    elif choice == 1:
        username = input("Enter your username: ")
        inUser = find_user(username)
        if inUser == None:
            print("User doesn't exist")
        else:
            password = getpass.getpass("Enter your password: ")
            if inUser.password == password:
                print("✅ Logged in successfully")
                while True:
                    print("\n1. Show Profile\n2. Check Inbox\n3. Send Message\n4. Logout")
                    opt = int(input("Enter your choice: "))
                    if opt == 1:
                        showProfile(inUser)
                    elif opt == 2:
                        check_inbox(inUser)
                    elif opt == 3:
                        send_message(inUser)
                    else:
                        print("Logged out")
                        break
            else:
                print("❌ Incorrect password! Try again")

    elif choice == 2:
        username = input("Enter Username: ")
        if find_user(username):
            print("❌ Username is not available")
            continue
        password = getpass.getpass("Enter password: ")
        cPass = getpass.getpass("Confirm Password: ")
        if cPass!= password:
            print("Password doesn't match")
            continue
        name = input("Enter your name: ")
        branch = input("Enter your branch: ")
        reg_no = input("Enter your registration number: ")
        fav_sub = input("Your favourite subject: ")

        c.execute("INSERT INTO users(username,password,name,branch,reg_no,fav_sub) VALUES(?,?,?,?,?,?)",
                  (username,password,name,branch,reg_no,fav_sub))
        conn.commit()
        print("Successfully Registered ✅")

    elif choice == 3:
        username = input("Enter your username: ")
        inUser = find_user(username)
        if inUser == None:
            print("User doesn't exist")
        else:
            inFavS = input("Enter your favourite subject: ")
            if inFavS == inUser.fav_sub:
                nPass = getpass.getpass("Enter new password: ")
                c.execute("UPDATE users SET password=? WHERE username=?", (nPass, username))
                conn.commit()
                print("Password Changed Successfully ✅")
            else:
                print("Wrong Answer try again!")

conn.close()
