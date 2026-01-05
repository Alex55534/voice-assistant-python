import speech_recognition as sr
import subprocess
from gtts import gTTS
import pygame
import threading
import time
import os
import tempfile
import webbrowser
import random
import psutil
import queue
from collections import deque
import io

# Глобальные переменные
audio_queue = queue.Queue()
command_queue = queue.Queue()
is_playing_audio = False
is_processing_command = False

# Инициализация pygame один раз при запуске
pygame.mixer.init()

def cleanup():
    """Очистка при завершении"""
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass

def audio_worker():
    """Рабочий поток для воспроизведения аудио"""
    global is_playing_audio
    
    while True:
        text = audio_queue.get()
        if text is None:  # Сигнал завершения
            break
            
        is_playing_audio = True
        print(f"Ассистент: {text}")
        
        try:
            # Создаем gTTS объект
            tts = gTTS(text=text, lang='ru')
            
            # Сохраняем в временный файл
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_filename = temp_file.name
                tts.save(temp_filename)
            
            # Воспроизводим аудио
            try:
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                # Ждем окончания воспроизведения
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Даем время для завершения воспроизведения
                time.sleep(0.5)
                
            finally:
                # Всегда пытаемся удалить файл, даже если были ошибки воспроизведения
                try:
                    os.unlink(temp_filename)
                except (OSError, PermissionError):
                    # Если файл занят, планируем его удаление позже
                    threading.Timer(5.0, lambda: try_remove_file(temp_filename)).start()
                    
        except Exception as e:
            print(f"Ошибка воспроизведения аудио: {e}")
        
        is_playing_audio = False
        audio_queue.task_done()

def try_remove_file(filename, max_attempts=3):
    """Попытка удалить файл с несколькими попытками"""
    for attempt in range(max_attempts):
        try:
            if os.path.exists(filename):
                os.unlink(filename)
                return True
        except (OSError, PermissionError):
            if attempt < max_attempts - 1:
                time.sleep(1)
    return False

def command_worker():
    """Рабочий поток для обработки команд"""
    global is_processing_command
    
    while True:
        command_data = command_queue.get()
        if command_data is None:  # Сигнал завершения
            break
            
        is_processing_command = True
        command_type, data = command_data
        
        try:
            if command_type == "open_app":
                app_name, app_path = data
                open_application(app_name, app_path)
            elif command_type == "open_website":
                site_name, url = data
                open_website(site_name, url)
            elif command_type == "close_app":
                app_name = data
                close_application(app_name)
            elif command_type == "close_browser":
                site_name = data
                close_browser_tab(site_name)
                
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")
            speak(f"Ошибка при выполнении команды")
        
        is_processing_command = False
        command_queue.task_done()

def speak(text):
    """Добавление текста в очередь на озвучивание"""
    audio_queue.put(text)

# Запускаем рабочие потоки при импорте
audio_thread = threading.Thread(target=audio_worker, daemon=True)
audio_thread.start()

command_thread = threading.Thread(target=command_worker, daemon=True)
command_thread.start()

# Регистрируем очистку при завершении программы
import atexit
atexit.register(cleanup)

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
    "амнезию": r"C:\Program Files\AmneziaVPN\AmneziaVPN.exe",
}

web_sites = {
    "криптовалюту": "https://ru.tradingview.com/chart/NSWcyp2r/?symbol=PEPPERSTONE%3AGER40",
    "аниме": "https://animego.me/anime",
    "чат": "https://chat.deepseek.com/",
    "бин": "https://bingx.com/ru-ru/perpetual/ETH-USDT",
    "переводчик":"https://translate.google.com/?hl=ru&sl=en&tl=ru&op=translate",
}

app_paths_to_names = {path: name for name, path in apps.items()}

# Словарь для отслеживания запущенных процессов
running_processes = {}
# Очередь для быстрых команд (приоритетные)
fast_command_queue = deque()

def open_application(app_name, app_path):
    """Открыть приложение (выполняется в отдельном потоке)"""
    try:
        process = subprocess.Popen(app_path)
        running_processes[app_name] = process
        speak(f"Успешно открыл {app_name}")
    except Exception as e:
        print(f"Ошибка при запуске {app_name}: {e}")
        speak(f"Ошибка при запуске {app_name}")

def open_website(site_name, url):
    """Открыть веб-сайт (выполняется в отдельном потоке)"""
    try:
        webbrowser.open(url)
        speak(f"Успешно открыл {site_name}")
    except Exception as e:
        print(f"Ошибка при открытии {site_name}: {e}")
        speak(f"Ошибка при открытии {site_name}")

def recognize_speech():
    """Распознавание речи с проверкой, не воспроизводится ли сейчас аудио"""
    # Не слушаем, если воспроизводится аудио или обрабатывается команда
    if is_playing_audio or is_processing_command:
        return ""
        
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1.0
        r.energy_threshold = 400
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Речь не распознана")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")
    return ""

