from flask import Flask, request
import requests
import json
import re

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1342459643431223386/Eg_wAZNUPNt2yIPzGbCUNgi4_fJbvQNLP9SNxh3i2yp2cD4Kl5hfh8cZXGCBMqw3IzMa"

# List of users to exclude from sending to Discord
BLOCKED_USERS = {"system", "discobot", "anonymous"}  # Add more if needed

# List of event types to exclude from Discord notifications
BLOCKED_EVENTS = {"topic_closed_status_updated"}  # Add more if needed

def strip_html_tags(text):
    """Removes HTML tags from Discourse post content."""
    return re.sub(r"<.*?>", "", text)  # Removes all HTML tags

def is_blocked_user(data):
    """Checks if the event was triggered by a blocked user."""
    # Check if user info exists in "user" field (for most events)
    if "user" in data and data["user"]["username"].lower() in BLOCKED_USERS:
        return True

    # Check if user info exists in "post" field (for post_created events)
    if "post" in data and data["post"]["username"].lower() in BLOCKED_USERS:
        return True

    # Check if user info exists in "topic" field (for topic_created events)
    if "topic" in data:
        if "created_by" in data["topic"] and data["topic"]["created_by"]["username"].lower() in BLOCKED_USERS:
            return True
        if "last_poster" in data["topic"] and data["topic"]["last_poster"]["username"].lower() in BLOCKED_USERS:
            return True

    return False

def is_private_message(data):
    """Checks if the event is a private message."""
    if "topic" in data and data["topic"].get("topic_archetype") == "private_message":
        return True
    if "post" in data and data["post"].get("topic_archetype") == "private_message":
        return True
    return False

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get("X-Discourse-Event")
    data = request.json

    # Log event for debugging
    print(f"Received event: {event_type}")

    # Skip if the event type is in the blocked list
    if event_type in BLOCKED_EVENTS:
        print(f"🔹 Skipping event `{event_type}` (not relevant for Discord).")
        return "OK", 200  # Do nothing, just return OK

    # Check if the sender is in the BLOCKED_USERS list
    if is_blocked_user(data):
        print("🔹 Skipping message from blocked user (privacy protection).")
        return "OK", 200  # Do nothing, just return OK

    # Exclude private messages (admin notifications)
    if is_private_message(data):
        print("🔹 Skipping private message (admin notification).")
        return "OK", 200

    # Create message for Discord
    message_content = f"📢 **New event from Discourse:** `{event_type}`\n"

    if "topic" in data:
        title = data["topic"]["title"]
        url = f"https://forum.concordium.com/t/{data['topic']['id']}"
        message_content += f"**Topic:** [{title}]({url})\n"

    if "post" in data:
        raw_content = data["post"]["cooked"]  # HTML content from Discourse
        cleaned_content = strip_html_tags(raw_content)  # Remove HTML tags
        url = f"https://forum.concordium.com/t/{data['post']['topic_id']}?p={data['post']['id']}"
        message_content += f"**Post:** {cleaned_content[:100]}... ([Read more]({url}))\n"

    if "user" in data:
        username = data["user"]["username"]
        message_content += f"👤 **User:** {username}\n"

    # Send to Discord
    payload = {"content": message_content}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

    return "OK", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
