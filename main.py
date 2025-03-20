from telethon import events
from help_registry import help_registry

async def ping_handler(event):
    """Обработчик команды .ping"""
    message = await event.reply("🏓 Ping...")
    await message.edit("🏓 Pong!")

async def register(client):
    client.add_event_handler(
        ping_handler,
        events.NewMessage(pattern=r"^\.ping$")
    )
    help_registry.register_command(
        ".ping",
        "Проверка работоспособности бота (анимированный ответ)"
    )
