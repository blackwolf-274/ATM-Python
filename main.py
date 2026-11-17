import json
import os
from datetime import datetime

USERS_FILE = 'users.json'
LOGS_FILE = 'logs.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def log_action(msg):
    with open(LOGS_FILE, 'a') as file:
        file.write(f"[{datetime.now()}] {msg}\n")

def main():
    while True:
        print('1. Create account')
        print('2. Login')
        print('3. Exit')   

        try:
            choice = int(input('> '))
        except ValueError:
            print('Invalid input. Please enter a number.\n')
            continue

        if choice == 1:
            username = input('username: ')
            try:
                pin = int(input('pin: '))
                balance = int(input('balance: USD '))
            except ValueError:
                print('Pin and balance must be numbers!\n')
                continue
            
            create_account(username, pin, balance)
        elif choice == 2:
            username = input('username: ')
            try:
                pin = int(input('pin: '))
            except ValueError:
                print('Pin must be a number!\n')
                continue
                
            if login(username, pin):
                dashboard(username)
        elif choice == 3:
            print('Exiting......\n')
            break

def create_account(username, pin, balance):
    users = load_users()
    if username in users:
        print('Username already exists!\n')
        return
    
    users[username] = {'pin': pin, 'balance': balance}
    save_users(users)
    log_action(f'Account created for {username}')
    print('Account created successfully!\n')

def login(username, pin):
    users = load_users()
    if username in users and users[username]['pin'] == pin:
        print('Login successfully!\n')
        log_action(f'User {username} logged in')
        return True
    else:
        print('Invalid credentials!\n')
        log_action(f'Failed login attempt for {username}')
        return False

def dashboard(username):
    while True:
        print(f'\n--- Welcome, {username} ---')
        print('1. Show balance')
        print('2. Withdrawal')
        print('3. Deposit')
        print('4. Update pin')
        print('5. Logout')

        try:
            choice = int(input('> '))
        except ValueError:
            print('Invalid choice.\n')
            continue

        if choice == 1:
            showbalance(username)
        elif choice == 2:
            try:
                amount = int(input('Enter amount: USD '))
                withdrawal(amount, username)
            except ValueError:
                print('Invalid amount.\n')
        elif choice == 3:
            try:
                amount = int(input('Enter amount: USD '))
                deposit(amount, username)
            except ValueError:
                print('Invalid amount.\n')
        elif choice == 4:
            changePin(username)
        elif choice == 5:
            print('Logging out......\n')
            break

def showbalance(username):
    users = load_users()
    if username in users:
        balance = users[username]['balance']
        log_action(f'{username} checked balance: USD {balance}')
        print(f'Current Balance: USD {balance}\n')
        return balance

def deposit(amount, username):
    if amount <= 0:
        print('Amount must be greater than zero.\n')
        return
        
    users = load_users()
    if username in users:
        users[username]['balance'] += amount
        save_users(users)
        log_action(f'{username} deposited USD {amount}')
        print(f'Successfully deposited USD {amount}')
        showbalance(username)

def changePin(username):
    users = load_users()
    if username in users:
        try:
            currentPin = int(input('Current Pin: '))
        except ValueError:
            print('Invalid pin format.\n')
            return

        if currentPin != users[username]['pin']:
            log_action(f'Failed pin update attempt for {username}')
            print('Incorrect current pin!\n')
        else:
            try:
                new_pin = int(input('New Pin: '))
            except ValueError:
                print('Invalid pin format.\n')
                return
                
            users[username]['pin'] = new_pin
            save_users(users)
            log_action(f'{username} updated pin')
            print('Pin updated successfully!\n')

def withdrawal(amount, username):
    if amount <= 0:
        print('Amount must be greater than zero.\n')
        return
        
    users = load_users()
    if username in users:
        if amount <= users[username]['balance']:
            users[username]['balance'] -= amount
            save_users(users)
            log_action(f'{username} withdrew USD {amount}')
            print(f'Successfully withdrew USD {amount}')
            showbalance(username)
        else:
            print('Insufficient funds\n')

if __name__ == '__main__':
    main()
