import poplib
import pyperclip
from email import parser
import re
import sys
import os
import threading
from datetime import datetime
from colorama import Fore, Style, init
from getmac import get_mac_address as g 
import requests , keyboard

reset = Fore.RESET
success = 0
success += 1
init(strip=not sys.stdout.isatty())
def extract_verification_code(email_body):
    match = re.search(r'\b\d{6}\b', email_body)
    if match:
        return match.group(0)
    return None

def parse_email_date(date_str):
    email_time_format = "%a, %d %b %Y %H:%M:%S %z"
    return datetime.strptime(date_str, email_time_format)

def login_to_hotmail(email_address, password, index):
    pop3_server = 'pop-mail.outlook.com'
    pop3_port = 995
    count = 0
    err = 0
    while True:
        if keyboard.is_pressed('='):
            sys.exit()
        try:
            mail = poplib.POP3_SSL(pop3_server, pop3_port, timeout=60)
            mail.user(email_address)
            mail.pass_(password)
            if count == 0:
                print(f'[{Fore.LIGHTGREEN_EX}{index + 1}/{lens}{Fore.RESET}]{Fore.MAGENTA} Success Login: {reset}[ {Fore.LIGHTGREEN_EX}{email_address}{Fore.RESET} ] ')
                with open('logined.txt','a',encoding='utf-8') as f:
                    f.write(f'{email_address}:{password}\n')
            count += 1
            num_messages = len(mail.list()[1])
            response, lines, octets = mail.retr(num_messages)
            msg_data = b"\n".join(lines).decode('utf-8')
            message = parser.Parser().parsestr(msg_data)
            from_email = message.get('from')
            subject = message.get('subject')
            if from_email and 'appleid@id.apple.com' in from_email and subject and 'Verify your Apple ID email address' in subject:
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode()
                            verification_code = extract_verification_code(body)
                            if verification_code:
                                mail.quit()
                                return verification_code
                else:
                    body = message.get_payload(decode=True).decode()
                    verification_code = extract_verification_code(body)
                    if verification_code:
                        mail.quit()
                        return verification_code
            else:
                if err == 0:
                    print(f"[{Fore.LIGHTRED_EX}{index + 1}{Fore.RESET}] Sleep until receive code....")
                err += 1
            mail.quit()
        except Exception as e:
            if str(e).strip() == "b'-ERR Logon failure: unknown user name or bad password.'":
                print(f'[{Fore.RED}-{Fore.RESET}]{Fore.LIGHTRED_EX} Failed Login: {reset}[ {Fore.LIGHTRED_EX}{email_address}{Fore.RESET} ] ')
                break
            else:
                pass

def main(email_address, password, account, index):
    verification_code = login_to_hotmail(email_address, password, index)
    if verification_code:
        pyperclip.copy(verification_code)
        print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}]{Fore.LIGHTYELLOW_EX} Verification code:{Fore.LIGHTCYAN_EX}', verification_code, Fore.RESET, f'[ {email_address} ]')
        with open('success.txt', 'a') as f:
            f.write(f'{account}\n')
        all_list.remove(account)
        with open('accounts.txt', 'w') as f:
            for account in all_list:
                f.write(f'{account}\n')
    else:
        print(f'[{Fore.RED}-{Fore.RESET}]{Fore.LIGHTRED_EX} Failed Login: {reset}[ {Fore.LIGHTRED_EX}{email_address}{Fore.RESET} ]')
        with open('failed.txt', 'a') as f:
            f.write(f'{account}\n') 
        all_list.remove(account)
        with open('accounts.txt', 'w') as f:
            for account in all_list:
                f.write(f'{account}\n')

def thread_main(account, index):
    email_address, password = account.split(':')
    main(email_address, password, account, index)

def logo():
    os.system('cls')
    print(Fore.LIGHTRED_EX + ( "\t\t\t\n"                                 
"\t ██████╗░░█████╗░██████╗░░█████╗░██████╗░░█████╗░\n"
"\t ╚════██╗██╔═══╝░██╔══██╗██╔══██╗██╔══██╗██╔══██╗\n"
"\t ░█████╔╝██████╗░██████╦╝██║░░██║██║░░██║███████║\n"
"\t ░╚═══██╗██╔══██╗██╔══██╗██║░░██║██║░░██║██╔══██║\n"
"\t ██████╔╝╚█████╔╝██████╦╝╚█████╔╝██████╔╝██║░░██║\n"
"\t ╚═════╝░░╚════╝░╚═════╝░░╚════╝░╚═════╝░╚═╝░░╚═╝\n"
"\t\t             Outlook Code Receiver             \n"
"\t\t     Made By: Mustafa N. Salem    \n"
"\t\t        telegram: @itz36boda"))
    print(Fore.RED +'\t\t MUSTAFA NASSER - Whattsapp [+201098974486]'+Style.RESET_ALL)
if __name__ == "__main__":
    logo()
    all_list = open('accounts.txt', 'r').read().splitlines()
    lens = len(all_list)
    threads = []
    for index, account in enumerate(all_list):
        t = threading.Thread(target=thread_main, args=(account, index))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    input('[-] Press Any Key ....')
