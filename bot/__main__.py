import asyncio
from importlib import import_module
from pathlib import Path
from bot import TelegramBot, logger
from bot.config import Telegram
from bot.server import server

def load_plugins():
    count = 0
    for path in Path('bot/plugins').rglob('*.py'):
        import_module(f'bot.plugins.{path.stem}')
        count += 1
    logger.info(f'Loaded {count} {"plugins" if count != 1 else "plugin"}.')

async def main():
    logger.info("Initializing...")
    await TelegramBot.start()
    logger.info("Telegram bot is now started.")
    
    # Start the web server
    asyncio.create_task(server.serve())

    logger.info("Loading bot plugins...")
    load_plugins()
    logger.info("Bot is now ready!")
    
    await TelegramBot.idle()

if __name__ == "__main__":
    asyncio.run(main())
