import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import os

os.environ["DISCORD_INSTANCE_NO_VOICE"] = "true"

TOKEN = '520bf0081246e737949371ade9948d953d512d4ebfefd08c6b02730fc1f001b5'  # Сюда вставите токен

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

DATA_FILE = 'time_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            'real_start': datetime.now().isoformat(),
            'game_start': datetime(764, 1, 1, 0, 0, 0).isoformat(),
            'speed': 2.0
        }
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

data = load_data()

def get_game_time():
    real_start = datetime.fromisoformat(data['real_start'])
    game_start = datetime.fromisoformat(data['game_start'])
    speed = data['speed']
    real_delta = (datetime.now() - real_start).total_seconds()
    game_delta = real_delta / speed
    return game_start + timedelta(seconds=game_delta)

@bot.command()
async def time(ctx):
    gt = get_game_time()
    await ctx.send(f'🕰️ **Игровое время:** {gt.strftime("%Y-%m-%d %H:%M:%S")}')

@bot.command()
@commands.has_permissions(administrator=True)
async def set_time(ctx, year: int, month: int, day: int, hour: int, minute: int):
    new_game_start = datetime(year, month, day, hour, minute)
    data['real_start'] = datetime.now().isoformat()
    data['game_start'] = new_game_start.isoformat()
    save_data(data)
    await ctx.send(f'✅ Время установлено на {new_game_start.strftime("%Y-%m-%d %H:%M:%S")}')

bot.run(TOKEN)
