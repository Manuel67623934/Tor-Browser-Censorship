from datetime import datetime
import time
import shutil
import requests
import re
import os
import subprocess
import stem
from stem import CircStatus
from stem.control import Controller
import re
import sys

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

def delete_bridges_block(file1, file2, file3):
    file1 = file1
    file2 = file2
    file3 = file3
    ipv4_addresses = []
    with open(file1, 'r') as file:
        file1_lines = file.readlines()
    with open(file2, 'r') as file:
        file2_lines = file.readlines()  
    for line in file1_lines:
        ip_matches = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
        ipv4_addresses.extend(ip_matches)
    bridges_blocks = []
    for ip_address in ipv4_addresses:
        for line in file2_lines:
            if ip_address.strip() in line:
                bridges_blocks.append(ip_address.strip())
    filtered_lines = []
    for line in file1_lines:
        ip_address = line.split()[1].split(":")[0]
        if ip_address not in bridges_blocks:
            filtered_lines.append(line) 
    cleaned_lines = []
    for line in filtered_lines:
        line = line.strip()  
        if not line:
            continue  
        cleaned_lines.append(line)
    with open(file3, 'w') as file:
        file.write('\n'.join(cleaned_lines))

def merge_files(file1, file2, output_file):
    print("-------------------------")
    with open(file1, 'r') as file:
        file1_lines = file.readlines()
    with open(file2, 'r') as file:
        file2_lines = file.readlines()  
    merged_lines = list(set(file1_lines + file2_lines))
    processed_lines = []
    for line in merged_lines:
        line = line.strip()
        processed_lines.append("bridge " + line)  
    processed_lines.insert(0, 'ClientTransportPlugin obfs4 exec C:\\Users\\cliente\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\PluggableTransports\\obfs4proxy.exe\n')
    processed_lines.append("\nUseBridges 1")    
    with open(output_file, 'w') as file:
        file.write('\n'.join(processed_lines))

def send_file_to_tor_directory(file_path):
    print("-------------------------")
    tor_directory = r'C:\Users\cliente\Desktop\Tor Browser\Browser\TorBrowser\Tor'
    tor_file_path = tor_directory + r'\bridges.txt'
    shutil.copyfile(file_path, tor_file_path)
    print("bridges.txt successfully copied to Tor directory!")

def execute_tor():
    print("-------------------------")
    target_directory = r'C:\Users\cliente\Desktop\Tor Browser\Browser\TorBrowser\Tor'
    os.chdir(target_directory)
    current_directory = os.getcwd()
    print("Directorio actual:", current_directory)
    command = 'tor.exe -f bridges.txt'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Tor command executed successfully!")
    start_time = time.time()
    max_wait_time = 300  #antes 180 - 120
    while True:
        output = process.stdout.readline().decode().strip()
        print(output)
        if output:
            print(output)
            if re.search(r'\[notice\] Bootstrapped 100% \(done\): Done', output):
                print("Tor circuit established. Ready to make requests!")
                break
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_wait_time:
            return False
    return True    

def terminate_tor():
    print("-------------------------")
    os.system('taskkill /f /im tor.exe')
    print("Tor process terminated! ---- taskkill")

def difference_time (time_1, time_2):
      difference_time = time_2 - time_1
      difference_milliseconds = difference_time.total_seconds() * 1000
      return difference_milliseconds

def request_url(url):
    try:
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
        r = session.get(url)        
        return "successful request"
    except Exception as e:
        return "failed request"   

def request_onion_services():
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"\nResults of {current_date}\n")
    file_results = "results_tor.txt"
    sites_onion = [
    #taken from: https://www.expressvpn.com/es/blog/las-mejores-19-paginas-web-onion-de-la-dark-web/
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/",       #Ahmia
    "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/",       #Haystak
    "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/",       #Torch
    "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/",      #DuckDuckGo
    "http://wasabiukrxmkdgve5kynjztuovbg43uxcbcxn6y2okcrsg7gb6jdmbad.onion/",       #Wasabi Wallet
    "http://p53lf57qovyuvwsc6xnrppyply3vtqm7l6pcobkmyqsiofyeznfu5uqd.onion/",       #ProPublica
    "http://archiveiya74codqgiixo33q62qlrqtkgmcitqx5u2oeqnmn5bpcbiyd.onion/",       #Archive Today
    "https://protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion/",      #ProtonMail
    "https://www.bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion/",  #BBC
    "http://ciadotgov4sjwlzihbbgxnqg3xiyrg7so2r2o3lt5wz5ypk4sxyjstad.onion/"        #CIA
    ]
    with open (file_results, "a") as file:
        file.write(f"\nResults of {current_date}\n")
        for site in sites_onion:
            time_1 = datetime.now()
            if execute_tor():
                time.sleep(5)
                print("Requesting url ...")         
                response = request_url(site)
                print("Requested url !!!")
                time_2 = datetime.now()
                difference_milliseconds = difference_time(time_1, time_2)
                file.write(f"{site}|{time_1}|{time_2}|{difference_milliseconds}|{response}|Tor browser DID run\n")
                terminate_tor()
            else:
                time_2 = datetime.now()
                difference_milliseconds = difference_time(time_1, time_2)
                time.sleep(5)
                file.write(f"{site}|{time_1}|{time_2}|{difference_milliseconds}|failed request|Tor browser DIDN'T run\n")
            time.sleep(5)
    print("File results_tor.txt was create!")

def execute_tor_request_onion_services():
    print("Init execute_tor_request_onion_services() function  .....")
    file1 = "bridges_telegram_temp.txt"
    file2 = "directory_final.txt"
    file3 = "bridges_telegram_temp_2.txt"
    delete_bridges_block(file1, file2, file3)
    file1 = "bridges_bank.txt"
    file2 = "directory_final.txt"
    file3 = "bridges_bank_2.txt"
    delete_bridges_block(file1, file2, file3)
    file1 = "bridges_telegram_temp_2.txt"
    file2 = "bridges_bank_2.txt"
    output_file = "bridges.txt"
    merge_files(file1, file2, output_file)
    file_path = 'C:\\Users\\cliente\\Documents\\Tesis\\script_Tor\\Temp_to_bridges\\bridges.txt'
    send_file_to_tor_directory(file_path)
    request_onion_services()   
    print("Terminated execute_tor_request_onion_services() function  .....") 

def main():   
    
    print("Init script Tor cliente ...")
    execute_tor_request_onion_services()
    print("Finalized script Tor cliente !")        
    #backup to results_tor.txt
    target_directory = r'C:\Users\cliente\Documents\Tesis\script_Tor\Temp_to_bridges' 
    os.chdir(target_directory)
    file_backup = "results_tor.txt"
    current_date = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    path_backup = "D:\\results_tor"
    name_backup = f"results_tor_{current_date}.txt"
    path_file_backup = os.path.join(path_backup, name_backup)
    shutil.copy2(file_backup, path_file_backup)
    print("------------------- file results_tor.txt backup done\n")  
    print("Sleeping for 30 min !!!")
    time.sleep(1800)

    script_path= "C:\\Users\\cliente\\Documents\\Tesis\\script_Tor\\Temp_to_bridges\\script_tor.py"
    python_path = sys.executable
    os.execv(python_path, [python_path, script_path])

    
   
if __name__ == "__main__":
    main()









