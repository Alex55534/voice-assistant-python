@echo off
echo Установка голосового ассистента...
pip install -r requirements.txt
pip install pipwin
pipwin install pyaudio
echo Установка завершена!
pause
