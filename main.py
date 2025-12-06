import logging
import os
import datetime
# from config.settings import TELEGRAM_TOKEN
# from bot.handlers import start_bot

# Standard Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Google Antigravity Bot...")
    
    from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
    from config.settings import TELEGRAM_TOKEN
    from bot.handlers import start, help_command, predict_command

    if not TELEGRAM_TOKEN:
        logger.error("No TELEGRAM_TOKEN found! Check your .env file.")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("predict", predict_command))

    # Schedule daily data update
    job_queue = application.job_queue
    from scripts.update_data import update_matches
    # We use a wrapper because job_queue expects a callback with 'context'
    async def scheduled_update(context: ContextTypes.DEFAULT_TYPE):
        import asyncio
        # Run synchronous update in a separate thread to not block bot
        await asyncio.to_thread(update_matches)
        
    # Run every day at 10:00 UTC (adjust as needed)
    job_queue.run_daily(scheduled_update, time=datetime.time(hour=10, minute=0))
    
    # Also run once heavily on startup for testing
    job_queue.run_once(scheduled_update, when=10)

    logger.info("Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
