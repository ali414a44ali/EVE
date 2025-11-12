from telethon import events
from storage import storage
import re

async def handle_auto_reply(event):
    """معالجة الردود التلقائية"""
    if not event.is_private:
        return
    
    # التحقق من الاشتراك في القناة
    channel_link = storage.get("channel_link")
    if channel_link and not await is_subscribed(event.sender_id, event.client):
        await event.reply(f"يجب الاشتراك في القناة أولاً: {channel_link}")
        await event.delete()
        return
    
    # الردود المخصصة
    responses = storage.get_responses()
    message_text = event.raw_text.lower()
    
    for keyword, response_data in responses.items():
        if keyword in message_text:
            await send_response(event, response_data)
            break

async def send_response(event, response_data):
    """إرسال الرد المناسب"""
    if isinstance(response_data, dict):
        text = response_data.get('response', '')
        photo = response_data.get('photo')
        
        if photo:
            await event.client.send_file(event.chat_id, photo, caption=text)
        else:
            await event.reply(text)
    else:
        await event.reply(response_data)

async def is_subscribed(user_id, client):
    """التحقق من اشتراك المستخدم في القناة"""
    channel_link = storage.get("channel_link")
    if not channel_link:
        return True
    
    try:
        channel_username = channel_link.replace('https://t.me/', '')
        participants = await client.get_participants(channel_username)
        return any(user.id == user_id for user in participants)
    except:
        return False