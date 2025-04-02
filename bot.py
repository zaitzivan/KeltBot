import os
import yfinance as yf
import numpy as np
import pandas as pd
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

timeframes = {
    "5 minutes": "5m",
    "15 minutes": "15m",
    "30 minutes": "30m",
    "1 hour": "60m"
}

def calculate_keltner_channel(df, length=20, scalar=1.5):
    df['EMA'] = df['Close'].ewm(span=length, adjust=False).mean()
    df['TR'] = np.maximum.reduce([
        df['High'] - df['Low'],
        abs(df['High'] - df['Close'].shift(1)),
        abs(df['Low'] - df['Close'].shift(1))
    ])
    df['ATR'] = df['TR'].ewm(span=length, adjust=False).mean()
    df['Upper'] = df['EMA'] + scalar * df['ATR']
    df['Lower'] = df['EMA'] - scalar * df['ATR']
    return df.iloc[-1]['Upper'].item(), df.iloc[-1]['EMA'].item(), df.iloc[-1]['Lower'].item()

def get_keltner_values(ticker="^GSPC", interval="1h"):
    df = yf.download(ticker, period="7d", interval=interval)
    if df.empty or len(df) < 20:
        return None
    try:
        return calculate_keltner_channel(df)
    except:
        return None

@app.event("message")
def handle_kelt_command(event, say):
    text = event.get("text", "").strip()

    if text.lower().startswith("!kelt"):
        parts = text.split()
        ticker = parts[1].upper() if len(parts) > 1 else "^GSPC"

        response = f"*Keltner Channel Levels for ${ticker}:*\n"

        for label, interval in timeframes.items():
            values = get_keltner_values(ticker, interval)
            if values:
                top, mid, bot = values
                response += (
                    f"*Time frame: {label}*\n"
                    f"Top Kelt: {round(top, 2)}\n"
                    f"Middle Kelt: {round(mid, 2)}\n"
                    f"Bottom Kelt: {round(bot, 2)}\n"
                )
            else:
                response += f"*Time frame: {label}*\nCould not fetch data.\n"

        say(response)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
