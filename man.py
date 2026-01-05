import speech_recognition as sr # распознает речи
import os
import subprocess # запускает приложения
import webbrowser # запускает сайты в браузере

apps = {
    "блокнот": "notepad.exe",
    "проводник": "explorer.exe",
    "ярость": r"C:\Games\Rage\RAGE64.exe",
    "впн": r"C:\Program Files\AdGuardVpn\AdGuardVpn.Launcher.exe",
    "vpn": r"C:\Program Files\AdGuardVpn\AdGuardVpn.Launcher.exe",
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "браузер": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "telegram": r"C:\Users\leonb\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "zona": r"C:\Program Files\Zona\Zona.exe",
    "cs": r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    "блендер": r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe",
    "амнезию": "C:\Program Files\AmneziaVPN\AmneziaVPN.exe",
}


def recognize_speech():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите команду...")
        r.pause_threshold = 0.5
        r.energy_threshold =  300
        r.dynamic_energy_adjustment_damping = True 
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
   
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Речь не распознана")
    except sr.RequestError:
        print("Ошибка сервиса распознания")
    return ""
while True:
    command = recognize_speech()

    if command =="":
        continue
    elif "открой" in command:
        app_name = command.replace("открой", "").strip()
        if app_name in apps:
            try:
                subprocess.Popen(apps[app_name])
                print(f"Открываю {app_name}")
            except FileNotFoundError:
                print(f"Приложение {app_name} не найдено")
        else:
            print("Приложение не найдено в списке")
    elif "останови" in command or "выход" in command:
        break

print("Задача выполнена")


        


