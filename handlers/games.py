import random
from telethon import events
from storage import storage

QUESTIONS_LIST = [
    "هل تحب شـهـم ؟",
    "حكي ودك يوصل للشخص المطلوب ؟",
    "منشن شخص تسولف معه تنسى هموم الدنيا ؟",
    # ... (بقية الأسئلة من الكود الأصلي)
]

async def handle_games(event):
    """معالجة ألعاب البوت"""
    command = event.pattern_match.group(0)
    
    if command == '.خيروك':
        question = random.choice(QUESTIONS_LIST)
        await event.edit(question)
    
    elif command == '.بوسة':
        responses = ["روح لعند المطور وقول له", "ايع مقرف", "همممممم"]
        await event.edit(random.choice(responses))
    
    elif command == '.محيبس':
        await handle_mahibis(event)

async def handle_mahibis(event):
    """لعبة المحيبس"""
    correct_answer = random.randint(1, 6)
    storage.set(f"mahibis_{event.chat_id}", correct_answer)
    
    await event.edit(
        "🎮 لعبة المحيبس\n\n"
        "أول من يرسل 'انا' يلعب\n"
        "الأوامر:\n"
        "• طك + رقم ← لفتح العظمة\n"
        "• جيب + رقم ← لأخذ المحبس\n\n"
        f"{format_mahibis_board()}"
    )

def format_mahibis_board():
    """تنسيق لوحة المحيبس"""
    numbers = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣"
    hands = "🖐️ 🖐️ 🖐️ 🖐️ 🖐️ 🖐️"
    return f"{numbers}\n{hands}"