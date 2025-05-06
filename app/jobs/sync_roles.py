from telegram.ext import ContextTypes


async def sync_roles(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.application.setup_roles()
