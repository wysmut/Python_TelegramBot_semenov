from dataclasses import dataclass
from typing import Callable, Optional

from app.handlers.filters import filter_for_command
from telegram.ext import BaseHandler, CommandHandler, CallbackQueryHandler

from app.core.users.constants import RolesEnum
from app.handlers.commands import start, create_order, add_item, finish_order
from app.handlers.waiter_commands import waiter_start, waiter_finish_order


@dataclass
class Handler:
    handler: BaseHandler
    role: RolesEnum | None = None


HANDLERS: tuple[Handler, ...] = (
    Handler(handler=CommandHandler("start", waiter_start), role=RolesEnum.waiter),
    Handler(handler=CommandHandler("start", start)),
    Handler(handler=CallbackQueryHandler(create_order,
                                         pattern=filter_for_command("order_create"))),
    Handler(
        handler=CallbackQueryHandler(add_item, pattern=filter_for_command("add_item"))),
    Handler(
        handler=CallbackQueryHandler(finish_order,
                                     pattern=filter_for_command("finish_order"))),
    Handler(handler=CallbackQueryHandler(waiter_finish_order, pattern=filter_for_command(
        "waiter_finish_order")), role=RolesEnum.waiter)
)
