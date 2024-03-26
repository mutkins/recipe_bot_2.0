from aiogram import Dispatcher
from handlers.admin import register_admin_handlers
from handlers.other import register_other_handlers
from handlers.user import register_user_handlers


def register_all_handlers(dp: Dispatcher):
    register_user_handlers(dp)
    register_admin_handlers(dp)
    register_other_handlers(dp)
