#!/usr/bin/python3

import os
import re
import sys
import shutil
import time
import ping3
import datetime
from datetime import datetime

print("--------- Exec Script ----------\n")

#---------------- Segment 0: purge ips invalidated ----------------------------------
def ping_ips(ips):
   ip_list_clear = list(filter(str.strip, ips))
   successful_ips = []
   current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
   print(current_date)
   number = 0
   for ip in ip_list_clear:
      number += 1
      try:
        response_time = ping3.ping(ip, timeout=1)
        if response_time is not None:
           successful_ips.append(ip)
           print(f"------------ address adding {number}")
      except Exception:
        pass
   current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
   print(current_date)
   successful_ips_clear =  list(filter(str.strip, successful_ips))
   return successful_ips_clear
#---------------- Segment 0: end ----------------------------------

#---------------- Segment 1: We download the EDLS ----------------------------------

time_1 = datetime.now()

os.system("wget --no-check-certificate --ftp-user=resegti_user --ftp-password=resegti_pass -O vps_temp.txt ftps://85.119.82.151:4321/ftp_data/ip_file.txt")
os.system("wget -O damuk.txt --inet4-only https://www.dan.me.uk//torlist/")
os.system("wget -O tor.txt https://check.torproject.org/torbulkexitlist")

#---------------- Segment 1: End ----------------------------------

#---------------- Segment 2: files temporales (vps_temp.txt & damuk_temp.txt) ----------------------------------
file_vps_temp = "vps_temp.txt"
file_vps = "vps.txt"

with open(file_vps_temp, 'r') as vps_temp:
    lines_temp_vps = vps_temp.readlines()

with open(file_vps, 'r') as vps:
    lines_vps = vps.readlines()

active_ips_vps = ping_ips(lines_vps)
lines_final_vps = list(set(active_ips_vps + lines_temp_vps))

with open(file_vps, 'w') as vps:
    vps.writelines(lines_final_vps)

print("-> file vps.txt update\n")
#---------------- Segment 2: End ----------------------------------

#---------------- Segment 3: Merge damuk.txt & tor.txt, filter IPv4 only ----------------------------------

file_damuk = "damuk.txt"
file_tor = "tor.txt"
file_temp = "temp.txt"

with open(file_damuk, 'r') as damuk:
    lines_damuk = damuk.readlines()

with open(file_tor, 'r') as tor:
    lines_tor = tor.readlines()

lines_temp = list(set(lines_damuk + lines_tor))
number_ipv4_ipv6 = len(lines_temp)
print(f"-> Number of IPv4 & IPv6 = {number_ipv4_ipv6}")

address_ipv4 = []
for linea in lines_temp:
    address = linea.strip()
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', address):
        address_ipv4.append(address)

number_ipv4_only = len(address_ipv4)
print(f"-> Number of IPv4 only = {number_ipv4_only}")

with open(file_temp, 'w') as temp:
    for ip in  address_ipv4:
        temp.write(ip + '\n')

print("-> file temp.txt create\n")
#---------------- Segment 3: End  ----------------------------------

#---------------- Segment 4: Merge vps.txt & temp.txt, remove duplicate addresses, remove IP invalitated -------------------------

file_temp = "temp.txt"
file_vps = "vps.txt"
file_final = "directory_final.txt"

with open(file_temp, 'r') as temp:
    lines_temp = temp.readlines()

with open(file_vps, 'r') as vps:
    lines_vps = vps.readlines()

lines_final = list(set(lines_temp + lines_vps))

with open(file_final, 'w') as final:
    final.writelines(lines_final)

number_directory = len(lines_final)
print(f"-> Number of IPv4 directory = {number_directory}")

print("-> file directory_final update\n")
#---------------- Segment 4: End  ----------------------------------

#---------------- Segment 5: Generate file for shorewall --------------------------

directory_shorewall = "directory_shorewall.txt"
directory_final = "directory_final.txt"

