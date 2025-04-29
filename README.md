# 🧩 Discourse → Discord Webhook

A lightweight Python-based webhook that listens for events from a Discourse forum and forwards selected public updates to a Discord channel via a webhook.

---

## 🚀 Quick Start (via Docker)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/discourse-webhook.git
cd discourse-webhook
```

### 2. Create the `.env` file

Copy and edit the `.env.example` file:

```bash
cp .env.example .env
```

Edit the file and set the following values:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-id
DISCOURSE_SECRET=your_discourse_webhook_secret
```

### 3. Build and run the service

```bash
docker-compose up --build -d
```

The service will run on:  
📍 `http://localhost:5000/webhook` — ready to receive POST requests from Discourse.

---

## 🔐 Environment Variables

| Variable              | Description                                  |
|-----------------------|----------------------------------------------|
| `DISCORD_WEBHOOK_URL` | Your Discord webhook URL                     |
| `DISCOURSE_SECRET`    | Secret string used for validating signatures |

---

## 📁 Project Structure

```
.
├── webhook.py            # Main Flask webhook server
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Easy service orchestration
├── requirements.txt      # Python dependencies
├── .env.example          # Template for environment config
├── .gitignore            # Standard exclusions (includes .env)
├── .dockerignore         # Prevents temp files from entering the image
└── README.md             # You're reading this
```

---

## ⚙ How It Works

- ✅ Listens for Discourse events such as `topic_created` and `post_created`
- ✅ Filters out private messages (`topic_archetype = private_message`)
- ✅ Blocks system/bot users like `system`, `discobot`, `anonymous`
- ✅ Validates incoming requests via `X-Discourse-Event-Signature` header
- ✅ Sends clean, HTML-free summaries to your Discord channel
- 🚫 Ignores noisy events such as `topic_closed_status_updated`

---

## 🛠 Local Development (without Docker)

If needed, you can run the webhook directly:

```bash
pip install -r requirements.txt
cp .env.example .env
python webhook.py
```

The service will be available at `http://0.0.0.0:5000/webhook`.

---

## 🧪 Test a Webhook Manually

You can simulate a webhook call with `curl`:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Discourse-Event: post_created" \
  -H "X-Discourse-Event-Signature: sha256=..." \
  -d '{
        "post": {
          "username": "testuser",
          "cooked": "<p>Hello from Discourse!</p>",
          "topic_id": 123,
          "id": 456
        }
      }'
```

Replace the `X-Discourse-Event-Signature` with a real HMAC if using `DISCOURSE_SECRET`.

---

## 🧹 Stop & Cleanup

To stop the service and remove the container:

```bash
docker-compose down
```

---

## 🔒 Security Considerations

- `.env` contains sensitive credentials — **do not commit it**.
- Webhook signature is validated with `HMAC SHA256` using `DISCOURSE_SECRET`.
- Private system messages and admin notifications are **excluded by default**.

---
