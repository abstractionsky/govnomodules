import os
import logging
import pickle
from telethon import events, functions, types
from help_registry import help_registry

logger = logging.getLogger(__name__)
BACKUP_FILE = "profile_backup.pkl"

async def backup_current_profile(client):
    try:
        me = await client.get_me()
        full_user = await client(functions.users.GetFullUserRequest(me))
        
        profile = {
            'first_name': me.first_name,
            'last_name': me.last_name,
            'about': full_user.full_user.about,
            'photo': await client.download_profile_photo(me, file=bytes())
        }
        
        with open(BACKUP_FILE, 'wb') as f:
            pickle.dump(profile, f)
            
        return True
    except Exception as e:
        logger.error(f"Backup error: {str(e)}")
        return False

async def clone_profile_handler(event):
    try:
        if event.sender_id != event.client.owner_id:
            await event.delete()
            return

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

        if not await backup_current_profile(event.client):
            await event.reply("❌ Ошибка создания резервной копии")
            return

        full_user = await event.client(functions.users.GetFullUserRequest(target))
        await event.client(functions.account.UpdateProfileRequest(
            first_name=target.first_name or "",
            last_name=target.last_name or "",
            about=full_user.full_user.about
        ))

        if target.photo:
            photo = await event.client.download_profile_photo(target, file=bytes())
            await event.client(functions.photos.UploadProfilePhotoRequest(
                file=await event.client.upload_file(photo)
            )

        await event.reply("✅ Профиль успешно скопирован! Используйте .restoreprofile для отмены")

    except Exception as e:
        await event.reply(f"❌ Ошибка: {str(e)}")

async def restore_profile_handler(event):
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
            )

        os.remove(BACKUP_FILE)
        await event.reply("✅ Профиль восстановлен")

    except Exception as e:
        await event.reply(f"❌ Ошибка восстановления: {str(e)}")

async def register(client):
    client.add_event_handler(
        clone_profile_handler,
        events.NewMessage(pattern=r"^\.stealprofile(?:\s+(\d+|@\w+)|$")
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
