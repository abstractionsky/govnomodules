import logging
from telethon import events
from modules import owner_only
from help_registry import help_registry

logger = logging.getLogger(__name__)
zaebal_mode = False

@owner_only
async def zaebal_command(event):
    global zaebal_mode
    args = event.pattern_match.group(1).lower()
    
    if args == "on":
        zaebal_mode = True
        await event.edit("✅ Режим **ZAEBAЛ** активирован!")
    elif args == "off":
        zaebal_mode = False
        await event.edit("⛔ Режим **ZAEBAЛ** выключен")
    else:
        await event.edit("❌ Используйте: `.zaebal [on/off]`")

async def message_modifier(event):
    global zaebal_mode
    if zaebal_mode == True:
        text = event.raw_text
        if text and not text.startswith("."):
            try:
                await event.edit(f"{text} заебал")
            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")

async def register(client):
    client.add_event_handler(
        zaebal_command,
        events.NewMessage(pattern=r"^\.zaebal\s+(on|off)$")
    )
    client.add_event_handler(
        message_modifier,
        events.NewMessage(outgoing=True)
    )
    help_registry.register_command(
        command=".zaebal [on/off]",
        description="Заебал"
    )
