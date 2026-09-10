import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables from the .env file
load_dotenv()

# Pull tokens from the environment variables safely
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Initialize your app
app = App(token=SLACK_BOT_TOKEN)

# Handle the /ahoy-hoy slash command
@app.command("/ahoy-hoy")
def handle_ahoy_command(ack, command, say):
    ack()
    print(f"User {command['user_name']} used /ahoy-hoy!")
    say(f"Ahoy-hoy, <@{command['user_id']}>! Welcome to WIIT 88.9 FM AutoBot. 📻")

if __name__ == "__main__":
    # Start the app in Socket Mode
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()