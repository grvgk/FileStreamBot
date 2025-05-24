import asyncio
from importlib import import_module
from pathlib import Path
from bot.client import app  # Now imported safely
from bot import logger
from bot.server import server
from pyrogram.idle import idle

def load_plugins():
    count = 0
    for path in Path('bot/plugins').rglob('*.py'):
        import_module(f'bot.plugins.{path.stem}')
        count += 1
    logger.info(f'Loaded {count} {"plugins" if count > 1 else "plugin"}.')

async def main():
    logger.info('initializing...')
    asyncio.create_task(server.serve())
    await app.start()
    logger.info('Telegram client is now started.')
    logger.info('Loading bot plugins...')
    load_plugins()
    logger.info('Bot is now ready!')
    await idle()
    await app.stop()

if __name__ == '__main__':
    asyncio.run(main())
