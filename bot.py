import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from datetime import datetime, timedelta
import asyncio
import os

API_TOKEN = '7533535042:AAFOL25oLPK8UZ1XFNtnXcY-ihvL_yOJhZY'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

lembretes = []

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("""✅ Envie a mensagem no formato:
`AAAA-MM-DD HH:MM texto do lembrete`

Exemplo:
`2025-06-08 14:30 Tomar remédio`""", parse_mode="Markdown")

@dp.message_handler()
async def receber_lembrete(msg: types.Message):
    try:
        partes = msg.text.split(" ", 2)
        if len(partes) < 3:
            raise ValueError("Formato inválido")

        data_hora_str = partes[0] + " " + partes[1]
        texto = partes[2]

        horario = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")

        lembretes.append((msg.chat.id, horario, texto))
        await msg.reply("✅ Lembrete salvo com sucesso!")

    except Exception:
        await msg.reply("""❌ Formato inválido. Use:
`AAAA-MM-DD HH:MM texto do lembrete`""", parse_mode="Markdown")

async def verificador():
    while True:
        agora = datetime.now()
        for lembrete in lembretes[:]:
            chat_id, horario, texto = lembrete
            if agora >= horario:
                try:
                    await bot.send_message(chat_id, f"⏰ Lembrete:\n{texto}")
                except Exception as e:
                    print(f"Erro ao enviar mensagem: {e}")
                lembretes.remove(lembrete)
        await asyncio.sleep(30)

async def on_startup(dp):
    asyncio.create_task(verificador())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
