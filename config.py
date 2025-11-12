import os
from telethon.sessions import StringSession
from telethon import TelegramClient
import redis

API_ID = int(os.environ.get("API_ID", "21681934"))
API_HASH = os.environ.get("API_HASH", "bc11cc1cdec262af2ca26bc16358c47e")
SESSION_STRING = "1ApWapzMBuxm-jGRxmnAMG3pnOQFgHn3AJIDmGwODOaAZR8Sg-_SnugSjH6YDK1Iv-hh_e2xywHQOTOYKGWsWaWNMirr6FH-9CH-XpZjcr_cDZtLsze8Fv78UtzWTECrlX0BaBlw_UgchPmh_1rTWL2IsHj0haprF2ax0HPzD6cpTC61Ks8jYzlUFWC1X0pQjIUd2JubulJ83_gxpT4vVznO5MUsykd-RfKEVV0bmo3SSyMm5wNkScPQl8VG9JPlN4uMKVvyg-g1qdvl0IsFaW7NDHTCKcEiQZG78HFGbv1k8yWj4gCM33EOB-_dk9s7TiW7O-6mZWnBEjs1c2EN-UfzzLBYoL9c="

BOT_TOKEN = "8192202802:AAGXwMFwGGhlALcb3b5BZzaDU7cS-12o058"
BOT_USERNAME = "bqrstbot"

api_id = API_ID
api_hash = API_HASH
session_string = SESSION_STRING

bot = TelegramClient('bot_session', api_id, api_hash)
client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def initialize_clients():
    print("• جاري تهيئة الحساب الرئيسي...")
    await client.start()
    
    print("• جاري تهيئة البوت المساعد...")
    await bot.start(bot_token=BOT_TOKEN)
    bot_username = await get_bot_username()
    
    from storage import storage
    storage.set("bot_username", bot_username)
    
    return bot_username

async def get_bot_username():
    try:
        bot_me = await bot.get_me()
        print(f"✅ البوت المساعد: @{bot_me.username}")
        return bot_me.username
    except Exception as e:
        print(f"❌ خطأ في الحصول على معلومات البوت: {e}")
        return None

try:
    REDIS_URL = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    REDIS_URL.ping()
    print("✅ تم الاتصال بـ Redis بنجاح")
except redis.ConnectionError:
    print("❌ فشل الاتصال بـ Redis")
    REDIS_URL = None

OWNER_ID = 6848908141
IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"

QUESTIONS_LIST = [
    "هل تحب شـهـم ؟",
    "حكي ودك يوصل للشخص المطلوب ؟",
    "منشن شخص تسولف معه تنسى هموم الدنيا ؟",
    "مقوله او مثل او بيت شعر قريب من قلبك?",
    "اكثر مكان تحب تروح له ف الويكند ?",
    "كم وجبه تآكل ف اليوم ?",
    "كم ساعه تنام ف اليوم ?",
    "هل وثقت ف احد و خذلك ?",
    "كلمه تعبر عن شعورك ?",
    "منشن شخص فاهمك ف كل شيء ?",
    "اصدقاء المواقع افضل من الواقع تتفق?",
    "كلمه معينه م يفهمها الا اصحابك ?",
    "كل شيء يهون الا ?",
    "كلمه تعبر عن شعورك ?",
    "كيف تتصرف مع شخص تكلمه في سالفه مهمه ويصرفك ومعد يرد ابداً?",
    "ثلاث اشياء جنبك الحين ?",
    "تشوف انو التواصل بشكل يومي من اساسيات الحب ?",
    "نوعيات ودك ينقرضون من تويتر?",
    "ماذا تفعل عندما تري دموع زوجتك..?",
    "ما هي هوايتك المفضلة?",
    "لو خيروك تسافر لأي مكان في العالم، وين بتروح?",
    "ايش اكثر اكلة تحبها?",
    "ايش اكثر لون تحبه?",
    "تحب القهوة او الشاي?",
    "ايش موقف صار لك ما تنساه?",
    "ايش اكثر شيء يضايقك?",
    "ايش اكثر شيء يسعدك?",
    "ايش هي امنيتك في الحياة?",
    "لو كان بإمكانك تغيير شيء واحد في العالم، ماذا سيكون?",
    "هل تؤمن بالحب من اول نظرة?",
    "هل انت شخص صباحي او مسائي?",
    "ما هو برجك?",
    "ما هو فيلمك المفضل?",
    "ما هي اغنيتك المفضلة?",
    "ما هي فرقتك الموسيقية المفضل?",
    "ما هو كتابك المفضل?",
    "ما هو مسلسل Netflix  المفضل لديك?",
    "هل تفضل الصيف او الشتاء?",
    "هل تفضل العيش في المدينة او الريف?",
    "هل تفضل الكلاب او القطط?",
    "ما هو رأيك في وسائل التواصل الاجتماعي?",
    "ما هي نصيحتك لأي شخص يمر بيوم سيء?",
    "ما هو الشيء الذي تفتخر به?",
    "ما هو الشيء الذي تخاف منه?",
    "ما هو الشيء الذي يجعلك تضحك?",
    "ما هو الشيء الذي يجعلك تبكي?",
    "ما هو الشيء الذي يجعلك تشعر بالامتنان?",
    "ما هو تعريفك للسعادة?",
    "ما هو تعريفك للنجاح?",
    "لو كان بإمكانك امتلاك اي قوة خارقة، ماذا ستختار?",
    "لو كان بإمكانك العودة بالزمن، الى اي فترة زمنية ستعود?",
    "من هو مثلك الأعلى?",
    "ما هي أكبر غلطة سويتها في حياتك?",
    "ما هو الدرس اللي تعلمته من هذي الغلطة?",
    "ما هي أفضل نصيحة  انعطت لك?",
    "ايش اكثر شيء تعلمته من والديك?",
    "ايش اكثر شيء تحبه في نفسك?",
    "ايش اكثر شيء تكرهه في نفسك?",
    "كيف تصف نفسك في ثلاث كلمات?",
    "ما هو الشيء الذي يميزك عن غيرك?",
    "ما هي طموحاتك المستقبلية?",
    "ما هو الشيء الذي تتمنى تحقيقه قبل ما تموت?",
    "هل تؤمن بالحياة بعد الموت?",
    "هل تؤمن بالأشباح?",
    "هل تؤمن بالكائنات الفضائية?",
    "ما هو رأيك في الذكاء الاصطناعي?",
    "هل تعتقد أن الروبوتات ستسيطر على العالم?",
]