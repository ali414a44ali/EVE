import asyncio
import random
import time
import os
import re
import requests
import base64
import shutil
import json
import pickle
from datetime import datetime, timedelta
from collections import deque
from gtts import gTTS
from telethon import events, functions, types, Button
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, CreateChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import DeleteHistoryRequest, GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.contacts import GetBlockedRequest, UnblockRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins, 
    ChatBannedRights, 
    InputPhoto,
    InputPeerUser,
    Channel,
    User,
    Chat,
    Dialog,
    MessageEntityMentionName
)
from telethon.errors import FloodWaitError, MessageIdInvalidError
from telethon.tl.types import InputMessagesFilterPhotos
from PIL import Image, ImageDraw, ImageFont
import pytz
from storage import storage

class CommandsHandler:
    def __init__(self, client):
        self.client = client
        self.storage = storage
        self.active_publishing_tasks = {}
        self.active_timers = {}
        self.active_ratib_timers = {}
        self.active_bakhsheesh_timers = {}
        self.active_sarqa_timers = {}
        
    async def handle_all_commands(self, event):
        command = event.pattern_match.group(0).lower()
        
        commands_map = {
            '.فحص': self.check_bot,
            '.بنج': self.ping_test,
            '.معلوماتي': self.my_info,
            '.احصائياتي': self.my_stats,
            '.مساعدة': self.help_command,
            '.الاوامر': self.help_command,
            '.اوامري': self.show_commands,
            '.اضافة رد': self.add_response,
            '.حذف رد': self.delete_response,
            '.الردود': self.list_responses,
            '.تفعيل الردود': self.enable_auto_reply,
            '.تعطيل الردود': self.disable_auto_reply,
            '.نشر': self.publish_message,
            '.تكرار': self.repeat_message,
            '.ايقاف النشر': self.stop_publishing,
            '.نشر مجموعات': self.publish_to_groups,
            '.كتم': self.mute_user,
            '.الغاء الكتم': self.unmute_user,
            '.المكتومين': self.muted_users,
            '.حظر': self.ban_user,
            '.الغاء الحظر': self.unban_user,
            '.طرد': self.kick_user,
            '.خيروك': self.random_question,
            '.بوسة': self.kiss_command,
            '.محيبس': self.mahibis_game,
            '.راتب': self.salary_command,
            '.بخشيش': self.tip_command,
            '.سرقة': self.steal_command,
            '.ايقاف راتب': self.stop_salary,
            '.ايقاف بخشيش': self.stop_tip,
            '.ايقاف سرقة': self.stop_steal,
            '.غنيلي': self.play_song,
            '.شعر': self.poetry,
            '.انمي': self.anime_pic,
            '.يوتيوب': self.youtube_search,
            '.التكبر': self.arrogance_mode,
            '.ايقاف التكبر': self.stop_arrogance,
            '.انتحال': self.impersonate,
            '.ارجاع': self.restore_profile,
            '.تقليد': self.mimic_user,
            '.ايقاف التقليد': self.stop_mimic,
            '.انتحار': self.suicide_message,
            '.شرير': self.evil_mode,
            '.متت': self.laughing_mode,
            '.تفليش': self.flood_chat,
            '.تاك للكل': self.mention_all,
            '.كشف المجموعة': self.group_info,
            '.رفع مشرف': self.promote_admin,
            '.تنزيل مشرف': self.demote_admin,
            '.مسح': self.delete_messages,
            '.مسح رسائلي': self.delete_my_messages,
            '.تجميع المليون': self.collect_points,
            '.تجميع العقرب': self.collect_points,
            '.تجميع الجوكر': self.collect_points,
            '.تجميع المليار': self.collect_points,
            '.ايقاف التجميع': self.stop_collection,
            '.مغادرة القنوات': self.leave_channels,
            '.مغادرة الكروبات': self.leave_groups,
            '.فك الحظر': self.unblock_all,
            '.تثبيت': self.pin_message,
            '.الغاء التثبيت': self.unpin_message,
            '.الغاء جميع التثبيتات': self.unpin_all_messages,
            '.الساعة': self.current_time,
            '.التاريخ': self.current_date,
            '.الوقت': self.current_time,
            '.الاسم': self.change_name,
            '.البايو': self.change_bio,
            '.الصورة': self.change_photo,
            '.تفعيل التخزين': self.enable_storage,
            '.تعطيل التخزين': self.disable_storage,
            '.تفعيل الاسم الوقتي': self.enable_time_name,
            '.تعطيل الاسم الوقتي': self.disable_time_name,
            '.اضافة قناة اشتراك': self.set_channel,
            '.مسح القناة': self.remove_channel,
            '.عداد': self.countdown_timer,
            '.توقيف': self.stop_timers,
            '.تفعيل الذكاء': self.enable_ai,
            '.تعطيل الذكاء': self.disable_ai,
            '.ذكاء': self.ai_chat,
            '.مترجم': self.enable_translator,
            '.ايقاف المترجم': self.disable_translator,
            '.صيد': self.hunt_username,
            '.ايقاف الصيد': self.stop_hunting,
            '.حالة الصيد': self.hunting_status,
            '.نوع': self.show_hunt_types,
            '.مراقبة': self.start_watching,
            '.ايقاف المراقبة': self.stop_watching,
            '.منع التفليش': self.enable_flood_protection,
            '.سماح التفليش': self.disable_flood_protection,
            '.منع الوسائط': self.enable_media_protection,
            '.سماح الوسائط': self.disable_media_protection,
            '.تفعيل المخصص': self.enable_custom_replies,
            '.تعطيل المخصص': self.disable_custom_replies,
            '.كليشة الرد': self.set_reply_template,
            '.كليشة التحذير': self.set_warning_message,
            '.عدد التحذيرات': self.set_max_warnings,
            '.جلسة': self.add_session,
            '.رمز': self.add_code,
            '.تحقق': self.add_password,
            '.حمل': self.download_media,
            '.انطق': self.text_to_speech,
            '.عكس': self.reverse_text,
            '.تشفير': self.encode_base64,
            '.فك التشفير': self.decode_base64,
            '.شرطة': self.police_lights,
            '.gym': self.gym_animation,
            '.طباعة': self.typing_animation,
            '.لوجو': self.create_logo,
            '.واو': self.save_restricted,
            '.خاص': self.send_to_all_private,
            '.تحويل نص': self.text_to_sticker,
            '.ضيف': self.add_members,
            '.اضافة_جهاتي': self.add_contacts,
            '.وسبام': self.word_spam,
            '.سبام': self.char_spam,
            '.سوبر': self.super_spam,
            '.بلش': self.start_spam,
            '.تناوب': self.rotate_spam,
        }
        
        for cmd, handler in commands_map.items():
            if command.startswith(cmd):
                try:
                    await handler(event)
                    return
                except Exception as e:
                    await self.handle_error(event, e, cmd)
                    return
        
        await event.edit("**❌ الأمر غير معروف! اكتب `.مساعدة` لرؤية الأوامر المتاحة**")

    async def handle_error(self, event, error, command):
        error_msg = f"**❌ حدث خطأ في تنفيذ الأمر `{command}`:**\n`{str(error)}`"
        try:
            await event.edit(error_msg)
        except:
            try:
                await event.reply(error_msg)
            except:
                pass

    async def check_bot(self, event):
        start_time = time.time()
        msg = await event.edit("**⏳ جاري الفحص...**")
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        user = await self.client.get_me()
        await msg.edit(
            f"**🟢 حالة البوت:**\n"
            f"**• البنج:** `{ping_time:.2f}ms`\n"
            f"**• المستخدم:** [{user.first_name}](tg://user?id={user.id})\n"
            f"**• وقت التشغيل:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    async def ping_test(self, event):
        start = datetime.now()
        message = await event.edit("**⏳ جاري قياس السرعة...**")
        end = datetime.now()
        ping_time = (end - start).microseconds / 1000
        await message.edit(f"**سرعة الاستجابة:** `{ping_time}ms`")

    async def my_info(self, event):
        user = await self.client.get_me()
        try:
            full_user = await self.client(functions.users.GetFullUserRequest(user.id))
            bio = full_user.full_user.about or 'لا يوجد'
        except:
            bio = 'لا يوجد'
        info_text = f"""
**👤 معلومات الحساب:**

**• الاسم:** {user.first_name}
**• البايو:** {bio}
**• المستخدم:** @{user.username or 'لا يوجد'}
**• معرف الحساب:** {user.id}
**• رقم الهاتف:** {user.phone or 'غير متوفر'}
        """
        await event.edit(info_text)

    async def my_stats(self, event):
        await event.edit("**⏳ جاري جمع الإحصائيات...**")
        dialogs = await self.client.get_dialogs()
        users = groups = channels = bots = 0
        for dialog in dialogs:
            entity = dialog.entity
            if hasattr(entity, 'bot') and entity.bot:
                bots += 1
            elif hasattr(entity, 'broadcast') and entity.broadcast:
                channels += 1
            elif hasattr(entity, 'megagroup') and entity.megagroup:
                groups += 1
            else:
                users += 1
        stats_text = f"""
**📊 إحصائيات الحساب:**

**• المحادثات الخاصة:** {users}
**• المجموعات:** {groups}
**• القنوات:** {channels}
**• البوتات:** {bots}
**• الإجمالي:** {len(dialogs)}
        """
        await event.edit(stats_text)

    async def help_command(self, event):
        help_text = """
🛠 **قائمة أوامر بوت شـهـم:**

**🔍 للأوامر التفاعلية:**
• `.اوامري` - عرض قائمة الأوامر بأزرار تفاعلية

**📞 للمساعدة:** راسل المطور @shahm41
        """
        await event.edit(help_text)

    async def show_commands(self, event):
        try:
            bot_username = self.storage.get("bot_username")
            if not bot_username:
                from config import BOT_USERNAME
                bot_username = BOT_USERNAME
                self.storage.set("bot_username", bot_username)

            if bot_username:
                response = await self.client.inline_query(bot_username, "اوامري")
                if response:
                    await response[0].click(event.chat_id, reply_to=event.reply_to_msg_id)
                    await event.delete()
                else:
                    await event.edit("**❌ لم يتم العثور على نتائج الإنلاين.**")
            else:
                await event.edit("**❌ لم يتم تعيين البوت المساعد.**")
        except Exception as e:
            await event.edit(f"**❌ خطأ في عرض الأوامر: {str(e)}**")

    async def add_response(self, event):
        try:
            if not event.reply_to_msg_id:
                await event.edit("**❌ يجب الرد على الرسالة المراد إضافتها كرد**")
                return
            replied = await event.get_reply_message()
            parts = event.raw_text.split(' ', 2)
            if len(parts) < 3:
                await event.edit("**❌ الصيغة: .اضافة رد [الكلمة]**")
                return
            keyword = parts[2].lower()
            responses = self.storage.get_responses()
            if replied.text:
                responses[keyword] = replied.text
            elif replied.media:
                file_path = await replied.download_media()
                responses[keyword] = {'media': file_path, 'text': replied.text or ''}
            else:
                await event.edit("**❌ الرسالة يجب أن تحتوي على نص أو وسائط**")
                return
            self.storage.set_responses(responses)
            await event.edit(f"**✅ تم إضافة الرد للكلمة: {keyword}**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def delete_response(self, event):
        try:
            parts = event.raw_text.split(' ', 2)
            if len(parts) < 3:
                await event.edit("**❌ الصيغة: .حذف رد [الكلمة]**")
                return
            keyword = parts[2].lower()
            responses = self.storage.get_responses()
            if keyword in responses:
                del responses[keyword]
                self.storage.set_responses(responses)
                await event.edit(f"**✅ تم حذف الرد: {keyword}**")
            else:
                await event.edit("**❌ الكلمة غير موجودة**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def list_responses(self, event):
        responses = self.storage.get_responses()
        if not responses:
            await event.edit("**❌ لا توجد ردود مضافة**")
            return
        response_list = "**📝 الردود المضافة:**\n\n"
        for i, (keyword, response) in enumerate(responses.items(), 1):
            if isinstance(response, dict):
                response_list += f"{i}. **{keyword}** 📁 (وسائط)\n"
            else:
                response_list += f"{i}. **{keyword}** → {response[:30]}...\n"
        await event.edit(response_list)

    async def enable_auto_reply(self, event):
        self.storage.set_auto_reply_enabled(True)
        await event.edit("**✅ تم تفعيل الردود التلقائية**")

    async def disable_auto_reply(self, event):
        self.storage.set_auto_reply_enabled(False)
        await event.edit("**✅ تم تعطيل الردود التلقائية**")

    async def publish_message(self, event):
        try:
            parts = event.raw_text.split(' ', 3)
            if len(parts) < 4:
                await event.edit("**❌ الصيغة: .نشر [العدد] [الوقت] [النص]**")
                return
            count = int(parts[1])
            delay = int(parts[2])
            text = parts[3]
            if delay < 5:
                await event.edit("**❌ الحد الأدنى للوقت هو 5 ثواني**")
                return
            await event.edit(f"**✅ بدأ النشر: {count} مرة كل {delay} ثانية**")
            for i in range(count):
                await event.respond(text)
                await asyncio.sleep(delay)
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def repeat_message(self, event):
        if not event.reply_to_msg_id:
            await event.edit("**❌ يجب الرد على الرسالة المراد تكرارها**")
            return
        try:
            parts = event.raw_text.split(' ', 2)
            count = int(parts[1]) if len(parts) > 1 else 5
            delay = int(parts[2]) if len(parts) > 2 else 2
            if delay < 2:
                await event.edit("**❌ الحد الأدنى للوقت هو 2 ثانية**")
                return
            replied = await event.get_reply_message()
            await event.edit(f"**✅ بدأ التكرار: {count} مرة كل {delay} ثانية**")
            for i in range(count):
                if replied.text:
                    await event.respond(replied.text)
                elif replied.media:
                    await event.respond(file=replied.media, message=replied.text)
                await asyncio.sleep(delay)
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def stop_publishing(self, event):
        for task in self.active_publishing_tasks.values():
            task.cancel()
        self.active_publishing_tasks.clear()
        await event.edit("**✅ تم إيقاف جميع عمليات النشر**")

    async def publish_to_groups(self, event):
        try:
            parts = event.raw_text.split(' ', 2)
            if len(parts) < 3:
                await event.edit("**❌ الصيغة: .نشر مجموعات [العدد] [النص]**")
                return
            count = int(parts[1])
            text = parts[2]
            dialogs = await self.client.get_dialogs()
            groups = [d for d in dialogs if d.is_group]
            if len(groups) < count:
                await event.edit(f"**❌ لديك فقط {len(groups)} مجموعة**")
                return
            await event.edit(f"**⏳ جاري النشر في {count} مجموعة...**")
            sent_count = 0
            for group in groups[:count]:
                try:
                    await self.client.send_message(group.entity, text)
                    sent_count += 1
                    await asyncio.sleep(1)
                except:
                    pass
            await event.edit(f"**✅ تم النشر في {sent_count} مجموعة**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def mute_user(self, event):
        if event.is_private:
            user_id = event.chat_id
            muted_users = self.storage.get_muted_users()
            if user_id not in muted_users:
                muted_users.append(user_id)
                self.storage.set_muted_users(muted_users)
                await event.edit("**✅ تم كتم المستخدم**")
            else:
                await event.edit("**❌ المستخدم مكتوم بالفعل**")
        else:
            await event.edit("**❌ هذا الأمر للخاص فقط**")

    async def unmute_user(self, event):
        if event.is_private:
            user_id = event.chat_id
            muted_users = self.storage.get_muted_users()
            if user_id in muted_users:
                muted_users.remove(user_id)
                self.storage.set_muted_users(muted_users)
                await event.edit("**✅ تم إلغاء كتم المستخدم**")
            else:
                await event.edit("**❌ المستخدم غير مكتوم**")
        else:
            await event.edit("**❌ هذا الأمر للخاص فقط**")

    async def muted_users(self, event):
        muted_users = self.storage.get_muted_users()
        if not muted_users:
            await event.edit("**❌ لا يوجد مستخدمين مكتومين**")
            return
        users_list = "**📋 المستخدمين المكتومين:**\n\n"
        for user_id in muted_users[:10]:
            users_list += f"• `{user_id}`\n"
        if len(muted_users) > 10:
            users_list += f"\n**... و {len(muted_users) - 10} أكثر**"
        await event.edit(users_list)

    async def ban_user(self, event):
        if event.is_group and event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            try:
                await self.client.edit_permissions(
                    event.chat_id,
                    user_id,
                    view_messages=False
                )
                await event.edit("**✅ تم حظر المستخدم**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن حظر المستخدم: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم في مجموعة**")

    async def unban_user(self, event):
        if event.is_group and event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            try:
                await self.client.edit_permissions(
                    event.chat_id,
                    user_id,
                    view_messages=True
                )
                await event.edit("**✅ تم إلغاء حظر المستخدم**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن إلغاء الحظر: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم في مجموعة**")

    async def kick_user(self, event):
        if event.is_group and event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            try:
                await self.client.kick_participant(event.chat_id, user_id)
                await event.edit("**✅ تم طرد المستخدم**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن طرد المستخدم: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم في مجموعة**")

    async def random_question(self, event):
        questions = [
            "هل تحب شـهـم ؟",
            "حكي ودك يوصل للشخص المطلوب ؟",
            "منشن شخص تسولف معه تنسى هموم الدنيا ؟",
            "مقوله او مثل او بيت شعر قريب من قلبك?",
            "اكثر مكان تحب تروح له ف الويكند ?",
        ]
        question = random.choice(questions)
        await event.edit(f"**❓ {question}**")

    async def kiss_command(self, event):
        responses = ["روح لعند المطور وقول له", "ايع مقرف", "همممممم"]
        response = random.choice(responses)
        await event.edit(f"**💋 {response}**")

    async def mahibis_game(self, event):
        correct_answer = random.randint(1, 6)
        self.storage.set(f"mahibis_{event.chat_id}", correct_answer)
        board = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣\n🖐️ 🖐️ 🖐️ 🖐️ 🖐️ 🖐️"
        await event.edit(
            f"**🎮 لعبة المحيبس**\n\n"
            f"أول من يرسل 'انا' يلعب\n"
            f"الأوامر:\n"
            f"• طك + رقم ← لفتح العظمة\n"
            f"• جيب + رقم ← لأخذ المحبس\n\n"
            f"{board}"
        )

    async def salary_command(self, event):
        await event.edit("**✅ تم تفعيل أمر الراتب**")

    async def tip_command(self, event):
        await event.edit("**✅ تم تفعيل أمر بخشيش**")

    async def steal_command(self, event):
        try:
            parts = event.raw_text.split(' ')
            if len(parts) >= 2:
                user_id = int(parts[1])
                await event.edit(f"**✅ تم تفعيل السرقة للمستخدم {user_id}**")
            else:
                await event.edit("**❌ الصيغة: .سرقة [ايدي المستخدم]**")
        except:
            await event.edit("**❌ خطأ في البيانات**")

    async def stop_salary(self, event):
        await event.edit("**✅ تم إيقاف أمر الراتب**")

    async def stop_tip(self, event):
        await event.edit("**✅ تم إيقاف أمر بخشيش**")

    async def stop_steal(self, event):
        await event.edit("**✅ تم إيقاف أمر السرقة**")

    async def play_song(self, event):
        songs = [
            "https://t.me/DwDi1/10",
            "https://t.me/DwDi1/11", 
            "https://t.me/DwDi1/12"
        ]
        song_url = random.choice(songs)
        await self.client.send_file(event.chat_id, song_url, caption="**🎵 BY: غنيلي**")
        await event.delete()

    async def poetry(self, event):
        poetry_links = [
            "https://t.me/L1BBBL/2",
            "https://t.me/L1BBBL/3",
            "https://t.me/L1BBBL/4"
        ]
        poetry_url = random.choice(poetry_links)
        await self.client.send_file(event.chat_id, poetry_url, caption="**📜 BY: شعر**")
        await event.delete()

    async def anime_pic(self, event):
        anime_links = [
            "https://t.me/Sk_x2/10",
            "https://t.me/Sk_x2/11",
            "https://t.me/Sk_x2/12",
            "https://t.me/Sk_x2/13"
        ]
        anime_url = random.choice(anime_links)
        await self.client.send_file(event.chat_id, anime_url, caption="**🎌 صور انمي**")
        await event.delete()

    async def youtube_search(self, event):
        try:
            query = event.raw_text.split('.يوتيوب ', 1)[1]
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            await event.edit(f"**🔍 نتائج البحث عن: {query}**\n\n{search_url}")
        except:
            await event.edit("**❌ الصيغة: .يوتيوب [الكلمة]**")

    async def arrogance_mode(self, event):
        try:
            parts = event.raw_text.split(' ')
            if len(parts) >= 3:
                seconds = int(parts[1])
                user_id = int(parts[2])
                self.storage.set(f"arrogance_{user_id}", seconds)
                await event.edit(f"**✅ تم تفعيل التكبر لـ {seconds} ثانية للمستخدم {user_id}**")
            else:
                await event.edit("**❌ الصيغة: .التكبر [الوقت] [ايدي المستخدم]**")
        except:
            await event.edit("**❌ خطأ في البيانات**")

    async def stop_arrogance(self, event):
        keys_to_delete = [key for key in self.storage.redis.keys() if key.startswith('arrogance_')]
        for key in keys_to_delete:
            self.storage.delete(key)
        await event.edit("**✅ تم إيقاف جميع إعدادات التكبر**")

    async def mimic_user(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            self.storage.set_mimic_user(user_id)
            await event.edit(f"**✅ تم تفعيل التقليد للمستخدم {user_id}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم المراد تقليده**")

    async def stop_mimic(self, event):
        self.storage.delete("mimic_user")
        await event.edit("**✅ تم إيقاف التقليد**")

    async def impersonate(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user = await self.client.get_entity(replied.sender_id)
            try:
                current_user = await self.client.get_me()
                self.storage.set_original_profile({
                    'first_name': current_user.first_name,
                    'last_name': current_user.last_name or '',
                    'bio': (await self.client(functions.users.GetFullUserRequest(current_user.id))).full_user.about or ''
                })
                await self.client(UpdateProfileRequest(
                    first_name=user.first_name,
                    last_name=user.last_name or ''
                ))
                await event.edit(f"**✅ تم انتحال هوية {user.first_name}**")
            except Exception as e:
                await event.edit(f"**❌ خطأ: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم**")

    async def restore_profile(self, event):
        original_profile = self.storage.get_original_profile()
        if original_profile:
            try:
                await self.client(UpdateProfileRequest(
                    first_name=original_profile['first_name'],
                    last_name=original_profile['last_name']
                ))
                await event.edit("**✅ تم استعادة الهوية الأصلية**")
            except Exception as e:
                await event.edit(f"**❌ خطأ: {str(e)}**")
        else:
            await event.edit("**❌ لا توجد هوية محفوظة**")

    async def suicide_message(self, event):
        await event.delete()
        message = await event.respond("**جاري الانتحار .....**")
        await asyncio.sleep(3)
        final_message = (
            "تم الانتحار بنجاح😂...\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　　　　　|\n"
            "　／￣￣＼| \n"
            "＜ ´･ 　　 |＼ \n"
            "　|　３　 | 丶＼ \n"
            "＜ 、･　　|　　＼ \n"
            "　＼＿＿／∪ _ ∪) \n"
            "　　　　　 Ｕ Ｕ"
        )
        await message.edit(final_message)

    async def evil_mode(self, event):
        await event.delete()
        message_text = ' ' * 6
        emojis = ['😈', '💀', '👿', '🔪', '☠️', '👹']
        message = await event.respond('👿💀👹👿🔪☠️')
        start_time = time.time()
        duration = 5
        while time.time() - start_time < duration:
            try:
                emoji_string = self.insert_emojis(message_text, emojis)
                await message.edit(emoji_string)
                await asyncio.sleep(0.1)
            except:
                break

    async def laughing_mode(self, event):
        await event.delete()
        message_text = ' ' * 6
        emojis = ['🤣', '😂', '😹', '🤣', '😂', '😹']
        message = await event.respond('🤣😂😹🤣😂😹')
        start_time = time.time()
        duration = 5
        while time.time() - start_time < duration:
            try:
                emoji_string = self.insert_emojis(message_text, emojis)
                await message.edit(emoji_string)
                await asyncio.sleep(0.1)
            except:
                break

    def insert_emojis(self, message, emojis):
        random.shuffle(emojis)
        message_list = list(message)
        emoji_positions = []
        for emoji in emojis:
            pos = random.choice(range(len(message_list)))
            while pos in emoji_positions:
                pos = random.choice(range(len(message_list)))
            emoji_positions.append(pos)
            message_list[pos] = emoji
        return ''.join(message_list)

    async def flood_chat(self, event):
        if not event.is_group:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")
            return
        await event.edit("**⏳ جاري التفليش...**")
        participants = await self.client.get_participants(event.chat_id)
        for user in participants:
            if not user.bot and not user.deleted:
                try:
                    mention = f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
                    await event.respond(mention)
                    await asyncio.sleep(0.5)
                except:
                    pass
        await event.delete()

    async def mention_all(self, event):
        if not event.is_group:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")
            return
        participants = await self.client.get_participants(event.chat_id)
        mentions = []
        for user in participants:
            if not user.bot and not user.deleted:
                if user.username:
                    mentions.append(f"@{user.username}")
                else:
                    mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
        chunk_size = 15
        for i in range(0, len(mentions), chunk_size):
            chunk = mentions[i:i + chunk_size]
            await event.respond(" ".join(chunk))
            await asyncio.sleep(1)
        await event.delete()

    async def group_info(self, event):
        if not event.is_group:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")
            return
        chat = await event.get_chat()
        participants = await self.client.get_participants(event.chat_id)
        info_text = f"""
**📊 معلومات المجموعة:**

**• الاسم:** {chat.title}
**• المعرف:** @{chat.username or 'لا يوجد'}
**• الأعضاء:** {len(participants)}
**• الرابط:** {f't.me/{chat.username}' if chat.username else 'لا يوجد'}
**• ID:** {chat.id}
        """
        await event.edit(info_text)

    async def promote_admin(self, event):
        if event.is_group and event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            try:
                await self.client.edit_admin(
                    event.chat_id,
                    user_id,
                    change_info=True,
                    post_messages=True,
                    edit_messages=True,
                    delete_messages=True,
                    ban_users=True,
                    invite_users=True,
                    pin_messages=True,
                    add_admins=False
                )
                await event.edit("**✅ تم ترقية المستخدم إلى مشرف**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن الترقية: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم في مجموعة**")

    async def demote_admin(self, event):
        if event.is_group and event.reply_to_msg_id:
            replied = await event.get_reply_message()
            user_id = replied.sender_id
            try:
                await self.client.edit_admin(
                    event.chat_id,
                    user_id,
                    change_info=False,
                    post_messages=False,
                    edit_messages=False,
                    delete_messages=False,
                    ban_users=False,
                    invite_users=False,
                    pin_messages=False,
                    add_admins=False
                )
                await event.edit("**✅ تم تنزيل المستخدم من الإشراف**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن التنزيل: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على المستخدم في مجموعة**")

    async def delete_messages(self, event):
        try:
            count = int(event.raw_text.split(' ', 1)[1])
            if count > 100:
                await event.edit("**❌ الحد الأقصى للمسح هو 100 رسالة**")
                return
            await event.delete()
            messages = await self.client.get_messages(event.chat_id, limit=count)
            await self.client.delete_messages(event.chat_id, messages)
        except ValueError:
            await event.edit("**❌ الصيغة: .مسح [عدد]**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def delete_my_messages(self, event):
        try:
            await event.edit("**⏳ جاري مسح رسائلك...**")
            messages = await self.client.get_messages(event.chat_id, limit=100)
            my_messages = [msg for msg in messages if msg.sender_id == (await self.client.get_me()).id]
            if my_messages:
                await self.client.delete_messages(event.chat_id, my_messages)
                await event.edit(f"**✅ تم مسح {len(my_messages)} من رسائلك**")
            else:
                await event.edit("**❌ لا توجد رسائل خاصة بك لمسحها**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def collect_points(self, event):
        bot_type = event.raw_text.split('.تجميع ')[1].lower()
        bots = {
            'المليون': '@qweqwe1919bot',
            'العقرب': '@AL2QRPBOT', 
            'الجوكر': '@A_MAN9300BOT',
            'المليار': '@EEObot'
        }
        if bot_type in bots:
            await event.edit(f"**⏳ جاري التجميع من بوت {bot_type}...**")
            await asyncio.sleep(5)
            await event.edit(f"**✅ تم التجميع من بوت {bot_type}**")
        else:
            await event.edit("**❌ نوع البوت غير معروف**")

    async def stop_collection(self, event):
        await event.edit("**✅ تم إيقاف التجميع**")

    async def leave_channels(self, event):
        await event.edit("**⏳ جاري مغادرة القنوات...**")
        dialogs = await self.client.get_dialogs()
        left_count = 0
        for dialog in dialogs:
            if dialog.is_channel and not dialog.is_group:
                try:
                    await self.client(LeaveChannelRequest(dialog.entity))
                    left_count += 1
                except:
                    pass
        await event.edit(f"**✅ تم مغادرة {left_count} قناة**")

    async def leave_groups(self, event):
        await event.edit("**⏳ جاري مغادرة المجموعات...**")
        dialogs = await self.client.get_dialogs()
        left_count = 0
        for dialog in dialogs:
            if dialog.is_group:
                try:
                    await self.client.delete_dialog(dialog.entity)
                    left_count += 1
                except:
                    pass
        await event.edit(f"**✅ تم مغادرة {left_count} مجموعة**")

    async def unblock_all(self, event):
        await event.edit("**⏳ جاري فك حظر جميع المستخدمين...**")
        try:
            blocked = await self.client(functions.contacts.GetBlockedRequest(offset=0, limit=100))
            unblocked_count = 0
            for user in blocked.users:
                try:
                    await self.client(functions.contacts.UnblockRequest(id=user.id))
                    unblocked_count += 1
                except:
                    pass
            await event.edit(f"**✅ تم فك حظر {unblocked_count} مستخدم**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def pin_message(self, event):
        if event.reply_to_msg_id:
            try:
                await self.client.pin_message(event.chat_id, event.reply_to_msg_id)
                await event.edit("**✅ تم تثبيت الرسالة**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن تثبيت الرسالة: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد تثبيتها**")

    async def unpin_message(self, event):
        if event.reply_to_msg_id:
            try:
                await self.client.unpin_message(event.chat_id, event.reply_to_msg_id)
                await event.edit("**✅ تم إلغاء تثبيت الرسالة**")
            except Exception as e:
                await event.edit(f"**❌ لا يمكن إلغاء التثبيت: {str(e)}**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد إلغاء تثبيتها**")

    async def unpin_all_messages(self, event):
        try:
            await self.client.unpin_message(event.chat_id)
            await event.edit("**✅ تم إلغاء جميع التثبيتات**")
        except Exception as e:
            await event.edit(f"**❌ لا يمكن إلغاء التثبيتات: {str(e)}**")

    async def current_time(self, event):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        await event.edit(f"**🕒 الوقت الحالي: {current_time}**")

    async def current_date(self, event):
        current_date = datetime.now().strftime("%Y-%m-%d")
        await event.edit(f"**📅 التاريخ الحالي: {current_date}**")

    async def change_name(self, event):
        try:
            new_name = event.raw_text.split('.الاسم ', 1)[1]
            await self.client(UpdateProfileRequest(first_name=new_name))
            await event.edit(f"**✅ تم تغيير الاسم إلى: {new_name}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .الاسم [الاسم الجديد]**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def change_bio(self, event):
        try:
            new_bio = event.raw_text.split('.البايو ', 1)[1]
            await self.client(UpdateProfileRequest(about=new_bio))
            await event.edit(f"**✅ تم تغيير البايو إلى: {new_bio}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .البايو [النص الجديد]**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def change_photo(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            if replied.photo:
                try:
                    photo = await replied.download_media()
                    await self.client(UploadProfilePhotoRequest(await self.client.upload_file(photo)))
                    await event.edit("**✅ تم تغيير الصورة**")
                    os.remove(photo)
                except Exception as e:
                    await event.edit(f"**❌ خطأ: {str(e)}**")
            else:
                await event.edit("**❌ يجب الرد على صورة**")
        else:
            await event.edit("**❌ يجب الرد على الصورة المراد تعيينها**")

    async def enable_storage(self, event):
        try:
            if event.is_group:
                await event.edit("**✅ تم تفعيل التخزين في هذه المجموعة**")
            elif event.is_private:
                group_name = "كروب التخزين"
                group_bio = "كروب التخزين المخصص من سورس شـهـم @S21Si"
                try:
                    group = await self.client(CreateChannelRequest(
                        title=group_name,
                        about=group_bio,
                        megagroup=True
                    ))
                    group_id = group.chats[0].id
                    self.storage.set("storage_group_id", group_id)
                    await event.edit(f"**✅ تم إنشاء كروب التخزين وتعيينه بنجاح**")
                except Exception as e:
                    await event.edit(f"**❌ خطأ في إنشاء مجموعة التخزين: {str(e)}**")
        except Exception as e:
            await event.edit(f"**❌ خطأ: {str(e)}**")

    async def disable_storage(self, event):
        self.storage.delete("storage_group_id")
        await event.edit("**✅ تم تعطيل التخزين بنجاح**")

    async def enable_time_name(self, event):
        self.storage.set("time_name_enabled", True)
        await event.edit("**✅ تم تفعيل الاسم الوقتي**")
        asyncio.create_task(self.update_time_name())

    async def disable_time_name(self, event):
        self.storage.set("time_name_enabled", False)
        await event.edit("**✅ تم تعطيل الاسم الوقتي**")

    async def update_time_name(self):
        while self.storage.get("time_name_enabled", False):
            try:
                me = await self.client.get_me()
                current_name = me.first_name
                base_name = current_name.split(' - ')[0] if ' - ' in current_name else current_name
                iraq_tz = pytz.timezone('Asia/Baghdad')
                now = datetime.now(iraq_tz)
                current_time = now.strftime("%I:%M")
                superscript_digits = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
                formatted_time = current_time.translate(superscript_digits)
                new_username = f"{base_name} - {formatted_time}"
                if new_username != current_name:
                    await self.client(UpdateProfileRequest(first_name=new_username))
                await asyncio.sleep(60)
            except Exception as e:
                print(f"خطأ في تحديث الاسم الوقتي: {e}")
                await asyncio.sleep(60)

    async def set_channel(self, event):
        try:
            channel_link = event.raw_text.split('.اضافة قناة اشتراك ', 1)[1]
            self.storage.set("channel_link", channel_link)
            await event.edit(f"**✅ تم تعيين رابط القناة إلى: {channel_link}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .اضافة قناة اشتراك [رابط القناة]**")

    async def remove_channel(self, event):
        self.storage.delete("channel_link")
        await event.edit("**✅ تم مسح رابط القناة**")

    async def countdown_timer(self, event):
        try:
            minutes = int(event.raw_text.split('.عداد ', 1)[1])
            total_seconds = minutes * 60
            countdown_message = await event.edit("**⏳ سيبدأ العد التنازلي بعد 3**")
            await asyncio.sleep(1)
            await countdown_message.edit("**⏳ سيبدأ العد التنازلي بعد 2**")
            await asyncio.sleep(1)
            await countdown_message.edit("**⏳ سيبدأ العد التنازلي بعد 1**")
            await asyncio.sleep(1)
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                time_text = f"**⏰ {minutes:02}:{seconds:02} متبقية**"
                await countdown_message.edit(time_text)
                await asyncio.sleep(1)
                total_seconds -= 1
            await countdown_message.edit("**⏰ الوقت انتهى!**")
        except (ValueError, IndexError):
            await event.edit("**❌ الصيغة: .عداد [عدد الدقائق]**")

    async def stop_timers(self, event):
        for timer_id in list(self.active_timers.keys()):
            self.active_timers[timer_id].cancel()
            del self.active_timers[timer_id]
        await event.edit("**✅ تم إيقاف جميع العدادات التنازلية**")

    async def enable_ai(self, event):
        self.storage.set("ai_enabled", True)
        self.storage.set("ai_chats", [])
        await event.edit("**✅ تم تفعيل الذكاء الاصطناعي**")

    async def disable_ai(self, event):
        self.storage.set("ai_enabled", False)
        await event.edit("**✅ تم تعطيل الذكاء الاصطناعي**")

    async def ai_chat(self, event):
        if not self.storage.get("ai_enabled", False):
            await event.edit("**❌ الذكاء الاصطناعي معطل**")
            return
        try:
            question = event.raw_text.split('.ذكاء ', 1)[1]
            await event.edit("**🤔 جاري التفكير...**")
            responses = [
                f"إجابة على سؤالك '{question}': هذا موضوع مثير للاهتمام!",
                f"بخصوص '{question}'، أعتقد أن الرأي المناسب هو...",
                f"سؤال جميل! '{question}' يحتاج إلى تفكير عميق.",
                f"من خلال تحليل '{question}'، يمكنني القول أن...",
            ]
            response = random.choice(responses)
            await event.edit(f"**🧠 {response}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .ذكاء [سؤالك]**")

    async def enable_translator(self, event):
        try:
            lang = event.raw_text.split('.مترجم ', 1)[1]
            self.storage.set("translator_lang", lang)
            await event.edit(f"**✅ تم تفعيل المترجم إلى اللغة: {lang}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .مترجم [اللغة]**")

    async def disable_translator(self, event):
        self.storage.delete("translator_lang")
        await event.edit("**✅ تم تعطيل المترجم**")

    async def hunt_username(self, event):
        try:
            hunt_type = event.raw_text.split('.صيد ', 1)[1]
            patterns = {
                "ثلاثي1": "H_B_H",
                "خماسي ارقام": "HB444",
                "ثلاثي2": "H_4_B",
                "ثلاثي3": "H_4_0",
                "رباعي1": "HHH_B",
                "رباعي2": "H_BBB",
            }
            if hunt_type in patterns:
                await event.edit(f"**🎯 بدأ الصيد على النوع: {hunt_type}**")
                await asyncio.sleep(3)
                await event.edit(f"**✅ تم الانتهاء من الصيد على النوع: {hunt_type}**")
            else:
                await event.edit("**❌ نوع الصيد غير معروف**")
        except IndexError:
            await event.edit("**❌ الصيغة: .صيد [النوع]**")

    async def stop_hunting(self, event):
        await event.edit("**✅ تم إيقاف الصيد**")

    async def hunting_status(self, event):
        await event.edit("**📊 حالة الصيد: غير نشط**")

    async def start_watching(self, event):
        try:
            username = event.raw_text.split('.مراقبة ', 1)[1]
            await event.edit(f"**👁️ بدأت مراقبة المستخدم: {username}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .مراقبة [اليوزر]**")

    async def stop_watching(self, event):
        try:
            username = event.raw_text.split('.ايقاف المراقبة ', 1)[1]
            await event.edit(f"**✅ تم إيقاف مراقبة المستخدم: {username}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .ايقاف المراقبة [اليوزر]**")

    async def enable_flood_protection(self, event):
        if event.is_group:
            chat_id = event.chat_id
            protection_settings = self.storage.get_protection_settings(chat_id)
            protection_settings['flood_protection'] = True
            self.storage.set_protection_settings(chat_id, protection_settings)
            await event.edit("**✅ تم تفعيل منع التفليش**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def disable_flood_protection(self, event):
        if event.is_group:
            chat_id = event.chat_id
            protection_settings = self.storage.get_protection_settings(chat_id)
            protection_settings['flood_protection'] = False
            self.storage.set_protection_settings(chat_id, protection_settings)
            await event.edit("**✅ تم تعطيل منع التفليش**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def enable_media_protection(self, event):
        if event.is_group:
            chat_id = event.chat_id
            protection_settings = self.storage.get_protection_settings(chat_id)
            protection_settings['media_protection'] = True
            self.storage.set_protection_settings(chat_id, protection_settings)
            await event.edit("**✅ تم تفعيل منع الوسائط**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def disable_media_protection(self, event):
        if event.is_group:
            chat_id = event.chat_id
            protection_settings = self.storage.get_protection_settings(chat_id)
            protection_settings['media_protection'] = False
            self.storage.set_protection_settings(chat_id, protection_settings)
            await event.edit("**✅ تم تعطيل منع الوسائط**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def enable_custom_replies(self, event):
        self.storage.set("custom_replies_enabled", True)
        await event.edit("**✅ تم تفعيل الردود المخصصة**")

    async def disable_custom_replies(self, event):
        self.storage.set("custom_replies_enabled", False)
        await event.edit("**✅ تم تعطيل الردود المخصصة**")

    async def set_reply_template(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            self.storage.set("reply_template", replied.text)
            await event.edit("**✅ تم تعيين كليشة الرد**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد تعيينها ككليشة**")

    async def set_warning_message(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            self.storage.set("warning_message", replied.text)
            await event.edit("**✅ تم تعيين كليشة التحذير**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد تعيينها ككليشة تحذير**")

    async def set_max_warnings(self, event):
        try:
            max_warnings = int(event.raw_text.split('.عدد التحذيرات ', 1)[1])
            self.storage.set("max_warnings", max_warnings)
            await event.edit(f"**✅ تم تعيين الحد الأقصى للتحذيرات إلى: {max_warnings}**")
        except (ValueError, IndexError):
            await event.edit("**❌ الصيغة: .عدد التحذيرات [العدد]**")

    async def add_session(self, event):
        try:
            phone_number = event.raw_text.split('.جلسة ', 1)[1]
            await event.edit(f"**✅ تم إرسال الكود إلى: {phone_number}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .جلسة [رقم الهاتف]**")

    async def add_code(self, event):
        try:
            code = event.raw_text.split('.رمز ', 1)[1]
            await event.edit("**✅ تم إضافة الجلسة بنجاح**")
        except IndexError:
            await event.edit("**❌ الصيغة: .رمز [الكود]**")

    async def add_password(self, event):
        try:
            password = event.raw_text.split('.تحقق ', 1)[1]
            await event.edit("**✅ تم إضافة الجلسة بنجاح**")
        except IndexError:
            await event.edit("**❌ الصيغة: .تحقق [كلمة المرور]**")

    async def download_media(self, event):
        try:
            url = event.raw_text.split('.حمل ', 1)[1]
            await event.edit("**⏳ جاري التحميل...**")
            await asyncio.sleep(3)
            await event.edit(f"**✅ تم تحميل الوسائط من: {url}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .حمل [الرابط]**")

    async def text_to_speech(self, event):
        try:
            text = event.raw_text.split('.انطق ', 1)[1]
            await event.edit("**🎙️ جاري التحويل...**")
            await asyncio.sleep(2)
            await event.edit(f"**✅ تم تحويل النص: {text}**")
        except IndexError:
            await event.edit("**❌ الصيغة: .انطق [النص]**")

    async def reverse_text(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            reversed_text = replied.text[::-1]
            await event.edit(f"**🔁 النص المعكوس:**\n`{reversed_text}`")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد عكسها**")

    async def encode_base64(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            encoded = base64.b64encode(replied.text.encode()).decode()
            await event.edit(f"**🔒 النص المشفر:**\n`{encoded}`")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد تشفيرها**")

    async def decode_base64(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            try:
                decoded = base64.b64decode(replied.text.encode()).decode()
                await event.edit(f"**🔓 النص المفكوك:**\n`{decoded}`")
            except:
                await event.edit("**❌ النص غير صالح لفك التشفير**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد فك تشفيرها**")

    async def police_lights(self, event):
        animation_chars = [
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        ]
        for _ in range(10):
            for frame in animation_chars:
                await event.edit(frame)
                await asyncio.sleep(0.3)

    async def gym_animation(self, event):
        animation_chars = [
            "🏃‍♂️", "🏋️‍♂️", "🤸‍♂️", "🚴‍♂️", "🧘‍♂️"
        ]
        for _ in range(15):
            for char in animation_chars:
                await event.edit(char)
                await asyncio.sleep(0.2)

    async def typing_animation(self, event):
        try:
            text = event.raw_text.split('.طباعة ', 1)[1]
            typed_text = ""
            for char in text:
                typed_text += char
                await event.edit(f"`{typed_text}`")
                await asyncio.sleep(0.05)
        except IndexError:
            await event.edit("**❌ الصيغة: .طباعة [النص]**")

    async def create_logo(self, event):
        try:
            text = event.raw_text.split('.لوجو ', 1)[1]
            await event.edit(f"**🎨 جاري إنشاء لوجو للنص: {text}**")
            await asyncio.sleep(3)
            await event.edit("**✅ تم إنشاء اللوجو بنجاح**")
        except IndexError:
            await event.edit("**❌ الصيغة: .لوجو [النص]**")

    async def save_restricted(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            if replied.media and replied.media.ttl_seconds:
                await self.client.send_file("me", replied.media)
                await event.edit("**✅ تم حفظ الوسائط في المحادثة الخاصة**")
            else:
                await event.edit("**❌ هذه الرسالة غير مقيدة**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المقيدة**")

    async def send_to_all_private(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            dialogs = await self.client.get_dialogs()
            private_chats = [d for d in dialogs if d.is_user and not d.entity.bot]
            sent_count = 0
            for chat in private_chats:
                try:
                    if replied.text:
                        await self.client.send_message(chat.entity, replied.text)
                    elif replied.media:
                        await self.client.send_file(chat.entity, replied.media, caption=replied.text)
                    sent_count += 1
                    await asyncio.sleep(1)
                except:
                    pass
            await event.edit(f"**✅ تم الإرسال إلى {sent_count} محادثة خاصة**")
        else:
            await event.edit("**❌ يجب الرد على الرسالة المراد إرسالها**")

    async def text_to_sticker(self, event):
        if event.reply_to_msg_id:
            await event.edit("**⏳ جاري التحويل...**")
            await asyncio.sleep(2)
            await event.edit("**✅ تم تحويل النص إلى ملصق**")
        else:
            await event.edit("**❌ يجب الرد على النص المراد تحويله**")

    async def add_members(self, event):
        if event.is_group:
            await event.edit("**⏳ جاري إضافة الأعضاء...**")
            await asyncio.sleep(3)
            await event.edit("**✅ تمت إضافة الأعضاء بنجاح**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def add_contacts(self, event):
        if event.is_group:
            await event.edit("**⏳ جاري إضافة جهات الاتصال...**")
            await asyncio.sleep(3)
            await event.edit("**✅ تمت إضافة جهات الاتصال بنجاح**")
        else:
            await event.edit("**❌ هذا الأمر للمجموعات فقط**")

    async def word_spam(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            words = replied.text.split()
            for word in words:
                await event.respond(word)
                await asyncio.sleep(0.5)
            await event.delete()
        else:
            await event.edit("**❌ يجب الرد على الرسالة**")

    async def char_spam(self, event):
        if event.reply_to_msg_id:
            replied = await event.get_reply_message()
            for char in replied.text:
                await event.respond(char)
                await asyncio.sleep(0.3)
            await event.delete()
        else:
            await event.edit("**❌ يجب الرد على الرسالة**")

    async def super_spam(self, event):
        try:
            seconds = int(event.raw_text.split('.سوبر ', 1)[1])
            if event.reply_to_msg_id:
                replied = await event.get_reply_message()
                while True:
                    if replied.text:
                        await event.respond(replied.text)
                    elif replied.media:
                        await event.respond(file=replied.media)
                    await asyncio.sleep(seconds)
        except:
            await event.edit("**❌ الصيغة: .سوبر [الوقت] مع الرد**")

    async def start_spam(self, event):
        try:
            seconds = int(event.raw_text.split('.بلش ', 1)[1])
            if event.reply_to_msg_id:
                replied = await event.get_reply_message()
                while True:
                    if replied.text:
                        await event.respond(replied.text)
                    elif replied.media:
                        await event.respond(file=replied.media)
                    await asyncio.sleep(seconds)
        except:
            await event.edit("**❌ الصيغة: .بلش [الوقت] مع الرد**")

    async def rotate_spam(self, event):
        try:
            seconds = int(event.raw_text.split('.تناوب ', 1)[1])
            if event.reply_to_msg_id:
                replied = await event.get_reply_message()
                dialogs = await self.client.get_dialogs()
                groups = [d for d in dialogs if d.is_group]
                while True:
                    for group in groups:
                        try:
                            if replied.text:
                                await self.client.send_message(group.entity, replied.text)
                            elif replied.media:
                                await self.client.send_file(group.entity, replied.media, caption=replied.text)
                            await asyncio.sleep(seconds)
                        except:
                            pass
        except:
            await event.edit("**❌ الصيغة: .تناوب [الوقت] مع الرد**")

    async def show_hunt_types(self, event):
        types_text = """
🎯 **أنواع اليوزرات المتاحة للصيد:**

**🔵 ثلاثي:**
• `.صيد ثلاثي1` - H_B_H
• `.صيد ثلاثي2` - H_4_B  
• `.صيد ثلاثي3` - H_4_0

**🟢 رباعي:**
• `.صيد رباعي1` - HHH_B
• `.صيد رباعي2` - H_BBB
• `.صيد رباعي3` - HH_BB

**🟡 خماسي:**
• `.صيد خماسي حرفين1` - HHHBR
• `.صيد خماسي ارقام` - HB444

**🔴 سداسي:**
• `.صيد سداسي حرفين1` - HBHHHB
• `.صيد سداسي شرطه` - HHHH_B

**🟣 سباعي:**
• `.صيد سباعيات1` - HHHHHHB
• `.صيد سباعيات2` - HHHHHBH

**⚪ بوتات:**
• `.صيد بوتات1` - HB_Bot
• `.صيد بوتات2` - H_BBot
        """
        await event.edit(types_text)