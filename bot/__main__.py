import asyncio
from importlib import import_module
from pathlib import Path
from bot.client import app
from bot import logger
from bot.server import server
from pyrogram import idle

def load_plugins():
    count = 0
    for path in Path('bot/plugins').rglob('*.py'):
        if not path.name.startswith("__"):  # Avoid importing __init__.py or __pycache__
            import_module(f'bot.plugins.{path.stem}')
            count += 1
    logger.info(f'Loaded {count} {"plugins" if count != 1 else "plugin"}.')

async def main():
    logger.info('Initializing...')
    asyncio.create_task(server.serve())  # Start Quart server
    await app.start()
    logger.info('Telegram client is now started.')
    logger.info('Loading bot plugins...')
    load_plugins()
    logger.info('Bot is now ready!')
    await idle()
    logger.info('Shutting down bot...')
    await app.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped manually.')