def find_process_by_name(process_name):
    """Найти процесс по имени"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print(f"Ошибка поиска процесса: {e}")
    return None

def close_application(app_name):
    """Закрыть приложение по имени (выполняется в отдельном потоке)"""
    try:
        # Сначала проверяем запущенные процессы через наш ассистент
        if app_name in running_processes:
            process = running_processes[app_name]
            try:
                process.terminate()
                def wait_and_clean():
                    try:
                        process.wait(timeout=2)
                    except:
                        try:
                            process.kill()
                            process.wait(timeout=1)
                        except:
                            pass
                    finally:
                        if app_name in running_processes:
                            del running_processes[app_name]
                
                threading.Thread(target=wait_and_clean, daemon=True).start()
                speak(f"Закрываю {app_name}")
                return True
            except Exception as e:
                print(f"Ошибка закрытия процесса {app_name}: {e}")
        
        # Если не нашли в running_processes, ищем по имени процесса
        app_process_names = {
            "блокнот": "notepad.exe",
            "проводник": "explorer.exe",
            "steam": "steam.exe",
            "браузер": "chrome.exe",
            "telegram": "telegram.exe",
            "zona": "zona.exe",
            "cs": "cs2.exe",
            "блендер": "blender.exe",
            "амнезию": "AmneziaVPN.exe",
            "впн": "AdGuardVpn.Launcher.exe",
            "vpn": "AdGuardVpn.Launcher.exe",
            "ярость": "RAGE64.exe",
        }
        
        if app_name in app_process_names:
            process_name = app_process_names[app_name]
            proc = find_process_by_name(process_name)
            if proc:
                try:
                    proc.terminate()
                    speak(f"Закрыл {app_name}")
                    return True
                except:
                    try:
                        proc.kill()
                        speak(f"Принудительно закрыл {app_name}")
                        return True
                    except Exception as e:
                        print(f"Ошибка: {e}")
        
        speak(f"Не удалось найти или закрыть {app_name}")
        return False
        
    except Exception as e:
        print(f"Ошибка при закрытии {app_name}: {e}")
        speak(f"Ошибка при закрытии {app_name}")
        return False

def close_browser_tab(site_name):
    """Закрыть вкладку браузера"""
    try:
        if site_name in web_sites:
            speak(f"Для закрытия вкладки {site_name} используйте Ctrl+W")
            return True
        else:
            speak(f"Не знаю сайт {site_name}")
            return False
    except Exception as e:
        print(f"Ошибка при закрытии вкладки: {e}")
        speak("Не удалось закрыть вкладку")
        return False

def process_fast_commands():
    """Обработка быстрых команд (приоритетных)"""
    while fast_command_queue:
        command = fast_command_queue.popleft()
        if "стоп" in command or "останови" in command or "выход" in command:
            return "exit"
        elif "привет" in command:
            speak("Привет! Чем могу помочь?")
        elif "как дела" in command:
            speak("Всё отлично, готов выполнять ваши команды!")
    return None

# Запуск ассистента
speak("Голосовой помощник запущен")

# Основной цикл
try:
    while True:
        # Обрабатываем быстрые команды в первую очередь
        result = process_fast_commands()
        if result == "exit":
            break
            
        # Небольшая пауза для снижения нагрузки на CPU
        time.sleep(0.05)
        command = recognize_speech()

        if not command:
            continue

        if any(word in command for word in ["стоп", "останови", "выход", "привет", "как дела"]):
            fast_command_queue.append(command)
            continue
        
        if "открой" in command:
            app_name = command.replace("открой", "").strip()

            if app_name in web_sites:
                speak(f"Открываю {app_name}")
                command_queue.put(("open_website", (app_name, web_sites[app_name])))
            
            elif app_name in apps:
                speak(f"Открываю {app_name}")
                command_queue.put(("open_app", (app_name, apps[app_name])))
            else:
                speak(f"Не знаю приложение или сайт: {app_name}")

        elif "закрой" in command or "закрыть" in command:
            target_name = command.replace("закрой", "").replace("закрыть", "").strip()
        
            # Пытаемся закрыть приложение
            command_queue.put(("close_app", target_name))

        elif "стоп" in command or "останови" in command or "выход" in command:
            speak("Завершаю работу. До свидания!")
            time.sleep(3)
            break
        
        elif any(word in command for word in ["привет", "здравствуй", "эй крошка"]):
            responses = ["Мой любимый вернулся!", "Здравствуйте!", "я люблю тебя"]
            speak(random.choice(responses))
        
        elif any(phrase in command for phrase in ["как дела", "как ты", "что нового"]):
            responses = ["Всё отлично, готов выполнять ваши команды!", 
                    "Работаю в штатном режиме!", "Всё хорошо, спасибо!"]
            speak(random.choice(responses))
    
        elif "сделай паузу" in command:
            speak("Будет исполнено")
            time.sleep(300)

        else:
            speak("Не понял команду. Попробуйте еще раз.")

except KeyboardInterrupt:
    speak("Программа прервана")

finally:
    speak("Завершаю работу. До свидания!")
    time.sleep(1)
    
    # Останавливаем рабочие потоки
    audio_queue.put(None)
    command_queue.put(None)
    
    # Даем время на завершение
    time.sleep(2)
    
    # Очистка
    cleanup()
    print("Программа завершена")