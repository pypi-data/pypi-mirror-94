import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
from urllib.request import urlopen
from googletrans import Translator
import os
import webbrowser
import subprocess

def jeff():


    global name
    name = 'Gauthier'
    wikipedia.set_lang("fr")
    inutile=["peux-tu","va","sur",'non','enfin',"c'est-à-dire que","la","le","une",'un','et','mes']

    def boot():
        talk("Bonjour, je suis votre assisstant jeff, conçu par un grand chercheur je me mets à votre service, Quel votre nom ?")
        name = take_command()

    def salutations():
        hour = int(datetime.datetime.now().hour)
        if hour>= 0 and hour<10:
            talk(f"Bonjour{name}, j'espère que vous avez passez une bonne nuit !")
    
        elif hour>= 10 and hour<18:
            talk(f"Bonjour {name} !")   
    
        else:
            talk(f"Bonsoir {name} !")  

    def rencontrebasique():
        talk(f"Bonjour {name}, mon processeur se porte bien merci de votre préoccupation ! Et vous comment allez vous?")
        command = take_command()
        if False in command :
            talk ('Bon je suis à votre service')    
            return False
        if "bien" in command or "ça va" in command:
            talk("Tout va bien alors !")
        elif "bof" in command or "mal" in command or "ne va" in command or "pas" in command:
            talk("Bon demain sera un meilleur jour !")
        else :
            talk('Bon je suis à votre service')

    def internet():
        try:
            urlopen('https://www.google.fr', timeout=1)
            print("Connecté")
            return True
        except:
            print("Déconnecté")
            return False

    def decorecointernet():
        os.popen("networksetup -setairportpower en0 off")
        time.sleep(0.5)
        os.popen("networksetup -setairportpower en0 on")
        print('Connexion...')
        time.sleep(9)
        if internet():
            talk("Je suis de nouveau connecté à Internet, je suis à votre service")
        else :
            talk("La connexion semble compromise... Je n'ai pas accès à Internet")

    def talk(text):
        voice = pyttsx3.init()
        print("A.I : " + text)
        voice.say(text)
        voice.runAndWait()

    def take_command():
        r = sr.Recognizer()
        r.energy_threshold = 5000
        pas_compris = "Désolé, je n'ai pas compris ."
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 0.8
            print(".... ")
            audio = r.listen(source)
            if internet():
                try:
                    vocal = r.recognize_google(audio, language = 'fr-FR')
                    vocal = vocal.lower()
                    print(vocal)
                    return vocal
                except sr.UnknownValueError:
                    print("veille")
                    return False
            else:
                talk("Je ne suis pas connecté à internet, je vais essayer de régler le problème...")
                decorecointernet()

    def run_jeff():
        global name
        command = take_command()

        if command == False:
            command = ""

        if "jeff" in command:
            command = command.replace("jeff","")

            if 'mets à jour' in command or "mets-toi à jour" in command or "remets-toi à jour" in command :
                os.popen("python3 /Users/gauthierbassereau/Documents/Programmation/AI/Jeff.py")
                talk("Mise à jour en cours")
                exit()

            elif 'redémarre le wifi'in command or "wifi" in command :
                decorecointernet()
            
            elif "quitte tout" in command:
                os.popen("killall 'Safari'")
                os.popen("killall 'League Of Legends'")
                os.popen("killall 'Visual Studio Code'")
                talk("Adieu")
                exit()

            elif 'terminal' in command :
                command = command.replace('tape dans','')
                command = command.replace('écris dans','')
                command = command.replace('va','')
                command = command.replace('dans','')
                command = command.replace('terminale','')
                try:
                    subprocess.call(['gnome-terminal', '-x', 'python bb.py'])
                except:
                    pass

            elif 'ouvre' in command or 'va sur' in command:
                command = command.replace('va sur','')
                command = command.replace('ouvre','')
                command = command.replace('chercher','')
                command = command.replace('sur','')
                command = command.replace(' ','')
                os.popen(f"open -a {command}.app")
                subcmd=os.popen('ls ./','r')
                if subcmd != None:
                    command = command.replace(" ", "")
                    try:
                        webbrowser.open("http://www."+command+".com", new = 2)
                    except:
                        talk("désolé je n'ai pas trouvé ni un site avec ce nom ni une application... Je vais chercher sur internet")


            elif 'youtube' in command or 'joue' in command or 'vidéo' in command or 'musique' in command:
                command = command.replace('joue','')
                command = command.replace('vidéo','')
                command = command.replace('musique','')
                for i in range(len(inutile)):
                    command = command.replace(inutile[i],'')
                if 'recherche' in command or 'cherche' in command and 'youtube' in command :
                    command = command.replace(" ","")
                    command = command.replace("cherche","")
                    command = command.replace("recherche","")
                    command = command.replace("re","")
                    try:
                        webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(command), new = 2)
                    except:
                        talk("désolé la recherche à recontrer un problème...")
                    
                else :
                    command = command.replace('youtube','')
                    pywhatkit.playonyt(command)
                    
            elif 'cherche' in command or 'recherche' in command or 'google' in command:
                command = command.replace("google","")
                command = command.replace("cherche","")
                command = command.replace("recherche","")
                command = command.replace(" ","")
                command = command.replace("re","")
                for i in range(len(inutile)):
                    command = command.replace(inutile[i],'')
                webbrowser.open("https://www.google.com/search?q=" + "+".join(command), new = 2)

            elif 'wikipedia' in command or 'qui' in command :
                command = command.replace("wikipedia", '')
                command = command.replace("qui", '')
                command = command.replace("est", '')
                try:
                    info = wikipedia.summary(command, 3)
                    talk("Voici ce que j'ai trouvé")
                    time.sleep(0.5)
                    talk(info)
                except:
                    talk("Désolé je n'ai pas réussi à trouver la page wikipedia correspondant cependant voici ce que j'ai trouvé sur le web :")
                    try:
                        webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(command), new = 2)
                    except:
                        talk("La recherche n'a rien donné non plus...")
        

            elif "stop" in command:
                talk("je vais au dodo")
                exit()

            elif 'heure' in command:
                heure= datetime.datetime.now().strftime('%H')
                minute= datetime.datetime.now().strftime('%M')
                talk('il est ' +hours+' et '+minutes+'minutes')

            elif 'merci' in command :
                talk('Votre plaisir est ma seule préoccupation')

            elif 'bonjour' in command or 'comment vas-tu' in command or 'nouvelles' in command or 'salut' in command or 'coucou' in command or 'bonsoir' in command or "vas bien" in command :
                command = command.replace("bonjour","")
                command = command.replace("salut","")
                command = command.replace("coucou","")
                command = command.replace("bonsoir","")
                command = command.replace(" ","")
                if command!=None:
                    rencontrebasique()
                if command == None:
                    salutations()

            elif "je m'appelle" in command :
                command = command.replace("je m'appelle","")
                for i in range(len(inutile)):
                    command = command.replace(inutile[i],'')
                name = command

            elif "allô" in command or "jeff" in command :
                talk(f'Je suis encore là {name}')


            else : 
                talk("Je n'ai pas réussi à traiter votre demande")
                pass
        else:
            pass

    #boot() 
    run = True
    while True:
        while run :
            run_jeff()
        