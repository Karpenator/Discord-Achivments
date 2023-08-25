import discord
import asyncio
from datetime import datetime, timedelta
import pytz
from flask import Flask
from threading import Thread

# создание Flask приложения
app = Flask('')

@app.route('/')
def home():
  return "Монитор активен."

# запуск Flask приложения в отдельном потоке
def run():
    app.run(host='0.0.0.0', port=8080)

# Установка временной зоны UTC+0
tz = pytz.timezone('Etc/GMT')

# Установка ID канала Достижений
achievements_channel_id = Channel ID where bot sent message 

# Установка ID сервера
guild_id = Server ID where bot sent message 

# Установка ID ролей для проверки
roles_to_check = [Role ID for scan, Role ID for scan, Role ID for scan, Role ID for scan, Role ID for scan]

# Включение intents, необходимых для получения информации о ролях и пользователях
intents = discord.Intents.default()
intents.members = True

# Установка представителя бота
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Бот успешно запущен и готов к работе')

async def check_roles():
    await client.wait_until_ready()
    
    # Получение объекта сервера по его ID
    guild = client.get_guild(guild_id)

    while not client.is_closed():
        # Установка времени проверки
        now = datetime.now(tz)
        check_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Находим канал Достижений
        achievements_channel = client.get_channel(achievements_channel_id)

        # Формируем сообщение для отправки в канал Достижений
        message = f'Достижения на {now.strftime("%d.%m.%Y")}\n'
        for role_id in roles_to_check:
            role = guild.get_role(role_id)
            if role is not None:
                # Ищем и фильтруем участников сервера с данной ролью
                members_with_role = [m for m in guild.members if role in m.roles]
                if members_with_role:
                    message += f'**{role.name}** - у пользователей: '
                    for member in members_with_role:
                        message += f'{member.mention}, '
                    message = message[:-2] + '\n'
        # Отправляем сообщение в канал Достижений
        await achievements_channel.send(message)

        # Задержка на один день
        next_check_time = check_time + timedelta(days=1)
        wait_time = (next_check_time - datetime.now(tz)).seconds
        await asyncio.sleep(wait_time)
      

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    client.loop.create_task(check_roles())
    client.run('YOUR DISCORD BOT TOKEN')
