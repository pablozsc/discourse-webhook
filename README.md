# Discourse → Discord Webhook

This Python-based webhook receives events from a Discourse forum and selectively forwards them to a Discord channel using a Discord webhook.

## 🔧 What It Does

This webhook filters, processes, and relays relevant forum activity from Discourse to Discord, with a focus on **privacy and clarity**.

### ✅ Core Features

- **Listens for webhooks** sent from a Discourse forum (e.g. `topic_created`, `post_created`).
- **Filters out messages** from system-level users like:
  - `system`
  - `discobot`
  - `anonymous`
- **Skips private messages** (`topic_archetype: "private_message"`) to avoid leaking sensitive or internal notifications to Discord.
- **Ignores unnecessary event types**, e.g. `topic_closed_status_updated`.
- **Strips HTML tags** from post content for clean formatting in Discord.
- **Sends Discord messages** only for relevant, public posts by real users.

### 📥 Events Processed

| Event Type        | Description                                | Action                      |
|-------------------|--------------------------------------------|-----------------------------|
| `topic_created`   | A new topic was created                    | Forwarded (unless blocked)  |
| `post_created`    | A new post was added to a topic            | Forwarded (unless blocked)  |
| Others            | All others (e.g. topic_closed)             | Ignored                     |

### ❌ What Gets Blocked

- Any message from users in the `BLOCKED_USERS` list.
- Any message associated with a topic marked as a private message.
- Events listed in the `BLOCKED_EVENTS` set.

## 🛠 Requirements

- Python 3.6+
- Flask
- requests

Install dependencies:

```bash
pip install flask requests