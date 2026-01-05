import speech_recognition as sr
import subprocess
from gtts import gTTS
import pygame
import io
import threading
import time
import os
import tempfile
import webbrowser

# Глобальный словарь для отслеживания временных файлов
temp_files = []

def cleanup_temp_files():
    """Очистка временных файлов при завершении"""
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except (OSError, PermissionError, FileNotFoundError) as e:
            print(f"Не удалось удалить {temp_file}: {e}")

def speak(text):
    """Озвучивание через Google TTS с улучшенной обработкой файлов"""
    print(f"Ассистент: {text}")
    try:
        tts = gTTS(text=text, lang='ru') # создает объект Google Text-to-Speech:
        
        # Создаем временный файл с уникальным именем
        fd, temp_file = tempfile.mkstemp(suffix='.mp3')
        os.close(fd) 
        tts.save(temp_file)
        temp_files.append(temp_file)
        
        # Воспроизводим в отдельном потоке
        def play_audio():
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Ждем окончания воспроизведения
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                   # Освобождаем ресурсы
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                
                # Даем немного времени перед удалением файла
                time.sleep(0.5)
                
                # Удаляем файл если существует
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    if temp_file in temp_files:
                        temp_files.remove(temp_file)

            except Exception as e:
                print(f"Ошибка воспроизведения: {e}")
            
        
        # Запускаем воспроизведение в отдельном потоке
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.daemon = True
        audio_thread.start()
        
    except Exception as e:
        print(f"Ошибка создания аудио: {e}")

# Регистрируем очистку при завершении программы
import atexit
atexit.register(cleanup_temp_files)

# Словарь приложений
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

web_sites = {
    "криптовалюту": "https://ru.tradingview.com/chart/NSWcyp2r/?symbol=PEPPERSTONE%3AGER40",
    "аниме": "https://animego.me/anime",
    "чат": "https://chat.deepseek.com/",
    "бин": "https://bingx.com/ru-ru/perpetual/ETH-USDT",
    "переводчик":"https://translate.google.com/?hl=ru&sl=en&tl=ru&op=translate",
    }

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        time.sleep(4)
        speak("Скажите команду...")
        r.pause_threshold = 0.8
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        time.sleep(2)
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        time.sleep(2)
        print("Речь не распознана")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")
    return ""

# Запуск ассистента
speak("Голосовой помощник запущен")

# Основной цикл
while True:
    command = recognize_speech()

    if not command:
        continue
        
    if "открой" in command:
        app_name = command.replace("открой", "").strip()

        if app_name in web_sites:
            try:
                speak(f"Открываю {app_name}")
                time.sleep(2)
                webbrowser.open(web_sites[app_name])
            except Exception as e:
                speak(f"Ошибка при запуске {app_name}")
        
        if app_name in apps:
            try:
                speak(f"Открываю {app_name}")
                time.sleep(2)  # Пауза перед запуском приложения
                subprocess.Popen(apps[app_name])
            except Exception as e:
                speak(f"Ошибка при запуске {app_name}")
                print(f"Ошибка: {e}")
            
    elif "стоп" in command or "останови" in command or "выход" in command:
        speak("Завершаю работу. До свидания!")
        time.sleep(3)
        break
        
    elif "привет" in command:
        speak("Привет! Чем могу помочь?")
        
    elif "как дела" in command:
        speak("Всё отлично, готов выполнять ваши команды!")
    
    elif "сделай паузу" in command:
        speak("Будет исполнено")
        time.sleep(300)

# Очистка при выходе
cleanup_temp_files()
print("Программа завершена")