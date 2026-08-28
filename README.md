# 👑 Winning Heaven — VIP Email Marketing & Anti-Spam Dispatch Engine

A high-performance, automated bulk email marketing tool customized for **[winningheaven.com](https://winningheaven.com)** and configured with your Hostinger business email.

---

## 🚀 Quick Start (Running the Dashboard)

The application is already running at **`http://127.0.0.1:5050`**!

### To open or restart the dashboard anytime:
1. **Method 1 (One-Click on Mac):** Double-click [`Run_Email_Marketing.command`](file:///Users/apple/Desktop/Email_Marketing/Run_Email_Marketing.command)
2. **Method 2 (Terminal):**
   ```bash
   cd /Users/apple/Desktop/Email_Marketing
   ./start.sh
   # Or: python3 app.py
   ```
3. Open your browser and go to: **[http://127.0.0.1:5050](http://127.0.0.1:5050)**

---

## ⚙️ Configured Hostinger Credentials

- **SMTP Host:** `smtp.hostinger.com`
- **Port:** `465` (SSL Encrypted) / `587` (TLS)
- **Sender Email:** `verified@winningheaven.com`
- **Sender Password:** `0761071Na@`
- **Sender Display Name:** `Winning Heaven VIP`
- **Website Target:** `https://winningheaven.com`

---

## 📊 Client Sheet Analysis

- **File:** [`client sheet.xlsx`](file:///Users/apple/Desktop/Email_Marketing/client%20sheet.xlsx)
- **Total Valid Unique Leads:** **1,177 emails**
- All emails are pre-loaded in the queue, automatically deduplicated and validated.

---

## 🛡️ Built-in Anti-Spam & Deliverability Engine

To ensure your emails land directly in the **Primary Inbox** (and never in Spam/Junk):
1. **Human-like Throttling:** 3 to 6-second randomized delay between each email.
2. **Batch Sending & Cool-Down:** Sends 50 emails, then takes a 60s pause to respect Hostinger's hourly/daily limits.
3. **Multi-Part MIME (HTML + Plain-Text):** Sends both high-res HTML and clean plain-text fallback.
4. **RFC-Compliant Headers:** Unique Message-IDs, Date headers, and One-Click Unsubscribe headers.
5. **Campaign State Persistence:** Powered by SQLite (`campaign_data.db`) — if you stop or pause, it will never re-send duplicate emails to already contacted clients.

---

## ✉️ Pre-Loaded High-Converting Templates

1. **🌟 Celestial VIP Welcome (Highest Conversion):** Dark/Gold Vegas sweepstakes theme with instant cashouts & welcome bonus perks.
2. **⚡ High Roller & Instant Cashout Alert:** Action-oriented jackpot & fast withdrawal alert.
3. **✉️ 1-to-1 VIP Personal Note:** Ultra-high inbox deliverability text invitation.

---

## 🧪 Recommended Step-by-Step Workflow

1. Open **[http://127.0.0.1:5050](http://127.0.0.1:5050)** in your browser.
2. Under **"Send Test Email"**, enter your own personal Gmail/Yahoo address and click **"Send Test"**.
3. Open your personal email and verify that the message arrives in your inbox looking sharp.
4. When you are happy, click **"Start 1-Click Campaign"**!
5. Watch the live progress bar, sent counter, and real-time logs console.
