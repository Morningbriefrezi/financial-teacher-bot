# 🐙 GitHub Setup Tutorial | GitHub-ზე დაყენების ინსტრუქცია

სრული გზამკვლევი თქვენი ფინანსური ბოტის GitHub-ზე ატვირთვისა და გაშვებისთვის.

Complete guide to upload and run your financial bot on GitHub.

---

## 📋 Table of Contents | სარჩევი

1. [Create GitHub Account](#step-1-create-github-account)
2. [Install Git](#step-2-install-git)
3. [Create Repository](#step-3-create-repository)
4. [Upload Your Bot](#step-4-upload-your-bot)
5. [Deploy to Cloud (Free Options)](#step-5-deploy-to-cloud)
6. [Keep Bot Running 24/7](#step-6-keep-bot-running-247)

---

## Step 1: Create GitHub Account | GitHub ანგარიშის შექმნა

### ქართულად:

1. **გახსენით** [github.com](https://github.com)
2. **დააჭირეთ** "Sign up" (რეგისტრაცია)
3. **შეიყვანეთ**:
   - Email მისამართი
   - პაროლი (ძლიერი!)
   - Username (მაგ: `giorgi_investor`)
4. **გაიარეთ** verification
5. **დაადასტურეთ** email მისამართი

### In English:

1. **Visit** [github.com](https://github.com)
2. **Click** "Sign up"
3. **Enter**:
   - Email address
   - Password (strong!)
   - Username (e.g., `giorgi_investor`)
4. **Complete** verification
5. **Verify** your email

---

## Step 2: Install Git | Git-ის დაყენება

### For Windows:

1. **Download** Git from [git-scm.com](https://git-scm.com/download/win)
2. **Run** the installer
3. **Use default settings** (just click "Next")
4. **Important**: Check "Add Git to PATH"
5. **Finish** installation

### For Mac:

**Option A - Using Homebrew (Recommended):**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git
```

**Option B - Direct Download:**
1. Download from [git-scm.com](https://git-scm.com/download/mac)
2. Run the installer

### For Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install git
```

### Verify Installation | დაყენების შემოწმება:

```bash
git --version
```

You should see something like: `git version 2.40.0`

---

## Step 3: Create Repository | რეპოზიტორიის შექმნა

### ქართულად:

1. **შედით** GitHub.com-ზე
2. **დააჭირეთ** "+" ღილაკს (ზედა მარჯვენა კუთხე)
3. **აირჩიეთ** "New repository"
4. **შეავსეთ**:
   - **Repository name**: `financial-teacher-bot`
   - **Description**: `Georgian financial education Telegram bot`
   - **აირჩიეთ**: ✅ Public (ან Private თუ გინდათ)
   - **ჩართეთ**: ✅ Add a README file
   - **აირჩიეთ**: .gitignore template → Python
5. **დააჭირეთ** "Create repository"

### In English:

1. **Login** to GitHub.com
2. **Click** "+" button (top right)
3. **Select** "New repository"
4. **Fill in**:
   - **Repository name**: `financial-teacher-bot`
   - **Description**: `Georgian financial education Telegram bot`
   - **Choose**: ✅ Public (or Private if you prefer)
   - **Check**: ✅ Add a README file
   - **Choose**: .gitignore template → Python
5. **Click** "Create repository"

---

## Step 4: Upload Your Bot | ბოტის ატვირთვა

### Method 1: Using Git Command Line (Recommended) | Git-ით ატვირთვა

#### Step 4.1: Configure Git | Git-ის კონფიგურაცია

**First time only:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Step 4.2: Clone Repository | რეპოზიტორიის კლონირება

1. **Go to your repository** on GitHub
2. **Click** green "Code" button
3. **Copy** the HTTPS URL (looks like: `https://github.com/username/financial-teacher-bot.git`)

4. **Open Terminal/Command Prompt**
5. **Navigate to where you want to save**:
   ```bash
   cd Documents  # or any folder you prefer
   ```

6. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/financial-teacher-bot.git
   ```
   Replace `YOUR_USERNAME` with your actual GitHub username

7. **Enter the folder**:
   ```bash
   cd financial-teacher-bot
   ```

#### Step 4.3: Add Your Bot Files | ფაილების დამატება

1. **Copy all your bot files** into this folder:
   - `financial_bot.py`
   - `requirements.txt`
   - `.env.example`
   - `README.md`
   - `QUICKSTART.md`
   - `.gitignore`

2. **Check what files were added**:
   ```bash
   git status
   ```

3. **Add all files**:
   ```bash
   git add .
   ```

4. **Commit the files**:
   ```bash
   git commit -m "Initial commit: Georgian financial teacher bot"
   ```

5. **Push to GitHub**:
   ```bash
   git push origin main
   ```
   
   If it asks for authentication:
   - **Username**: Your GitHub username
   - **Password**: You need a Personal Access Token (see below)

#### Creating GitHub Personal Access Token | GitHub Token-ის შექმნა

If `git push` asks for password:

1. **Go to** GitHub.com → Settings (your profile)
2. **Click** "Developer settings" (left sidebar, bottom)
3. **Click** "Personal access tokens" → "Tokens (classic)"
4. **Click** "Generate new token" → "Generate new token (classic)"
5. **Fill in**:
   - Note: `Financial Bot Token`
   - Expiration: `90 days` (or longer)
   - Check: ✅ `repo` (full control of private repositories)
6. **Click** "Generate token"
7. **Copy** the token (you'll only see it once!)
8. **Use this token as password** when Git asks

---

### Method 2: Using GitHub Web Interface | ვებ ინტერფეისით ატვირთვა

Easier but limited:

1. **Go to** your repository on GitHub.com
2. **Click** "Add file" → "Upload files"
3. **Drag and drop** all your bot files (except `.env` - never upload this!)
4. **Write** commit message: `Add bot files`
5. **Click** "Commit changes"

⚠️ **Important**: Never upload your `.env` file! Only upload `.env.example`

---

## Step 5: Deploy to Cloud | Cloud-ზე განთავსება

Now your code is on GitHub! Let's run it 24/7.

### Option A: PythonAnywhere (FREE) ✅ რეკომენდირებული

**Best for beginners - Free tier available**

#### Step 5A.1: Create Account

1. **Go to** [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Click** "Start running Python online in less than a minute!"
3. **Choose** "Create a Beginner account" (FREE)
4. **Fill in** your details
5. **Verify** email

#### Step 5A.2: Upload Code

**Option 1 - Using Git (Recommended):**

1. **Open** "Consoles" tab
2. **Click** "Bash"
3. **Clone your repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/financial-teacher-bot.git
   cd financial-teacher-bot
   ```

**Option 2 - Upload Files:**

1. **Go to** "Files" tab
2. **Upload** all your bot files

#### Step 5A.3: Install Dependencies

In the Bash console:
```bash
cd financial-teacher-bot
pip3 install --user -r requirements.txt
```

#### Step 5A.4: Set Environment Variables

1. **Go to** "Files" tab
2. **Create** a new file: `.env`
3. **Add** your keys:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   OPENAI_API_KEY=your_openai_key_here
   ```
4. **Save** the file

Or use bash:
```bash
cd financial-teacher-bot
nano .env
# Paste your environment variables
# Press Ctrl+X, then Y, then Enter to save
```

#### Step 5A.5: Modify Bot for PythonAnywhere

We need to load the .env file. Edit `financial_bot.py`:

1. **Open** the file editor
2. **Add** at the top (after imports):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
3. **Update** requirements.txt:
   ```bash
   echo "python-dotenv==1.0.0" >> requirements.txt
   pip3 install --user python-dotenv
   ```

#### Step 5A.6: Run the Bot

**For Free Account (Scheduled Tasks):**

Free accounts can't run always-on tasks, but you can use scheduled tasks:

1. **Go to** "Tasks" tab
2. **Create** 3 scheduled tasks:
   - Task 1: At 09:00 daily
   - Task 2: At 12:50 daily
   - Task 3: At 16:50 daily
3. **Command** for each:
   ```bash
   cd /home/YOUR_USERNAME/financial-teacher-bot && python3 financial_bot.py --send-now
   ```

**Note**: You'll need to modify the bot to support `--send-now` flag, or upgrade to paid account.

**For Paid Account ($5/month):**

1. **Go to** "Web" tab
2. **Scroll** to "Always-on tasks"
3. **Add** new task:
   ```
   Working directory: /home/YOUR_USERNAME/financial-teacher-bot
   Command: python3 financial_bot.py
   ```
4. **Enable** the task

---

### Option B: Heroku (Paid, but simple)

Heroku removed free tier, but it's still good for $7/month.

#### Step 5B.1: Create Account

1. **Go to** [heroku.com](https://www.heroku.com)
2. **Sign up** for account

#### Step 5B.2: Install Heroku CLI

**Windows**: Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

**Mac**:
```bash
brew tap heroku/brew && brew install heroku
```

**Linux**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 5B.3: Create Procfile

In your bot folder, create `Procfile` (no extension):
```
worker: python financial_bot.py
```

#### Step 5B.4: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create financial-teacher-bot

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHAT_ID=your_chat_id
heroku config:set OPENAI_API_KEY=your_openai_key

# Deploy
git push heroku main

# Start the worker
heroku ps:scale worker=1

# Check logs
heroku logs --tail
```

---

### Option C: Railway.app (Free $5 credit/month)

1. **Go to** [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click** "New Project"
4. **Select** "Deploy from GitHub repo"
5. **Choose** your bot repository
6. **Add** environment variables in settings
7. **Deploy**!

---

### Option D: DigitalOcean ($4/month)

1. **Create** account at [digitalocean.com](https://www.digitalocean.com)
2. **Create** a Droplet (Ubuntu)
3. **SSH** into your server
4. **Install** dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```
5. **Clone** your repository
6. **Install** requirements
7. **Set up** systemd service to run bot
8. **Enable** auto-start

---

## Step 6: Keep Bot Running 24/7 | 24/7 მუშაობა

### Using systemd (for Linux servers)

1. **Create** service file:
   ```bash
   sudo nano /etc/systemd/system/financial-bot.service
   ```

2. **Add** this content:
   ```ini
   [Unit]
   Description=Georgian Financial Teacher Bot
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/financial-teacher-bot
   ExecStart=/usr/bin/python3 /path/to/financial-teacher-bot/financial_bot.py
   Restart=always
   RestartSec=10
   Environment="TELEGRAM_BOT_TOKEN=your_token"
   Environment="TELEGRAM_CHAT_ID=your_chat_id"
   Environment="OPENAI_API_KEY=your_openai_key"

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable** and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable financial-bot
   sudo systemctl start financial-bot
   ```

4. **Check** status:
   ```bash
   sudo systemctl status financial-bot
   ```

5. **View** logs:
   ```bash
   sudo journalctl -u financial-bot -f
   ```

---

## 🔄 Updating Your Bot | ბოტის განახლება

When you want to update your bot:

```bash
# Make changes to your files locally
# Then commit and push:

git add .
git commit -m "Description of changes"
git push origin main

# On your server (PythonAnywhere/DigitalOcean/etc):
cd financial-teacher-bot
git pull origin main
# Restart the bot
```

---

## 📊 Monitoring | მონიტორინგი

### Check if bot is running:

**PythonAnywhere**: Check Tasks tab

**Heroku**:
```bash
heroku logs --tail
```

**Linux server**:
```bash
sudo systemctl status financial-bot
```

### View logs:

**PythonAnywhere**: Click on task → View log

**Heroku**:
```bash
heroku logs --tail
```

**Linux server**:
```bash
sudo journalctl -u financial-bot -f
```

---

## ⚠️ Security Best Practices | უსაფრთხოების წესები

### ✅ DO | გააკეთეთ:
- ✅ Use `.env` file for secrets
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables on hosting platforms
- ✅ Upload `.env.example` (without real values)
- ✅ Rotate tokens if exposed
- ✅ Use strong passwords
- ✅ Enable 2FA on GitHub

### ❌ DON'T | არ გააკეთოთ:
- ❌ Never commit `.env` to GitHub
- ❌ Never hardcode API keys in code
- ❌ Never share your bot token publicly
- ❌ Never commit sensitive data
- ❌ Don't use same password everywhere

---

## 🐛 Troubleshooting | პრობლემების გადაჭრა

### Bot not sending messages

1. **Check** environment variables are set
2. **Verify** bot token is correct
3. **Check** you messaged the bot first
4. **Verify** chat ID is correct
5. **Check** OpenAI API has credits
6. **View** logs for errors

### Git push rejected

```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### Permission denied on Linux

```bash
# Make sure files are owned by your user
sudo chown -R $USER:$USER /path/to/financial-teacher-bot
```

### Module not found

```bash
pip3 install -r requirements.txt --user
```

---

## 💡 Tips | რჩევები

1. **Test locally first** before deploying
2. **Use git branches** for testing new features
3. **Check logs regularly** to catch errors
4. **Monitor OpenAI costs** in your dashboard
5. **Backup your .env file** securely
6. **Keep Python and dependencies updated**
7. **Use meaningful commit messages**

---

## 📚 Useful Resources | სასარგებლო რესურსები

- [GitHub Docs](https://docs.github.com)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI API Docs](https://platform.openai.com/docs)

---

## 🎉 Success! | წარმატება!

თქვენი ბოტი ახლა მუშაობს GitHub-ზე და Cloud-ზე! 🚀

Your bot is now running on GitHub and Cloud! 🚀

**Next Steps:**
1. Monitor your bot's messages
2. Adjust content if needed
3. Check OpenAI usage
4. Enjoy your financial education! 📈💰

---

**გისურვებთ წარმატებებს! Good luck!** 🌟
