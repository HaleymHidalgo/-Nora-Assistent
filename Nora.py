import speech_recognition as sr
from googleapiclient.discovery import build
import pyttsx3, webbrowser, subprocess

name = "nora" #Nombre que activa el asistente
engine = pyttsx3.init() #Motor de voz
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[1].id) #Escoger la voz
engine.setProperty("pause", 0.5)
engine.setProperty("rate", 125) #Velocidad a la que habla

#Credencial YT
API_KEY = 'AIzaSyAarCRSO9eU8LvI08MV90euKKLchPstTFI'

#Speaker
def talk(some_text):
    engine.say(some_text)
    engine.runAndWait()

#Escucha
def listen():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Nora: escuchando...")
            listener.adjust_for_ambient_noise(source) #Suprime el ruido de ambiente
            pc = listener.listen(source) #Guarda el audio
            rec = listener.recognize_google(pc, language="es") #Transforma el audio en texto
            rec = rec.lower() #Texto en Minuscula
    except sr.UnknownValueError:
        print("Nora: reintentando")
    return rec

#Principal
def run_nora():
    while True:
        try:
            rec = listen() #guarda el texto
            print(f"Yo: {rec}")
        except UnboundLocalError:
            continue
        #Si en el texto esta el nombre
        if name in rec:
            talk(" dime")
            print("Nora: Dime...")
            #Las funciones
            while True:
                try:
                    rec = listen() #guarda el texto
                    print(f"Yo: {rec}")
                except UnboundLocalError:
                    talk(" ¿Podrias repetirlo?")
                    print("Nora: ¿Podrias repetirlo?")
                    continue

                #Saluda
                if "hola" in rec:
                    print("Nora: Hola, ¿Como estas?")
                    talk(" Hola, ¿Como estas?")

                elif "cómo estás" in rec:
                    print("Nora: en proceso de creacion actualmente, pero bien")
                    talk(" En proceso de creacion actualmente, pero bien")

                #abre 
                elif "abre" in rec:
                    #Elimina la palabra
                    accion = rec.replace("abre", "").strip()

                    #Microsoft - Egde
                    if "edge" in accion:
                        edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' #Asigna la ruta
                        webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))  #Registra el navegador
                        webbrowser.get('edge').open("https://www.google.com")
                        talk(" Abriendo el navegador")
                        print("Nora: Abriendo el navegador")

                    #Google - Chrome
                    if "chrome" in accion:
                        chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
                        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                        webbrowser.get('chrome').open("https://www.google.com")
                        talk(" Abriendo el navegador")
                        print("Nora: Abriendo el navegador")

                    #OperaGX
                    if "opera gx" in accion:
                        opera_path = r"C:\Users\haley\AppData\Local\Programs\Opera GX\launcher.exe"
                        webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))
                        webbrowser.get('opera').open("https://www.google.com")
                        talk(" Abriendo el navegador")
                        print("Nora: Abriendo el navegador")

                    #Steam
                    if "steam" in accion:
                        app_path = r"C:\Program Files (x86)\Steam\steam.exe" #Asigna la ruta
                        subprocess.Popen(app_path) #Abre la app de la ruta
                        talk(" Abriendo Steam")
                        print("Nora: Abriendo Steam")

                #Búsqueda de video en YouTube
                elif "busca en youtube" in rec:
                    query = rec.replace("busca en youtube", "").strip()
                    youtube = build('youtube', 'v3', developerKey=API_KEY) #Usa el objeto para interactiar con la API de YT
                    #Crea una solicitud de busqueda 
                    request = youtube.search().list(
                        part='snippet',
                        q=query,
                        type='video',
                        maxResults=1
                    )
                    response = request.execute() #Solicia una busqueda
                    video_id = response['items'][0]['id']['videoId']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    webbrowser.get('chrome').open(video_url)
                    talk(f" Abriendo video en YouTube")
                    print(f"Abriendo video en YouTube.")
                
                elif "quiero escuchar" in rec:
                    query = rec.replace("quiero escuchar", "").strip()
                    youtube = build('youtube', 'v3', developerKey=API_KEY)
                    request = youtube.search().list(
                        part='snippet',
                        q=query,
                        type='video',
                        maxResults=1
                    )
                    response = request.execute()
                    video_id = response['items'][0]['id']['videoId']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    webbrowser.get('chrome').open(video_url)
                    talk(" Reproduciendo.")
                    print("Nora: Reproduciendo.")

                #Cierra el programa
                elif "esperando" in rec:
                    print("Nora: Esta bien")
                    talk(" Esta bien")
                    break

                #En caso de que la pregunta no exista, que diga
                else:
                    print("Nora: Comando no encontrado")
                    talk("Comando no encontrado")
        elif "buenas noches" in rec:
            print("Nora: Hasta pronto.")
            talk(" Hasta pronto")
            break

if __name__ == "__main__":
    run_nora()