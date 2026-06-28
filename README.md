# Refrena Bot

A Discord bot for tournament automation and integrations.

## Requirements
 - Done: role updates based on reactions to a specified post (with refresh on bot start and with !pronouns command)
 - Done: rule recall (!rule n posts the text of the corresponding rule from the rules channel, and mentions admins)
 - TBD: unit tests? maybe

## Setup

1. Virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure vars:
   - Copy `.env.example` to `.env`
   - Add token

5. Run the bot:
   ```bash
   python bot.py
   ```
