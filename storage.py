import redis
import json
import pickle
import os
from config import REDIS_URL

class RedisStorage:
    def __init__(self):
        try:
            if isinstance(REDIS_URL, str):
                self.redis = redis.from_url(REDIS_URL, decode_responses=True)
            else:
                self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Redis: {e}")
            self.redis = None
            self.memory_storage = {}
    
    def set(self, key, value):
        try:
            if self.redis:
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                self.redis.set(key, value)
            else:
                self.memory_storage[key] = value
        except Exception as e:
            print(f"❌ خطأ في حفظ البيانات: {e}")
    
    def get(self, key, default=None):
        try:
            if self.redis:
                value = self.redis.get(key)
                if value is None:
                    return default
                try:
                    return json.loads(value)
                except:
                    return value
            else:
                return self.memory_storage.get(key, default)
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات: {e}")
            return default
    
    def delete(self, key):
        try:
            if self.redis:
                self.redis.delete(key)
            else:
                self.memory_storage.pop(key, None)
        except Exception as e:
            print(f"❌ خطأ في حذف البيانات: {e}")
    
    def exists(self, key):
        try:
            if self.redis:
                return self.redis.exists(key)
            else:
                return key in self.memory_storage
        except Exception as e:
            print(f"❌ خطأ في التحقق من البيانات: {e}")
            return False
    
    def get_responses(self):
        return self.get("responses", {})
    
    def set_responses(self, responses):
        self.set("responses", responses)
    
    def get_muted_users(self):
        return self.get("muted_users", [])
    
    def set_muted_users(self, users):
        self.set("muted_users", users)
    
    def get_protection_settings(self, chat_id):
        return self.get(f"protection_{chat_id}", {})
    
    def set_protection_settings(self, chat_id, settings):
        self.set(f"protection_{chat_id}", settings)
    
    def get_active_timers(self):
        return self.get("active_timers", {})
    
    def set_active_timers(self, timers):
        self.set("active_timers", timers)
    
    def get_user_data(self, user_id):
        return self.get(f"user_{user_id}", {})
    
    def set_user_data(self, user_id, data):
        self.set(f"user_{user_id}", data)
    
    def get_auto_reply_enabled(self):
        return self.get("auto_reply_enabled", False)
    
    def set_auto_reply_enabled(self, enabled):
        self.set("auto_reply_enabled", enabled)
    
    def get_mimic_user(self):
        return self.get("mimic_user")
    
    def set_mimic_user(self, user_id):
        self.set("mimic_user", user_id)
    
    def get_original_profile(self):
        return self.get("original_profile")
    
    def set_original_profile(self, profile):
        self.set("original_profile", profile)
    
    def get_time_name_enabled(self):
        return self.get("time_name_enabled", False)

    def set_time_name_enabled(self, enabled):
        self.set("time_name_enabled", enabled)

    def get_channel_link(self):
        return self.get("channel_link")

    def set_channel_link(self, link):
        self.set("channel_link", link)

    def get_ai_enabled(self):
        return self.get("ai_enabled", False)

    def set_ai_enabled(self, enabled):
        self.set("ai_enabled", enabled)

    def get_translator_lang(self):
        return self.get("translator_lang")

    def set_translator_lang(self, lang):
        self.set("translator_lang", lang)

    def get_custom_replies_enabled(self):
        return self.get("custom_replies_enabled", False)

    def set_custom_replies_enabled(self, enabled):
        self.set("custom_replies_enabled", enabled)

    def get_reply_template(self):
        return self.get("reply_template")

    def set_reply_template(self, template):
        self.set("reply_template", template)

    def get_warning_message(self):
        return self.get("warning_message", "⚠️ تحذير {warnings}/{max_warnings}")

    def set_warning_message(self, message):
        self.set("warning_message", message)

    def get_max_warnings(self):
        return self.get("max_warnings", 5)

    def set_max_warnings(self, count):
        self.set("max_warnings", count)

    def get_bot_username(self):
        return self.get("bot_username")

    def set_bot_username(self, username):
        self.set("bot_username", username)

storage = RedisStorage()