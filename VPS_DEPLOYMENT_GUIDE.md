# 🚀 VPS Deployment Guide: `tool.winningheaven.com`

Yeh guide aap ko step-by-step batayegi ke aap is Email Marketing Tool ko apne VPS server par subdomain **`tool.winningheaven.com`** par kaise live karein, **bina aap ki main live website (`winningheaven.com`) ko disturb kiye**.

---

## 🛡️ Important Safety Rule (Main Website Safe Rahegi)
- Aap ki main domain `winningheaven.com` pehle se VPS par live hai.
- Nginx mein hum **aik alag file** banayenge: `/etc/nginx/sites-available/tool.winningheaven.com`.
- Yeh file main website ki settings ko bilkul touch nahi karegi.
- Testing command `nginx -t` chalane se ensure hoga ke koi syntax error na ho.

---

## 📋 Step 1: DNS Record Add Karein (Subdomain Pointing)

Jahan aap ka domain manage hota hai (Cloudflare, Namecheap, ya Hostinger DNS):
1. **DNS Management** open karein.
2. Naya **A Record** add karein:
   - **Type**: `A`
   - **Name / Host**: `tool`
   - **IPv4 Address**: `Aap Ka VPS IP Address` (Jahan main website chal rahi hai)
   - **TTL**: Auto / 1 min (agar Cloudflare hai toh Proxy ON / Orange Cloud rakh sakte hain).

*Note: DNS update hone mein 2 se 10 minute lagte hain.*

---

## 📂 Step 2: VPS Par Project Folder Banayein & Files Upload Karein

Apne VPS terminal (SSH) mein login karein:
```bash
ssh root@YOUR_VPS_IP
```

1. Folder banayein:
```bash
mkdir -p /var/www/tool.winningheaven.com
cd /var/www/tool.winningheaven.com
```

2. Apne Mac se files upload karein:
Aap Mac Terminal se `scp` ya `rsync` use kar sakte hain, ya zip bana kar SFTP / Cyberpanel / Filezilla se upload kar sakte hain:
```bash
# Apne Mac terminal se run karein:
rsync -avz --exclude 'node_modules' --exclude '.git' /Users/apple/Desktop/Email_Marketing/ root@YOUR_VPS_IP:/var/www/tool.winningheaven.com/
```

---

## 🐍 Step 3: Python Environment & Dependencies Setup

VPS par `/var/www/tool.winningheaven.com` directory mein yeh commands run karein:

```bash
cd /var/www/tool.winningheaven.com

# Python virtual environment banayein
python3 -m venv venv

# Virtual environment activate karein
source venv/bin/activate

# Pip upgrade aur required packages install karein
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Step 4: `config.json` Update Karein (Click Tracking Domain)

File `/var/www/tool.winningheaven.com/config.json` ko open karein:
```bash
nano /var/www/tool.winningheaven.com/config.json
```
Is mein `"tracking_base_url"` ko change kar ke live subdomain kar dein:
```json
"tracking_base_url": "https://tool.winningheaven.com",
```
*(Is se recipients jab email mein link click karenge toh `tool.winningheaven.com/r?e=...` ke zariye track ho kar automatically `https://winningheaven.com` par redirect ho jayenge!)*

---

## 🔄 Step 5: Background 24/7 Service Setup (Systemd)

Taake tool background mein continuous chalta rahe aur VPS restart hone par khud ba khud start ho jaye:

1. Ready-made service file copy karein:
```bash
cp /var/www/tool.winningheaven.com/email-marketing.service /etc/systemd/system/email-marketing.service
```

2. Service ko reload aur start karein:
```bash
systemctl daemon-reload
systemctl enable email-marketing
systemctl start email-marketing
```

3. Status check karein (Green "active (running)" dikhna chahiye):
```bash
systemctl status email-marketing
```

---

## 🌐 Step 6: Isolated Nginx Configuration (Subdomain Setup)

Yeh step aap ki main website ko 100% safe rakhta hai:

1. Ready-made Nginx config file copy karein:
```bash
cp /var/www/tool.winningheaven.com/nginx_tool_winningheaven.conf /etc/nginx/sites-available/tool.winningheaven.com
```

2. Config file ko enable karein:
```bash
ln -s /etc/nginx/sites-available/tool.winningheaven.com /etc/nginx/sites-enabled/
```

3. **Safe Check (Very Important)**:
```bash
nginx -t
```
Agar output aaye:
`nginx: configuration file /etc/nginx/nginx.conf test is successful`
Toh Nginx reload karein:
```bash
systemctl reload nginx
```
*(Agar koi error aaye toh reload na karein, pehle error check karein, main website bilkul chalti rahegi).*

---

## 🔒 Step 7: Free SSL Certificate (Let's Encrypt / Certbot)

Apne subdomain ko secure HTTPS banane ke liye certbot run karein:
```bash
certbot --nginx -d tool.winningheaven.com
```
Certbot khud ba khud SSL install kar dega aur Nginx file ko HTTPS par redirect set kar dega.

---

## ✅ Step 8: Done! Live Test Karein

Ab apne browser mein open karein:
👉 **`https://tool.winningheaven.com`**

Aap ke samnay secure **Admin Login Screen** aayegi!

---

## 🔐 Admin Login Credentials

Aap code ke andar set kiye gaye credentials se login kar sakte hain:

| Field | Login Value |
|---|---|
| **Username** | `admin` *(ya `winningheaven` / `verified@winningheaven.com`)* |
| **Password** | `WinningHeaven@2026` |

> [!TIP]
> **Password Change Kaise Karein?**
> Agar aap password ya username badalna chahein toh file `/var/www/tool.winningheaven.com/app.py` mein line 24 par `ADMIN_CREDENTIALS` dictionary mein apni marzi ka username/password set kar ke `systemctl restart email-marketing` chala dein!

---

## 🛠️ Handy Management Commands

| Action | Command |
|---|---|
| **Live Logs Check** | `journalctl -u email-marketing -f` ya `tail -f /var/www/tool.winningheaven.com/app.log` |
| **Restart Tool** | `systemctl restart email-marketing` |
| **Stop Tool** | `systemctl stop email-marketing` |
| **Status Check** | `systemctl status email-marketing` |
| **Nginx Reload** | `systemctl reload nginx` |
