from telethon import events
from help_registry import help_registry
from modules import owner_only
from help_registry import help_registry
import socket

@owner_only
async def getip_handler(event):
    args = event.pattern_match.group(1)
    if args:
        result = socket.gethostbyname(args)
    else:
        result = "❌ Используйте: `.getip <domain>`"

    await event.edit(result, parse_mode='markdown')

async def register(client):
    client.add_event_handler(
        getip_handler,
        events.NewMessage(pattern=r"^\.mc(?:\s+(\S+))?$")
    )
    help_registry.register_command(
        command='.getip [domain]',
        description='Получить айпи с домена'
    )
