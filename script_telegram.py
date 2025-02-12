from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from datetime import datetime
import time
import shutil
import os

def send_sms_telegram(): 
        print("-------------------------")  
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")         
        api_id = '27545689'
        api_hash = 'c5a0550e09d0f573e911b956d2a3208c'
        phone = '+51933898635'        
        client = TelegramClient(phone, api_id, api_hash)
        client.connect()
        print("Client connect ...")
        time.sleep(5)
        if not client.is_user_authorized():
            client.send_code_request(phone)
            client.sign_in(phone, input('Enter the code: '))        
        destination = 'GetBridgesBot'        
        message = "/bridges"
        try:
            receiver = client.get_input_entity(destination)
            client.send_message(receiver, message)
            time.sleep(5)
            print("Message send!!")
            try:                
                file_bridges = 'bridges_telegram.txt'
                with open(file_bridges, 'a') as file:
                    file.write(f"\nResults of {current_date}\n")
                    messages = client.get_messages(receiver, limit=2)
                    second_message = client.get_messages(receiver, min_id=messages[-1].id)
                    for sms in second_message:
                        file.write(sms.text + "\n")                    
                print("bridges_telegram.txt was created successfully!!")
            except Exception as e:
                print(str(e))
                if str(e) == "list index out of range":
                    print("There are no more messages to read")
                client.disconnect()
        except Exception as e:
            print(str(e))
            print("The SMS was not sent")
        client.disconnect()

def clean_file_telegram(input_file, output_file):
    print("-------------------------")
    with open(input_file, 'r') as file:
        lines = file.readlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()  
        if line.startswith("Results of"):
            continue          
        if not line:
            continue  
        cleaned_lines.append(line)
    with open(output_file, 'w') as file:
        file.write('\n'.join(cleaned_lines))

def main():    
    count = 0
    while True:
        count += 1
        print("Init script Telegram ..." + str(count))
        send_sms_telegram()
        input_file = "bridges_telegram.txt"
        output_file = "bridges_telegram_temp.txt"
        clean_file_telegram(input_file, output_file)
        print("Finalized script Telegram !")
        #backup to results_telegram.txt
        file_backup = "bridges_telegram.txt"
        current_date = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        path_backup = "D:\\results_telegram"
        name_backup = f"bridges_telegram_{current_date}.txt"
        path_file_backup = os.path.join(path_backup, name_backup)
        shutil.copy2(file_backup, path_file_backup)
        print("------------------- file bridges_telegram.txt backup done\n")       
        print("Sleeping for 24h !!!")
        time.sleep(87000) #24h + 10 min   
if __name__ == "__main__":
    main()
