import os
import logging
from telethon import events, functions, types
from help_registry import help_registry
from modules import owner_only

logger = logging.getLogger(__name__)
BACKUP_FILE = "profile_backup.json"

async def backup_current_profile(client):
    """Создание резервной копии текущего профиля"""
    me = await client.get_me()
    profile = {
        'first_name': me.first_name,
        'last_name': me.last_name,
        'about': await client(functions.account.GetProfileRequest())['about'],
        'photo': await client.download_profile_photo(me.id, file=bytes)
    }
    with open(BACKUP_FILE, 'wb') as f:
        f.write(profile)
    return True

@owner_only
async def clone_profile_handler(event):
    """Обработчик команды .stealprofile"""
    try:
        if event.sender_id != event.client.owner_id:
            await event.delete()
            return

        # Получаем целевого пользователя
        target = None
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            target = await reply.get_sender()
        else:
            args = event.pattern_match.group(1)
            if args:
                target = await event.client.get_entity(args)

        if not target or not isinstance(target, types.User):
            await event.reply("❌ Цель не найдена")
            return

        # Создаем резервную копию
        await backup_current_profile(event.client)

        # Копируем данные
        await event.client(functions.account.UpdateProfileRequest(
            first_name=target.first_name or "",
            last_name=target.last_name or "",
            about=(await event.client(functions.users.GetFullUserRequest(target))['about'])
        ))

        # Копируем аватарку
        if target.photo:
            photo = await event.client.download_profile_photo(target)
            await event.client(functions.photos.UploadProfilePhotoRequest(
                file=await event.client.upload_file(photo)
            ))

        # Премиум-эмодзи (только для премиум)
        if target.premium:
            await event.client(functions.account.UpdateEmojiStatusRequest(
                emoji_status=target.emoji_status
            ))

        await event.reply("✅ Профиль успешно скопирован! Используйте .restoreprofile для отмены")

    except Exception as e:
        await event.reply(f"❌ Ошибка: {str(e)}")

@owner_only
async def restore_profile_handler(event):
    """Восстановление оригинального профиля"""
    try:
        if not os.path.exists(BACKUP_FILE):
            await event.reply("❌ Резервная копия не найдена")
            return

        with open(BACKUP_FILE, 'rb') as f:
            backup = pickle.load(f)

        await event.client(functions.account.UpdateProfileRequest(
            first_name=backup['first_name'],
            last_name=backup['last_name'],
            about=backup['about']
        ))

        if backup['photo']:
            await event.client(functions.photos.UploadProfilePhotoRequest(
                file=await event.client.upload_file(backup['photo'])
            ))

        os.remove(BACKUP_FILE)
        await event.reply("✅ Профиль восстановлен")

    except Exception as e:
        await event.reply(f"❌ Ошибка восстановления: {str(e)}")

async def register(client):
    client.add_event_handler(
        clone_profile_handler,
        events.NewMessage(pattern=r"^\.stealprofile(?:\s+(\d+|\@\w+)|$")
    )
    client.add_event_handler(
        restore_profile_handler,
        events.NewMessage(pattern=r"^\.restoreprofile$")
    )
    help_registry.register_command(
        ".stealprofile [id/@username]",
        "Копирование профиля пользователя (только для владельца)"
    )
    help_registry.register_command(
        ".restoreprofile",
        "Восстановление оригинального профиля"
    )
