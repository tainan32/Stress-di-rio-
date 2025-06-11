import json
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime

API_TOKEN = '7866677408:AAGk7mEN9vTsYLqhQjl1Q1ya-z6K5_tsBMY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

LEMBRETES_FILE = 'lembretes.json'

# Carregar lembretes
def carregar_lembretes():
    try:
        with open(LEMBRETES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Salvar lembretes
def salvar_lembretes(lembretes):
    with open(LEMBRETES_FILE, 'w') as f:
        json.dump(lembretes, f)

# Checagem de lembretes
async def checar_lembretes():
    while True:
        lembretes = carregar_lembretes()
        agora = datetime.now().strftime('%Y-%m-%d %H:%M')
        for user_id, user_lembretes in list(lembretes.items()):
            for lembrete in user_lembretes[:]:
                if lembrete['hora'] == agora:
                    try:
                        await bot.send_message(user_id, f"⏰ Lembrete: {lembrete['texto']}")
                    except:
                        pass
                    user_lembretes.remove(lembrete)
            lembretes[user_id] = user_lembretes
        salvar_lembretes(lembretes)
        await asyncio.sleep(60)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("✅ Envie a mensagem no formato:
`AAAA-MM-DD HH:MM texto do lembrete`
Exemplo:
`2025-06-08 14:30 Tomar remédio`", parse_mode="Markdown")

@dp.message_handler()
async def receber_lembrete(msg: types.Message):
    try:
        partes = msg.text.split(' ', 2)
        data_hora = partes[0] + ' ' + partes[1]
        datetime.strptime(data_hora, '%Y-%m-%d %H:%M')
        texto = partes[2]

        lembretes = carregar_lembretes()
        user_id = str(msg.from_user.id)
        if user_id not in lembretes:
            lembretes[user_id] = []
        lembretes[user_id].append({"hora": data_hora, "texto": texto})
        salvar_lembretes(lembretes)

        await msg.reply("✅ Lembrete salvo com sucesso!")
    except:
        await msg.reply("❌ Formato inválido. Use:
`2025-06-08 14:30 Texto do lembrete`", parse_mode="Markdown")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(checar_lembretes())
    executor.start_polling(dp, skip_updates=True)