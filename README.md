# 🎤 Голосовой помощник на Python

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Голосовой ассистент для управления компьютером с помощью речевых команд.

## ✨ Возможности

- 🎤 **Распознавание речи** через Google Speech Recognition
- 🔊 **Синтез речи** с помощью gTTS и pyttsx3
- 🚀 **Управление приложениями** — запуск и закрытие
- 🌐 **Открытие веб-сайтов** по голосовой команде
- ⚡ **Многопоточная обработка** без блокировки интерфейса
-  🎮 **Поддержка игр и программ** — Steam, Telegram, браузеры и другие
- ⚙️ **Конфигурируемые команды** через YAML-файлы

  ## 📋 Поддерживаемые команды

### Базовые команды
- **"Привет"** — приветствие
- **"Как дела?"** — проверка состояния
- **"Стоп" / "Выход"** — завершение работы
- **"Сделай паузу"** — пауза на 5 минут

### Управление приложениями
- **"Открой браузер"** — Google Chrome
- **"Открой проводник"** — проводник
- **"Откройи Steam"** — Steam клиент
- **"Открой Telegram"** — мессенджер
- **"Открой блокнот"** — текстовый редактор
- **"Открой CS-GO"** — CS:GO
- **"Открой Blender"** — 3D редактор
- **"Открой VPN"** — AdGuard VPN

### Веб-сайты
- **"Открой криптовалюту"** — TradingView графики
- **"Открой аниме"** — AnimeGo
- **"Открой чат"** — DeepSeek Chat
- **"Открой переводчик"** — Google Translate
- **"Открой бин"** — BingX

 <img width="454" height="196" alt="image" src="https://github.com/user-attachments/assets/71dd57ce-1a0c-4467-ad80-324c14f6541f" />

 ## 👣 Автор

**Шкурин Алексей Витальевич**  
*Python разработчик

- **GitHub**: (https://github.com/Alex55534)
- **Telegram**: [@Kliso3373274](https://t.me/Kliso3373274)
- **Email**: leonbarsia@yandex.ru

🎇 MIT License

Copyright (c) 2025 Alex55534

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## 🚀 Быстрый старт

### Установка
```bash
# Клонировать репозиторий
git clone https://https://github.com/Alex55534/voice-assistant-python.git
cd voice-assistant-python

# Установите зависимости
pip install -r requirements.txt

# Если возникают проблемы с PyAudio на Windows:
# 1. Установите Microsoft Visual C++ Build Tools
# 2. Или используйте: pip install pipwin && pipwin install pyaudio

# На Ubuntu/Debian сначала установите системные пакеты:
sudo apt-get install python3-pyaudio portaudio19-dev
