import requests
import json
import time
import sys
import os
import random
import string
from platform import system
from rich import print as printer
from rich.panel import Panel
from datetime import datetime

# Color definitions
BOLD = '\033[1m'
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = '\033[31m'
BLUE = "\033[34m"
MAGENTA = "\033[95m"
RESET = '\033[0m'

APPROVAL_FILE = ".toolkey"  # local file for saving generated key
APPROVAL_URL = "https://raw.githubusercontent.com/sahil-tech-official/convobysahilxhaseeb/main/approval.txt"

def liness():
    print('\u001b[37m' + '---------------------------------------------------')

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(MAGENTA + BOLD + r"""
   _____         _    _ _____ _      
  / ____|  /\   | |  | |_   _| |     
 | (___   /  \  | |__| | | | | |     
  \___ \ / /\ \ |  __  | | | | |     
  ____) / ____ \| |  | |_| |_| |____ 
 |_____/_/    \_\_|  |_|_____|______|                                                                                                                                                 
""" + RESET)
    print(CYAN + "╔════════════════════════╗")
    print("║      Made By sahil     ║")
    print("╚════════════════════════╝" + RESET)
    print(CYAN + "═" * 50 + RESET)

# Generate or load saved key
def get_or_create_key():
    if os.path.exists(APPROVAL_FILE):
        with open(APPROVAL_FILE, 'r') as f:
            return f.read().strip()
    else:
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        with open(APPROVAL_FILE, 'w') as f:
            f.write(key)
        return key

# Random key-based approval system
def approval():
    cls()
    key = get_or_create_key()
    try:
        httpChat = requests.get(APPROVAL_URL, timeout=5).text
        if key in httpChat:
            print(GREEN + "[✓] Approved Key: " + key + RESET)
            time.sleep(1)
            return True
        else:
            print(RED + "[x] Not Approved!" + RESET)
            print("Your Key: " + key)
            input('\nPress ENTER to request approval on WhatsApp...')
            tks = f'Hello! Sir, please approve my key: {key}'
            os.system('am start https://wa.me/+994400607075?text=' + tks.replace(" ", "%20"))
            return False
    except requests.exceptions.RequestException:
        print(RED + "[!] Internet connection error" + RESET)
        return False

# Token verification
def verify_token(token):
    try:
        resp = requests.get("https://graph.facebook.com/v15.0/me",
                            params={'access_token': token}, timeout=5)
        if resp.ok:
            data = resp.json()
            return data.get('name')
    except:
        return None
    return None

def get_tokens():
    tokens = []
    profiles = []
    valid_count = 0
    invalid_count = 0

    print("[1] Enter tokens manually")
    print("[2] Load tokens from file")
    mode = input("Choose token input mode (1/2): ")

    if mode == '1':
        count = int(input("How many tokens do you want to use?: "))
        for i in range(count):
            token = input(f"Enter Access Token {i+1}: ").strip()
            name = verify_token(token)
            if name:
                tokens.append(token)
                profiles.append(name)
                valid_count += 1
                print(GREEN + f"[✓] Valid Token: {name} | Token: {token}" + RESET)
            else:
                invalid_count += 1
                print(RED + f"[x] Invalid Token: {token}" + RESET)

    elif mode == '2':
        file = input("Enter token file path: ")
        with open(file, 'r') as f:
            for line in f:
                token = line.strip()
                name = verify_token(token)
                if name:
                    tokens.append(token)
                    profiles.append(name)
                    valid_count += 1
                    print(GREEN + f"[✓] Valid Token: {name} | Token: {token}" + RESET)
                else:
                    invalid_count += 1
                    print(RED + f"[x] Invalid Token: {token}" + RESET)
    else:
        print(RED + "Invalid selection!" + RESET)
        return get_tokens()

    print(CYAN + f"Total Valid: {valid_count} | Total Invalid: {invalid_count}" + RESET)
    return tokens, profiles

def send_convo(tokens, profiles):
    convo_id = input(CYAN + "Enter Conversation ID: " + RESET)
    text_file = input(CYAN + "Enter Text File Path: " + RESET)
    hater = input(CYAN + "Add Hater's Name: " + RESET)
    delay = int(input(CYAN + "Speed (seconds): " + RESET))

    with open(text_file, 'r') as f:
        messages = f.readlines()

    i = 0
    while True:
        try:
            idx = i % len(tokens)
            token = tokens[idx]
            profile_name = profiles[idx]
            msg = hater + ' ' + messages[i % len(messages)].strip()
            resp = requests.post(f"https://graph.facebook.com/v15.0/t_{convo_id}",
                                 data={'access_token': token, 'message': msg})
            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if resp.ok:
                print(GREEN + f"[✓] Sent by {profile_name}: {msg} | Time: {current_time}" + RESET)
            else:
                print(RED + f"[x] Failed by {profile_name}: {msg} | Error: {resp.text}" + RESET)
            i += 1
            time.sleep(delay)
        except KeyboardInterrupt:
            print(RED + "\n[!] Stopping Convo Sender..." + RESET)
            break
        except:
            print(RED + "[x] Network issue. Retrying..." + RESET)
            time.sleep(5)

def send_post(tokens, profiles):
    post_link = input(CYAN + "Enter Facebook Post Link: " + RESET)
    text_file = input(CYAN + "Enter Comment File Path: " + RESET)
    hater = input(CYAN + "Add Hater's Name: " + RESET)
    delay = int(input(CYAN + "Speed (seconds): " + RESET))

    with open(text_file, 'r') as f:
        comments = f.readlines()

    if "story_fbid=" in post_link:
        post_id = post_link.split("story_fbid=")[1].split("&")[0]
    elif "/posts/" in post_link:
        post_id = post_link.split("/posts/")[1].split("/")[0]
    else:
        post_id = post_link.split("/")[-1].split("?")[0]

    i = 0
    while True:
        try:
            idx = i % len(tokens)
            token = tokens[idx]
            profile_name = profiles[idx]
            comment = hater + ' ' + comments[i % len(comments)].strip()
            resp = requests.post(f"https://graph.facebook.com/{post_id}/comments",
                                 data={'access_token': token, 'message': comment})
            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if resp.ok:
                print(GREEN + f"[✓] Comment by {profile_name}: {comment} | Time: {current_time}" + RESET)
            else:
                print(RED + f"[x] Failed by {profile_name}: {comment} | Error: {resp.text}" + RESET)
            i += 1
            time.sleep(delay)
        except KeyboardInterrupt:
            print(RED + "\n[!] Stopping Post Commenter..." + RESET)
            break
        except:
            print(RED + "[x] Network issue. Retrying..." + RESET)
            time.sleep(5)

def main_menu():
    while True:
        cls()
        logo()
        print(CYAN + "[1] Facebook Convo Tool")
        print("[2] Facebook Post Comments")
        print("[3] Exit" + RESET)
        print(CYAN + "═" * 50 + RESET)
        choice = input(CYAN + "Choose option (1-3): " + RESET)

        if choice in ['1', '2']:
            tokens, profiles = get_tokens()
            if not tokens:
                input(RED + "No valid tokens. Press Enter to return to menu." + RESET)
                continue
            if choice == '1':
                send_convo(tokens, profiles)
            else:
                send_post(tokens, profiles)
        elif choice == '3':
            print(GREEN + "Exiting... Bye!" + RESET)
            sys.exit()
        else:
            input(RED + "Invalid choice. Press Enter to retry." + RESET)

if __name__ == "__main__":
    if not approval():
        sys.exit()
    main_menu()