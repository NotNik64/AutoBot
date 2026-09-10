import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
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

class HealthHandler(BaseHTTPRequestHandler):
    """Minimal HTTP endpoint so Render's free Web Service tier sees an open port."""

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, *args):
        pass  # silence per-request logging


def start_health_server():
    # Render provides $PORT; default to 10000 for local runs.
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()


if __name__ == "__main__":
    # Run the Slack Socket Mode bot in a background thread...
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    threading.Thread(target=handler.start, daemon=True).start()
    # ...and block the main thread serving HTTP so Render's port scan passes.
    start_health_server()