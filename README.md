Discord Nuke Bot

A nuke bot for Discord.

Basic Commands

  !ping – Test the bot's latency
  !test – Check if the bot is working
  !help – Show the list of commands
  !talk – Make the bot say the given message

Moderation Commands

  !create <channel_name> – Create one or multiple text channels (max 100)
  
  !ban <@member|ALL> [reason] – Ban a member or everyone (excluding admins and the bot)

  !kick <@member|ALL> [reason] – Kick a member or everyone (excluding admins and the bot)

  !clear – Delete the last messages in the channel (1 to 10000)

  !confirm_ban_all – Confirm banning all members (after !ban ALL)

  !confirm_kick_all – Confirm kicking all members (after !kick ALL)

Spam Commands

  !spam – Send a message multiple times in the channel (max 5000)

Dependencies
  Python 3.8+
  discord.py – to interact with Discord
  python-dotenv – to load the token from the .env file
  requests (optional, if you use APIs or images)
  beautifulsoup4 (optional, if you scrape images)
  Installation
  pip install discord.py python-dotenv requests beautifulsoup4
  Setup Requirements

This bot requires a .env file containing the bot token:

  TOKEN=your_bot_token_here

Without the .env file and a valid token, the bot will not work.

To create a Discord bot:

  Go to the Discord Developer Portal
  Create a new application
  Add a bot to the application
  Copy the bot token and place it in the .env file
  Generate an invite link using OAuth2 (scope: bot)
  Invite the bot to your server

Run the bot:

  python main.py


Disclaimer
  This bot is intended for testing or trolling in servers where you have permission. The developer is not responsible for any misuse, damage, or issues caused by this bot. Use at your own risk.
