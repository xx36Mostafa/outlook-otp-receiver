# Outlook Code Receiver

## Introduction

Outlook Code Receiver is a Python-based script that automates the process of logging into Hotmail/Outlook accounts via POP3 and retrieving Apple ID verification codes from received emails. The script is designed to handle multiple accounts concurrently using threading.

## Features

- **POP3 Authentication**: Automatically logs into Hotmail/Outlook accounts using credentials.
- **Apple ID Code Extraction**: Searches for emails from Apple with the subject "Verify your Apple ID email address" and extracts the 6-digit verification code.
- **Multi-threading**: Processes multiple accounts simultaneously for efficiency.
- **Clipboard Support**: Automatically copies the verification code to the clipboard once retrieved.
- **Error Handling**: Logs successful and failed login attempts.

## Requirements

- Python 3.x
- Required Python libraries:
  - `poplib`
  - `pyperclip`
  - `colorama`
  - `requests`
  - `keyboard`
  - `getmac`
  - `datetime`

Install the required packages using:

```bash
pip install -r requirements.txt
```
## Usage
Prepare Account List:

Add the Hotmail/Outlook accounts in the accounts.txt file in the format email:password, one account per line.
Run the Script:

Execute the script in your terminal or command prompt:
```bash
Copy code
python outlook.py
```
## Contact
= Telegram: @itz36boda
- WhatsApp: +201098974486
## Author
- Made by: Mustafa N. Salem