with open (directory_final,"r") as final:
 with open (directory_shorewall,"w") as shorewall:
  shorewall.write("#ACTION  SOURCE  DEST  PROTO DPORT SPORT ORIGDEST RATE USER MARK CONNLIMIT TIME HEADERS SWITCH HELPER\n")
  shorewall.write("?SECTION ALL\n")
  shorewall.write("?SECTION ESTABLISHED\n")
  shorewall.write("?SECTION RELATED\n")
  shorewall.write("?SECTION INVALID\n")
  shorewall.write("?SECTION UNTRACKED\n")
  shorewall.write("?SECTION NEW\n")
  shorewall.write("Ping(ACCEPT)	loc:10.10.10.0/24	net\n")
  shorewall.write("SSH(ACCEPT)	loc:10.10.10.15/32	fw:10.10.10.254\n")
  shorewall.write("DNS(ACCEPT)	loc:10.10.10.0/24	net\n")
  shorewall.write("\n########	Remote control \n")
  shorewall.write("ACCEPT	hamachi	fw	udp	1024:65535\n")
  shorewall.write("ACCEPT	hamachi	fw	tcp	1024:65535\n")
  shorewall.write("ACCEPT	fw	hamachi	udp	1024:65535\n")
  shorewall.write("ACCEPT	fw	hamachi	tcp	1024:65535\n")
  shorewall.write("ACCEPT	loc	hamachi	udp	1024:65535\n")
  shorewall.write("ACCEPT	loc	hamachi	tcp	1024:65535\n")
  shorewall.write("ACCEPT	net	hamachi	udp	1024:65535\n")
  shorewall.write("ACCEPT	net	hamachi	tcp	1024:65535\n")
  shorewall.write("\n########	Init -> black list TOR \n")

  for i in final:
   shorewall.write("REJECT	loc:10.10.10.0/24	"+"net:"+i)

  shorewall.write("\n########	finish -> black list TOR \n")
  shorewall.write("HTTP(ACCEPT)	loc:10.10.10.0/24	net\n")
  shorewall.write("HTTPS(ACCEPT)	loc:10.10.10.0/24	net\n")
  shorewall.write("ACCEPT	loc:10.10.10.0/24	net	udp 	1024:65535\n")
  shorewall.write("ACCEPT	loc:10.10.10.0/24     	net     tcp     1024:65535\n")

print("-> file directory_shorewall.txt create\n")
#---------------- Segment 5: End --------------------------

#---------------- Segment 6: Update the rules & response time calculate --------------------------
os.system("sudo cp directory_shorewall.txt /etc/shorewall/rules")
os.system("sudo systemctl restart shorewall")
print("-> Shorewall rules update\n")

time_2 = datetime.now()
difference_time = time_2 - time_1
difference_milliseconds = difference_time.total_seconds() * 1000

response_time = "response_time.txt"
pid_number = os.getpid()
with open(response_time, "a") as file:
	file.write(f"{pid_number}|{time_1}|{time_2}|{difference_milliseconds}\n")
print("-> file response_time.txt update\n")

#---------------- Segment 6: End --------------------------

#---------------- Segment 7: We make backups of the files (vps.txt, directory_final.txt) ----------------------------------

current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

file = "vps.txt"
path_backup = "/home/firewall/backups/results_vps"
name_backup = f"vps_{current_date}.txt"
path_file_backup = os.path.join(path_backup, name_backup)
shutil.copy2(file, path_file_backup)
print("-> file vps.txt backup done\n")

file = "directory_final.txt"
path_backup = "/home/firewall/backups/results_directory"
name_backup = f"directory_final_{current_date}.txt"
path_file_backup = os.path.join(path_backup, name_backup)
shutil.copy2(file, path_file_backup)
print("-> file directory_final.txt backup done\n")
os.system("sudo cp {} /home/firewall/samba/".format(file))

file = "response_time.txt"
path_backup = "/home/firewall/backups/results_shorewall"
name_backup = f"response_time_{current_date}.txt"
path_file_backup = os.path.join(path_backup, name_backup)
shutil.copy2(file, path_file_backup)
print("-> file response_time.txt backup done\n")

#---------------- Segment 7: End  ----------------------------------

#---------------- Segment 8: Sleep 30 min and the script is executed again --------------------------

print("------------------- script sleeping for 30 minutes\n")

time.sleep(1800) #en segundos

script_path="/home/firewall/Tesis/script_firewall.py"
python_path = sys.executable
os.execv(python_path, [python_path, script_path])
#---------------- Segment 8: End --------------------------
