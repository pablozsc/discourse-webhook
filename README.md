# Discourse → Discord Webhook

A lightweight Python-based webhook that listens for events from a Discourse forum and forwards selected public updates to a Discord channel via a webhook.

---

## Quick Start (via Docker)

1. Clone the repository

```bash
git clone https://github.com/your-org/discourse-webhook.git
cd discourse-webhook
```

2. Configure environment variables

Copy and edit the .env.example file:
```
cp .env.example .env
```

Edit the file and set the following values:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-id
DISCOURSE_SECRET=your_discourse_webhook_secret
```

3. Build and run the service
```
docker-compose up --build -d
```

The service will run at:
📍 http://localhost:5000/webhook — ready to receive POST requests from Discourse.
## Environment Variables
	Variable		Description
	DISCORD_WEBHOOK_URL	Your Discord webhook URL
	DISCOURSE_SECRET	Secret string used for validating signatures

## Project Structure

```
├── webhook.py            # Main Flask webhook server
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose orchestration
├── requirements.txt      # Python dependencies
├── .env.example          # Template for environment config
├── .gitignore            # Standard exclusions (includes .env)
├── .dockerignore         # Prevents temp files from entering the image
└── README.md             # You are reading this
```

## How It Works

✅ Listens for Discourse events such as topic_created and post_created

✅ Filters out private messages (topic_archetype = private_message)

✅ Blocks system/bot users like system, discobot, anonymous

✅ Validates incoming requests via X-Discourse-Event-Signature header (HMAC SHA256)

✅ Sends clean, HTML-free summaries to your Discord channel

🚫 Ignores noisy events such as topic_closed_status_updated

## Production Deployment (nginx example)

To securely expose the webhook endpoint, use nginx as a reverse proxy in front of your app.
Add this to your nginx configuration:
```
location /webhook {
    proxy_pass         http://127.0.0.1:5000/webhook;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
}
```

Sample full server block:
```
server {
    listen 443 ssl;
    server_name your.domain.com;

    # ... SSL configuration goes here ...

    location /webhook {
        proxy_pass         http://127.0.0.1:5000/webhook;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```
Point your Discourse webhook to https://your.domain.com/webhook

Adjust SSL, firewall, and allowed IPs as appropriate for your environment.

## Security Considerations

.env contains sensitive credentials — never commit it.

Webhook signature is validated with HMAC SHA256 using your DISCOURSE_SECRET.

Private messages and admin notifications are excluded by default.

System/bot users are blocked to reduce noise and protect privacy.

## Requirements

Python 3.8+

	Docker (optional but recommended)

	Flask, requests, python-dotenv (requirements.txt)

	Discourse forum with webhook support

	Discord webhook URL

## Possible Improvements

    Advanced error logging (e.g., to Sentry or email)

    Configurable blocked users/events via environment

    Admin dashboard for monitoring incoming events

    Rate limiting and access controls

## Contributing & Support

Pull requests and issues are welcome!
For questions or feedback, please open an Issue or contact the maintainer.