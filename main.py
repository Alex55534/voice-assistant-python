
import speech_recognition as sr
import os
import subprocess
import webbrowser

# Словарь с приложениями и их путями
apps = {
    "блокнот": "notepad.exe",
    "калькулятор": "calc.exe",
    "проводник": "explorer.exe",
    "браузер": "chrome.exe",  # Укажите путь к вашему браузеру
    "пайнт": "mspaint.exe",
    "слова": "winword.exe",
    "ярость": "RAGE64.exe",  # Для Microsoft Word
}

# Функция для распознавания речи
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите команду...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Речь не распознана")
    except sr.RequestError:
        print("Ошибка сервиса распознавания")
    return ""

# Основной цикл программы
while True:
    command = recognize_speech()
    
    if command == "":
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
    elif "останови" in command:
        break

print("Программа завершена")
