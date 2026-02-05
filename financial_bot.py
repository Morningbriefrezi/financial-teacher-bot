import os
import asyncio
import random
from datetime import datetime, time
from telegram import Bot
from telegram.ext import Application
from openai import OpenAI
import pytz
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  # Your personal chat ID

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Tbilisi timezone
TBILISI_TZ = pytz.timezone('Asia/Tbilisi')

# Message times (Tbilisi time)
MESSAGE_TIMES = [
    time(9, 0),   # 09:00 AM
    time(12, 50), # 12:50 PM
    time(16, 50)  # 16:50 PM
]

def generate_financial_message(message_number: int) -> str:
    """Generate a comprehensive financial education message in Georgian using OpenAI"""
    
    prompt = f"""შექმენი სრული ფინანსური განათლების შეტყობინება ქართულ ენაზე, რომელიც შეიცავს:

1. **ფინანსური ბაზრების ახალი ამბები** (რეალური დროის ინფორმაცია - მიუთითე, რომ მომხმარებელმა უნდა გადაამოწმოს ბოლო ინფორმაცია):
   - აქციების ბაზრების მიმოხილვა
   - კრიპტოვალუტის განახლებები
   - ეკონომიკური მაჩვენებლები

2. **ერთი კარგი ინტერვიუ** წარმატებულ მეწარმესთან ან ინვესტორთან:
   - მოკლე ბიოგრაფია
   - მთავარი გაკვეთილები
   - შთამაგონებელი ციტატა

3. **3 ფულის რჩევა**:
   - პრაქტიკული რჩევები ყოველდღიურ ფინანსებში
   - დანაზოგის სტრატეგიები
   - ხარჯების მართვა

4. **3 ინვესტიციის რჩევა**:
   - დივერსიფიკაციის იდეები
   - რისკების მართვა
   - გრძელვადიანი სტრატეგიები

5. **3 ახალი ინფორმაცია** ფულისა და ფინანსური სისტემის შესახებ:
   - როგორ მუშაობს ბანკები
   - ცენტრალური ბანკების როლი
   - ფულის შექმნის პროცესი

6. **რჩევა სიმდიდრის გასაზრდელად**:
   - კონკრეტული ნაბიჯები
   - აზროვნების შეცვლა
   - პასიური შემოსავლის იდეები

გააკეთე შეტყობინება საინტერესო, მოტივირებული და განსხვავებული. გამოიყენე emoji-ები. 
შეტყობინება უნდა იყოს დაახლოებით 800-1000 სიტყვა.
დღის შეტყობინება: #{message_number}/3

გთხოვ, შექმენი სრულიად ახალი და უნიკალური შინაარსი."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "შენ ხარ პროფესიონალი ფინანსური მასწავლებელი და მრჩეველი, რომელიც საუბრობს ქართულ ენაზე. შენი მიზანია ადამიანების ფინანსური განათლება და მოტივაცია."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,  # Higher temperature for more variety
            max_tokens=2500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error generating message: {e}")
        return f"⚠️ შეცდომა შეტყობინების გენერირებისას: {str(e)}"

async def send_scheduled_message(app: Application, message_number: int):
    """Send a scheduled financial message"""
    try:
        logger.info(f"Generating message #{message_number}")
        message = generate_financial_message(message_number)
        
        logger.info(f"Sending message #{message_number} to chat {CHAT_ID}")
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode=None
        )
        logger.info(f"Message #{message_number} sent successfully")
        
    except Exception as e:
        logger.error(f"Error sending message #{message_number}: {e}")

async def schedule_daily_messages(app: Application):
    """Schedule messages at specific times each day"""
    while True:
        now = datetime.now(TBILISI_TZ)
        
        for idx, scheduled_time in enumerate(MESSAGE_TIMES, 1):
            # Create datetime for today's scheduled time
            scheduled_datetime = TBILISI_TZ.localize(
                datetime.combine(now.date(), scheduled_time)
            )
            
            # If the time has passed today, schedule for tomorrow
            if now > scheduled_datetime:
                continue
            
            # Calculate seconds until scheduled time
            time_until = (scheduled_datetime - now).total_seconds()
            
            if time_until > 0 and time_until <= 60:  # Within next minute
                logger.info(f"Sending scheduled message #{idx} at {scheduled_time}")
                await send_scheduled_message(app, idx)
        
        # Check every 30 seconds
        await asyncio.sleep(30)

async def test_message(app: Application):
    """Send a test message immediately"""
    logger.info("Sending test message...")
    await send_scheduled_message(app, 1)

def main():
    """Main function to run the bot"""
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY or not CHAT_ID:
        logger.error("Missing required environment variables!")
        logger.error("Please set: TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, TELEGRAM_CHAT_ID")
        logger.error("Check your .env file or environment variables")
        return
    
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    logger.info("Bot started. Scheduling messages...")
    logger.info(f"Message times (Tbilisi): {', '.join([t.strftime('%H:%M') for t in MESSAGE_TIMES])}")
    logger.info(f"Target chat ID: {CHAT_ID}")
    
    # Run the scheduler
    app.create_task(schedule_daily_messages(app))
    
    # Uncomment the line below to send a test message on startup
    # app.create_task(test_message(app))
    
    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
