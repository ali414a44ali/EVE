import asyncio
import time
from datetime import datetime
from telethon import events
from telethon.tl.functions.account import UpdateProfileRequest 
from storage import storage

async def handle_utilities(event):
    """معالجة الأدوات المساعدة"""
    command = event.pattern_match.group(0)
    
    if command == '.فحص':
        await check_bot_status(event)
    
    elif command == '.بنج':
        await ping_test(event)
    
    elif command == '.معلوماتي':
        await user_info(event)
    
    elif command.startswith('.الاسم'):
        await change_name(event)

async def check_bot_status(event):
    """فحص حالة البوت"""
    start_time = time.time()
    msg = await event.edit("⏳ جاري الفحص...")
    
    # حساب البنج
    end_time = time.time()
    ping_time = (end_time - start_time) * 1000
    
    # معلومات النظام
    user = await event.client.get_me()
    
    status_text = f"""
🟢 **حالة البوت:**
• **البنج:** `{ping_time:.2f}ms`
• **المستخدم:** [{user.first_name}](tg://user?id={user.id})
• **معرف البوت:** @{user.username or 'لا يوجد'}
• **وقت التشغيل:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    await msg.edit(status_text)

async def ping_test(event):
    """اختبار سرعة البوت"""
    start = datetime.now()
    message = await event.edit("⏳ جاري قياس السرعة...")
    end = datetime.now()
    ping_time = (end - start).microseconds / 1000
    
    await message.edit(f"**سرعة الاستجابة:** `{ping_time}ms`")

async def user_info(event):
    """معلومات المستخدم"""
    user = await event.client.get_me()
    full_user = await event.client(user.id)
    
    info_text = f"""
👤 **معلومات الحساب:**
• **الاسم:** {user.first_name}
• **البايو:** {full_user.about or 'لا يوجد'}
• **المستخدم:** @{user.username or 'لا يوجد'}
• **معرف الحساب:** {user.id}
    """
    
    await event.edit(info_text)

async def change_name(event):
    """تغيير اسم الحساب"""
    try:
        new_name = event.raw_text.split('.الاسم ')[1]
        await event.client(UpdateProfileRequest(first_name=new_name))
        await event.edit(f"✅ تم تغيير الاسم إلى: {new_name}")
    except IndexError:
        await event.edit("❌ يرجى كتابة الاسم بعد الأمر: `.الاسم اسمك الجديد`")