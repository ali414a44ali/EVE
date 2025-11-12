from telethon import events
from storage import storage

async def handle_protection(event):
    """معالجة إعدادات الحماية"""
    if event.is_private:
        await handle_private_protection(event)
    else:
        await handle_group_protection(event)

async def handle_private_protection(event):
    """حماية الخاص"""
    protection_enabled = storage.get("private_protection", False)
    
    if not protection_enabled:
        return
    
    # قائمة الكلمات الممنوعة
    banned_words = storage.get("banned_words", [])
    message_text = event.raw_text.lower()
    
    for word in banned_words:
        if word in message_text:
            await event.delete()
            await warn_user(event)
            break

async def handle_group_protection(event):
    """حماية المجموعات"""
    chat_id = event.chat_id
    settings = storage.get_protection_settings(chat_id)
    
    if not settings:
        return
    
    # التحقق من أنواع المحتوى الممنوعة
    if settings.get('photos') and event.photo:
        await event.delete()
        await event.respond("❌ الصور غير مسموحة هنا!")
    
    elif settings.get('links') and 'http' in event.raw_text:
        await event.delete()
        await event.respond("❌ الروابط غير مسموحة هنا!")

async def warn_user(event):
    """تحذير المستخدم"""
    user_id = event.sender_id
    warnings = storage.get(f"warnings_{user_id}", 0) + 1
    storage.set(f"warnings_{user_id}", warnings)
    
    if warnings >= 3:
        await event.client.kick_participant(event.chat_id, user_id)
        await event.respond(f"🚫 تم حظر المستخدم بسبب تكرار المخالفات")
    else:
        await event.respond(
            f"⚠️ تحذير {warnings}/3\n"
            f"يرجى تجنب استخدام الكلمات غير اللائقة"
        )