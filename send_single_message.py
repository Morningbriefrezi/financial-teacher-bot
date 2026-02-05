import os
import asyncio
from datetime import datetime
from telegram import Bot
from openai import OpenAI
import pytz

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Tbilisi timezone
TBILISI_TZ = pytz.timezone('Asia/Tbilisi')

def determine_message_number():
    """Determine which message to send based on current time"""
    now = datetime.now(TBILISI_TZ)
    hour = now.hour
    
    if hour < 11:  # Before 11 AM
        return 1  # Morning message
    elif hour < 15:  # Before 3 PM
        return 2  # Afternoon message
    else:
        return 3  # Evening message

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
            temperature=0.9,
            max_tokens=2500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ შეცდომა შეტყობინების გენერირებისას: {str(e)}"

async def send_message():
    """Send a single financial message"""
    try:
        # Determine which message to send
        message_number = determine_message_number()
        
        print(f"Generating message #{message_number}...")
        message = generate_financial_message(message_number)
        
        # Initialize bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        print(f"Sending message #{message_number} to chat {CHAT_ID}...")
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode=None
        )
        
        print(f"✅ Message #{message_number} sent successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

def main():
    """Main function"""
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY or not CHAT_ID:
        print("❌ Missing required environment variables!")
        print("Please set: TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, TELEGRAM_CHAT_ID")
        return
    
    print("🤖 Starting Financial Teacher Bot...")
    print(f"📅 Current time (Tbilisi): {datetime.now(TBILISI_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the async function
    asyncio.run(send_message())

if __name__ == '__main__':
    main()
