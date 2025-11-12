import asyncio
from telethon import events
from storage import storage

class PublishingManager:
    def __init__(self):
        self.active_tasks = {}
    
    async def start_publishing(self, event, seconds, repeat_count, text):
        """بدء النشر التلقائي"""
        chat_id = event.chat_id
        
        if chat_id in self.active_tasks:
            await event.edit("❌ هناك عملية نشر نشطة بالفعل!")
            return
        
        task = asyncio.create_task(
            self._publish_loop(event, seconds, repeat_count, text)
        )
        self.active_tasks[chat_id] = task
        
        await event.edit(f"✅ بدأ النشر كل {seconds} ثانية لـ {repeat_count} مرة")
    
    async def stop_publishing(self, event):
        """إيقاف النشر التلقائي"""
        chat_id = event.chat_id
        
        if chat_id in self.active_tasks:
            self.active_tasks[chat_id].cancel()
            del self.active_tasks[chat_id]
            await event.edit("✅ تم إيقاف النشر التلقائي")
        else:
            await event.edit("❌ لا توجد عملية نشر نشطة")
    
    async def _publish_loop(self, event, seconds, repeat_count, text):
        """حلقة النشر"""
        for i in range(repeat_count):
            try:
                await event.respond(text)
                await asyncio.sleep(seconds)
            except asyncio.CancelledError:
                break

publishing_manager = PublishingManager()

async def handle_publishing(event):
    """معالجة أوامر النشر"""
    command = event.pattern_match.group(0)
    
    if command.startswith('.تكرار') or command.startswith('.نشر'):
        parts = event.raw_text.split()
        if len(parts) >= 3:
            try:
                seconds = int(parts[1])
                count = int(parts[2])
                text = ' '.join(parts[3:]) if len(parts) > 3 else ""
                
                await publishing_manager.start_publishing(
                    event, seconds, count, text
                )
            except ValueError:
                await event.edit("❌ يجب إدخال أرقام صحيحة")
    
    elif command == '.ايقاف النشر':
        await publishing_manager.stop_publishing(event)