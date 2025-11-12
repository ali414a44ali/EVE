import asyncio
import logging
from config import client, bot, initialize_clients, BOT_USERNAME
from storage import storage
from handlers.commands import CommandsHandler
from telethon import events, Button
import re
from data import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvaBot:
    def __init__(self):
        self.storage = storage
        self.client = client
        self.bot = bot
        self.commands_handler = CommandsHandler(self.client)
        self.bot_username = BOT_USERNAME

    async def start(self):
        try:
            await initialize_clients()
            self.storage.set("bot_username", self.bot_username)
            await self.register_handlers()
            await self.register_inline_handlers()
            logger.info("✅ تم تشغيل بوت شـهـم بنجاح!")
            await asyncio.gather(
                self.client.run_until_disconnected(),
                self.bot.run_until_disconnected()
            )
        except Exception as e:
            logger.error(f"❌ خطأ في التشغيل: {e}")

    async def register_handlers(self):
        @self.client.on(events.NewMessage(pattern=r'\.\w+'))
        async def handle_commands(event):
            await self.commands_handler.handle_all_commands(event)
        logger.info("✅ تم تسجيل ال event handlers")

    async def register_inline_handlers(self):
        def check_owner(func):
            async def wrapper(event):
                try:
                    user_id = event.query.user_id
                    client_uid = (await self.client.get_me()).id
                    if user_id == client_uid:
                        return await func(event)
                    else:
                        await event.answer("عذراً، عليك تنصيب سورس شهم من اجل استخدام الاوامر !", alert=True)
                except Exception as e:
                    print(f"Error in check_owner: {e}")
            return wrapper

        @self.bot.on(events.InlineQuery)
        async def inline_handler(event):
            try:
                builder = event.builder
                result = None
                query = event.text
                client_uid = (await self.client.get_me()).id
                
                if query == "اوامري" and event.query.user_id == client_uid:
                    buttons = []
                    for row in MAIN_BUTTONS:
                        button_row = []
                        for button in row:
                            button_row.append(Button.inline(button["text"], data=button["data"]))
                        buttons.append(button_row)
                    
                    if JEP_IC and JEP_IC.endswith((".jpg", ".png", "gif", "mp4")):
                        result = builder.photo(
                            JEP_IC, text=ROE, buttons=buttons, link_preview=False
                        )
                    elif JEP_IC:
                        result = builder.document(
                            JEP_IC,
                            title="EVA SOURCE",
                            text=ROE, 
                            buttons=buttons,
                            link_preview=False,
                        )
                    else:
                        result = builder.article(
                            title="EVA SOURCE",
                            text=ROE,
                            buttons=buttons,
                            link_preview=False,
                        )
                    await event.answer([result] if result else None)
            except Exception as e:
                print(f"Error in inline_handler: {e}")

        async def show_main_menu(event):
            buttons = []
            for row in MAIN_BUTTONS:
                button_row = []
                for button in row:
                    button_row.append(Button.inline(button["text"], data=button["data"]))
                buttons.append(button_row)
            await event.edit(ROE, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"l313l0")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="jrzst")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(ROZADM, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"jrzst")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="tslrzj")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(GRTSTI, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"tslrzj")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="krrznd")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(JMAN, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"krrznd")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="rozbot")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(TKPRZ, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"rozbot")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="Jmrz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(ROZBOT, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"Jmrz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="r7brz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(JROZT, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"r7brz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="sejrz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(JMTRD, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"sejrz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="gro")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(ROZSEG, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"gro")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="grrz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(JMGR1, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"grrz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="iiers")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(ROZPRV, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"iiers")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="rfhrz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(HERP, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"rfhrz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("التالي", data="uscuxrz")],
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(T7SHIZ, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"uscuxrz")))
        @check_owner
        async def _(event):
            buttons = [
                [Button.inline("🔙", data="ROE")]
            ]
            await event.edit(CLORN, buttons=buttons)

        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"ROE")))
        @check_owner
        async def _(event):
            await show_main_menu(event)


        @self.bot.on(events.CallbackQuery(pattern=re.compile(rb"back_to_main")))
        @check_owner
        async def _(event):
            await show_main_menu(event)

        logger.info("✅ تم تسجيل معالجات الإنلاين للبوت المساعد")

async def main():
    bot_instance = EvaBot()
    await bot_instance.start()

if __name__ == "__main__":
    asyncio.run(main())