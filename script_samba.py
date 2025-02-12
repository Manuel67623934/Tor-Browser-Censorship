import shutil 
import time

source_path = r"\\firewall.local\sharedsamba\directory_final.txt"
destination_path = r"C:\Users\cliente\Documents\Tesis\script_Tor\Temp_to_bridges\directory_final.txt" 

def get_file_samba():    
    try:    
        shutil.copyfile(source_path, destination_path)
        print("file copied successfully !!!")
    except FileNotFoundError:
        print("The file was not found in the shared path.")
    except Exception as e:
        print(f"Error copying file: {str(e)}")

def main():   
    while True:
        get_file_samba()
        print("Sleeping for 24h ..... bye")
        time.sleep(86400)
   
if __name__ == "__main__":
    main()

