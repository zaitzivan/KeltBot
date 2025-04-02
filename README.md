# Slack Keltner Bot (Working Example)

This bot responds to `!kelt` in Slack and returns Keltner Channel values for $SPX at multiple timeframes.

## Setup

1. Create a `.env` file from the `.env.example` file.
2. Paste in your working Slack tokens:
   - SLACK_BOT_TOKEN: from OAuth & Permissions
   - SLACK_APP_TOKEN: from App-Level Token with `connections:write`
3. Create virtual env (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the bot:
   ```
   python bot.py
   ```

Make sure your Slack app is installed, has `chat:write` and `app_mentions:read` scopes, and that Socket Mode is enabled.
