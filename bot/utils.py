from telegram import Chat, ParseMode

from mwt import MWT


class Utils:

    def __init__(self, bot):
        self.bot = bot
        self.update = None

    def set_update(self, update):
        print("set_update {}".format(update))
        self.update = update

    def is_chat_private(self):
        return self.get_chat().type == Chat.PRIVATE

    def is_user_admin(self):
        return self.update.message.from_user.id in self.get_admin_ids()

    @MWT(timeout=60*15)
    def get_admin_ids(self):
        return [admin.user.id for admin in self.bot.get_chat_administrators(self.update.message.chat_id)]

    def is_chat_all_admins(self):
        return self.get_chat().all_members_are_administrators

    def get_chat(self):
        return self.update.effective_chat

    def get_chatroom(self):
        return self.update.message.chat

    def get_message(self):
        return self.update.message

    def get_user(self):
        return self.update.effective_user

    def send_message(self, *args, **kwargs):
        kwargs.update({'parse_mode': ParseMode.HTML})
        self.bot.send_message(*args, **kwargs)

    def matches_user_id(self, owner_id):
        return str(self.update.message.from_user.id) == owner_id
