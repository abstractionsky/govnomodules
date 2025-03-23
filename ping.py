import time
import logging
from telethon import events, functions
from help_registry import help_registry
from modules import owner_only

logger = logging.getLogger(__name__)

@owner_only
async def ping_handler(event):
    try:
        start_time = time.time()
        await event.client(functions.PingRequest(ping_id=12345))
        latency = (time.time() - start_time) * 1000
        status_emoji = "🟢" if latency < 500 else "🟡" if latency < 1000 else "🔴"
        response = (
            f"{status_emoji} **Скорость отклика Telegram**\n"
            f"• Задержка: `{latency:.2f} мс`\n"
            f"• Сервер: `{event.client.session.server_address}`"
        )
        await event.reply(response, parse_mode='markdown')
    except Exception as e:
        await event.reply(f"❌ Ошибка измерения: {str(e)}")

async def register(client):
    client.add_event_handler(
        ping_handler,
        events.NewMessage(pattern=r"^\.ping$")
    )
    help_registry.register_command(
        ".ping",
        "Проверить скорость отклика серверов Telegram"
    )
