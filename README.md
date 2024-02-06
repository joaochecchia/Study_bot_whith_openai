Discord Study Bot
The Discord Study Bot is a simple Discord bot designed to help users manage their study tasks, set Pomodoro timers, and interact with OpenAI for answering questions.

Features
Task Management:

Add, list, remove, and edit study tasks using simple commands.
Pomodoro Timer:

Define a Pomodoro timer by specifying the duration. The bot will periodically check what you are doing and encourage you to stay focused on your tasks.
OpenAI Chat:

Ask questions to the OpenAI model by starting your message with [.?]. The bot will interact with the OpenAI API to provide responses.
Prerequisites
Make sure you have the following installed and configured:

Python:

Install Python on your system. You can download it from python.org.
Dependencies:

Install the required Python packages using the following command:
bash
pip install -r requirements.txt
Discord Bot Token:

Create a Discord bot on the Discord Developer Portal.
Copy the bot token and update the .env file with your Discord bot token:
makefile

discord_token=YOUR_DISCORD_BOT_TOKEN
OpenAI API Key:

Sign up for an account on the OpenAI platform.
Obtain your OpenAI API key and update the .env file with your OpenAI API key:
makefile

openai_key=YOUR_OPENAI_API_KEY
Usage

Run the bot:

bash
Copy code
python bot.py
Invite the bot to your Discord server:

Use the Discord bot invite link provided in the Discord Developer Portal.
Interact with the bot:

Use the defined commands to manage tasks, set Pomodoro timers, and ask questions.

Contributing
Contributions are welcome! If you have any improvements or additional features, feel free to fork the repository and submit a pull request.

