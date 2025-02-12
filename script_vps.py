#!/usr/bin/python3

import re
import os
import sys

print("---------Exec Script-------------")

#---------  Segment 1: Capture incoming IP addresses to port 9001 -------------------
print("------------------- capturing the traffic for 30 minutes\n")
os.system("sudo timeout 1800 tcpdump -i eth0 dst port 9001 | awk '{print $3}' > tcp_file.txt")
print("------------------- capture finished the traffic for 30 minutes\n")
#------------------------------- End of Segment 1 ----------------------------------

#--------- Segment 2: to separate IP addresses from their source ports -------------------
file_entry = "tcp_file.txt"
file_exit = "ip_file.txt"

with open(file_entry, 'r') as entry:
    lines = entry.readlines()

addresses_ip = []
for linea in lines:
    parts = linea.strip().split('.')
    address_ip = '.'.join(parts[:4])
    addresses_ip.append(address_ip)

addresses_ip_only = []
for linea in addresses_ip:
    parts = linea.strip().split('.')
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', linea):
        address_ip_only = '.'.join(parts[:4])
        addresses_ip_only.append(address_ip_only)

unique_ips = []
for ip in addresses_ip_only:
    if ip not in unique_ips:
        unique_ips.append(ip)

with open(file_exit, 'w') as exit:
    for address_ip in unique_ips:
        exit.write(address_ip + '\n')
#------------------------------- End of Segment 2 ----------------------------------

#------------------------------- Segment 3: Moving the file to the vsftpd server ----------------------------------
os.system("sudo cp ip_file.txt /home/resegti_user/ftp_directory/ftp_data/")
#------------------------------- End of Segment 3 ----------------------------------

print("--------- Final Exec Script-------------")

#------------- Segment 4: Reruns the script without creating new instances --------
script_path="/home/manuel/Tesis/script_vps.py"
python_path = sys.executable
os.execv(python_path, [python_path, script_path])
#------------------------------- End of Segment 4 ----------------------------------


