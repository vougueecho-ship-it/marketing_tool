import os
import glob
import json
import time
import random
import re
import smtplib
import ssl
import sqlite3
import socket
import threading
import logging
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from email.header import Header
import openpyxl
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "campaign_data.db")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

os.makedirs(UPLOADS_DIR, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "smtp_host": "smtp.hostinger.com",
        "smtp_port": 465,
        "use_ssl": True,
        "sender_email": "verified@winningheaven.com",
        "sender_password": "0761071Na@",
        "sender_name": "Winning Heaven VIP",
        "reply_to": "verified@winningheaven.com",
        "tracking_base_url": "",
        "min_delay_seconds": 3,
        "max_delay_seconds": 6,
        "batch_size": 50,
        "batch_pause_seconds": 60,
        "target_url": "https://winningheaven.com",
        "excel_file": "client sheet.xlsx",
        "active_template_id": "day1_morning_welcome"
    }

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT DEFAULT 'client sheet.xlsx',
            email TEXT,
            status TEXT DEFAULT 'pending', -- pending, sent, failed
            sent_at TEXT,
            error_msg TEXT,
            attempts INTEGER DEFAULT 0,
            sender_email TEXT,
            UNIQUE(file_name, email)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            click_count INTEGER DEFAULT 1,
            first_clicked_at TEXT,
            last_clicked_at TEXT,
            ip_address TEXT,
            user_agent TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT,
            recipient TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sender_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            provider TEXT DEFAULT 'custom', -- hostinger, gmail, custom
            smtp_host TEXT,
            smtp_port INTEGER DEFAULT 465,
            use_ssl INTEGER DEFAULT 1,
            sender_email TEXT UNIQUE,
            sender_password TEXT,
            sender_name TEXT,
            reply_to TEXT,
            daily_limit INTEGER DEFAULT 80,
            enabled INTEGER DEFAULT 1,
            created_at TEXT
        )
    """)
    
    # Check if columns exist in recipients table
    cursor.execute("PRAGMA table_info(recipients)")
    cols = [r["name"] for r in cursor.fetchall()]
    if "file_name" not in cols:
        try:
            cursor.execute("ALTER TABLE recipients ADD COLUMN file_name TEXT DEFAULT 'client sheet.xlsx'")
        except Exception:
            pass
    if "sender_email" not in cols:
        try:
            cursor.execute("ALTER TABLE recipients ADD COLUMN sender_email TEXT")
        except Exception:
            pass

    # Auto-migrate initial account from config.json if table is empty
    cursor.execute("SELECT COUNT(*) FROM sender_accounts")
    if cursor.fetchone()[0] == 0:
        cfg = load_config()
        if cfg.get("sender_email"):
            provider = "hostinger" if "hostinger" in cfg.get("smtp_host", "").lower() else ("gmail" if "gmail" in cfg.get("smtp_host", "").lower() else "custom")
            now_str = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                cursor.execute("""
                    INSERT INTO sender_accounts (name, provider, smtp_host, smtp_port, use_ssl, sender_email, sender_password, sender_name, reply_to, daily_limit, enabled, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
                """, (
                    f"{provider.capitalize()} Main ({cfg.get('sender_email')})",
                    provider,
                    cfg.get("smtp_host", "smtp.hostinger.com"),
                    int(cfg.get("smtp_port", 465)),
                    1 if cfg.get("use_ssl", True) else 0,
                    cfg.get("sender_email"),
                    cfg.get("sender_password", ""),
                    cfg.get("sender_name", "Winning Heaven VIP"),
                    cfg.get("reply_to", cfg.get("sender_email")),
                    80, # Default to 80 per user's requirement
                    now_str
                ))
            except Exception as e:
                print(f"Migration error for initial sender account: {e}")

    conn.commit()
    conn.close()

def get_sender_accounts():
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sender_accounts ORDER BY id ASC")
    rows = cursor.fetchall()
    accounts = [dict(r) for r in rows]
    
    today_str = time.strftime("%Y-%m-%d")
    for acc in accounts:
        em = acc["sender_email"]
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE sender_email = ? AND status = 'sent' AND sent_at LIKE ?", (em, f"{today_str}%"))
        acc["sent_today"] = cursor.fetchone()[0]
        acc["remaining_today"] = max(0, acc["daily_limit"] - acc["sent_today"])
    conn.close()
    return accounts

def add_sender_account(data):
    init_db()
    name = data.get("name", "").strip()
    provider = data.get("provider", "custom").strip().lower()
    smtp_host = data.get("smtp_host", "").strip()
    smtp_port = int(data.get("smtp_port", 465 if provider != "gmail" else 587))
    use_ssl = 1 if data.get("use_ssl", True) else 0
    sender_email = data.get("sender_email", "").strip().lower()
    sender_password = data.get("sender_password", "").strip()
    sender_name = data.get("sender_name", "").strip() or "Winning Heaven VIP"
    reply_to = data.get("reply_to", "").strip() or sender_email
    daily_limit = int(data.get("daily_limit", 80))

    if not sender_email or "@" not in sender_email:
        return False, "Please enter a valid email address."
    if not sender_password:
        return False, "Password / App Password is required."
    if not smtp_host:
        if provider == "gmail":
            smtp_host = "smtp.gmail.com"
            smtp_port = 587
            use_ssl = 0
        elif provider == "hostinger":
            smtp_host = "smtp.hostinger.com"
            smtp_port = 465
            use_ssl = 1
        else:
            return False, "SMTP Host is required."

    if not name:
        name = f"{provider.capitalize()} ({sender_email})"

    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO sender_accounts (name, provider, smtp_host, smtp_port, use_ssl, sender_email, sender_password, sender_name, reply_to, daily_limit, enabled, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (name, provider, smtp_host, smtp_port, use_ssl, sender_email, sender_password, sender_name, reply_to, daily_limit, now_str))
        conn.commit()
        acc_id = cursor.lastrowid
        conn.close()
        log_event(f"➕ Added new sender account: {sender_email} (Limit: {daily_limit}/day)")
        return True, f"Account '{sender_email}' added successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"Account '{sender_email}' already exists in sender list."
    except Exception as e:
        conn.close()
        return False, f"Error adding account: {str(e)}"

def update_sender_account(account_id, data):
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sender_accounts WHERE id = ?", (account_id,))
    acc = cursor.fetchone()
    if not acc:
        conn.close()
        return False, "Account not found."

    fields = []
    params = []
    for k in ["name", "provider", "smtp_host", "smtp_port", "use_ssl", "sender_password", "sender_name", "reply_to", "daily_limit", "enabled"]:
        if k in data:
            fields.append(f"{k} = ?")
            params.append(data[k])
    
    if "sender_email" in data and data["sender_email"].strip().lower() != acc["sender_email"]:
        fields.append("sender_email = ?")
        params.append(data["sender_email"].strip().lower())

    if not fields:
        conn.close()
        return True, "No changes updated."

    params.append(account_id)
    query = f"UPDATE sender_accounts SET {', '.join(fields)} WHERE id = ?"
    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()
        log_event(f"✏️ Updated sender account ID {account_id}")
        return True, "Account updated successfully."
    except Exception as e:
        conn.close()
        return False, f"Update failed: {str(e)}"

def delete_sender_account(account_id):
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sender_email FROM sender_accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Account not found."
    
    email = row["sender_email"]
    cursor.execute("DELETE FROM sender_accounts WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()
    log_event(f"🗑️ Deleted sender account: {email}")
    return True, f"Account '{email}' deleted successfully."


def log_event(message, level="INFO", recipient=""):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, level, message, recipient) VALUES (?, ?, ?, ?)",
                   (timestamp, level, message, recipient))
    conn.commit()
    conn.close()
    print(f"[{timestamp}] [{level}] {message}")

ENGAGED_LEADS_FILENAME = "engaged_hot_leads.csv"
ENGAGED_LEADS_PATH = os.path.join(UPLOADS_DIR, ENGAGED_LEADS_FILENAME)

def sync_engaged_leads_file():
    """
    Saves and synchronizes all hot clicked leads into a standalone CSV file:
    uploads/engaged_hot_leads.csv
    This file is immediately visible under Lead Files & Lists for 1-click re-engagement campaigns!
    """
    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email, click_count, first_clicked_at, last_clicked_at, ip_address FROM clicks ORDER BY click_count DESC, last_clicked_at DESC")
        rows = cursor.fetchall()
        conn.close()

        with open(ENGAGED_LEADS_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Email", "Total Clicks", "First Clicked", "Last Clicked", "IP Address", "Status"])
            for r in rows:
                writer.writerow([r["email"], r["click_count"], r["first_clicked_at"], r["last_clicked_at"], r["ip_address"] or "", "HOT_LEAD"])
    except Exception as e:
        print(f"[ENGAGED LEADS SYNC ERROR] {e}")

def record_click(email, ip="", user_agent=""):
    if not email:
        return 0
    email = email.strip().lower()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, click_count FROM clicks WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        new_count = row["click_count"] + 1
        cursor.execute("""
            UPDATE clicks 
            SET click_count = ?, last_clicked_at = ?, ip_address = ?, user_agent = ?
            WHERE id = ?
        """, (new_count, now_str, ip, user_agent, row["id"]))
    else:
        new_count = 1
        cursor.execute("""
            INSERT INTO clicks (email, click_count, first_clicked_at, last_clicked_at, ip_address, user_agent)
            VALUES (?, 1, ?, ?, ?, ?)
        """, (email, now_str, now_str, ip, user_agent))
    
    conn.commit()
    conn.close()
    log_event(f"🎯 LINK CLICKED: {email} (Total clicks: {new_count})", level="SUCCESS", recipient=email)
    
    # Automatically sync clicked lead into standalone CSV file
    sync_engaged_leads_file()
    
    return new_count

EXCLUDED_STAFF_EMAILS = {
    "sahil123@gmail.com",
    "sagar123@gmail.com",
    "blackpanther231@gmail.com",
    "kevin123@gmail.com",
    "shadow225@gmail.com",
    "sophia909@gmail.com",
    "spidy8772@gmail.com",
    "staff@jackpot.com",
    "verified@winningheaven.com",
    "islampakistan143@gmail.com",
    "msdhoni746432@gmail.com",
    "earningnepal7@gmail.com",
    "jackpotroyals604@gmail.com",
}

def parse_emails_from_file(full_path):
    emails = []
    ext = os.path.splitext(full_path)[1].lower()
    
    if ext in [".xlsx", ".xls"]:
        try:
            wb = openpyxl.load_workbook(full_path, data_only=True)
            sheet = wb.active
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if cell and isinstance(cell, str):
                        clean = cell.strip().lower()
                        if "@" in clean and "." in clean and clean not in EXCLUDED_STAFF_EMAILS:
                            emails.append(clean)
        except Exception as e:
            log_event(f"Error parsing Excel {full_path}: {str(e)}", level="ERROR")
    elif ext in [".csv", ".txt"]:
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    for cell in row:
                        if cell and isinstance(cell, str):
                            clean = cell.strip().lower()
                            if "@" in clean and "." in clean and clean not in EXCLUDED_STAFF_EMAILS:
                                emails.append(clean)
        except Exception as e:
            log_event(f"Error parsing CSV {full_path}: {str(e)}", level="ERROR")
            
    return list(dict.fromkeys(emails))

def load_file_recipients(file_name):
    init_db()
    
    # Look in root and uploads
    path1 = os.path.join(BASE_DIR, file_name)
    path2 = os.path.join(UPLOADS_DIR, file_name)
    full_path = path1 if os.path.exists(path1) else path2
    
    if not os.path.exists(full_path):
        log_event(f"Lead file not found: {file_name}", level="ERROR")
        return 0, 0

    try:
        unique_emails = parse_emails_from_file(full_path)
        conn = get_db()
        cursor = conn.cursor()
        
        inserted = 0
        for em in unique_emails:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO recipients (file_name, email, status) 
                    VALUES (?, ?, 'pending')
                """, (file_name, em))
                if cursor.rowcount > 0:
                    inserted += 1
            except Exception:
                pass
        
        conn.commit()
        conn.close()
        
        log_event(f"Loaded {len(unique_emails)} leads for list '{file_name}' ({inserted} newly added)")
        return len(unique_emails), inserted
    except Exception as e:
        log_event(f"Failed to load lead file {file_name}: {str(e)}", level="ERROR")
        return 0, 0

def get_available_lead_files():
    init_db()
    files_map = {}
    
    # Check root workspace files
    for ext in ["*.xlsx", "*.xls", "*.csv", "*.txt"]:
        for fpath in glob.glob(os.path.join(BASE_DIR, ext)):
            fname = os.path.basename(fpath)
            if fname not in ["package.json", "package-lock.json"]:
                files_map[fname] = fpath
                
    # Check uploads folder
    for ext in ["*.xlsx", "*.xls", "*.csv", "*.txt"]:
        for fpath in glob.glob(os.path.join(UPLOADS_DIR, ext)):
            fname = os.path.basename(fpath)
            files_map[fname] = fpath

    results = []
    conn = get_db()
    cursor = conn.cursor()
    
    for fname, fpath in files_map.items():
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ?", (fname,))
        in_db_count = cursor.fetchone()[0]
        
        # If not in DB, parse email count
        if in_db_count == 0:
            emails = parse_emails_from_file(fpath)
            total = len(emails)
        else:
            total = in_db_count
            
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'sent'", (fname,))
        sent = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'failed'", (fname,))
        failed = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'pending'", (fname,))
        pending = cursor.fetchone()[0]

        file_size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
        size_kb = f"{round(file_size / 1024, 1)} KB"

        results.append({
            "name": fname,
            "path": fpath,
            "size": size_kb,
            "total": total,
            "sent": sent,
            "failed": failed,
            "pending": pending if in_db_count > 0 else total
        })
        
    conn.close()
    return results

def process_spintax(text):
    """
    Processes spintax patterns like {option1|option2|option3}.
    Safely ignores single placeholders like {email} or {{email}}.
    Evaluates recursively up to 20 passes to support nested spins.
    """
    if not text or not isinstance(text, str):
        return text
    
    pattern = re.compile(r'\{([^{}]*\|[^{}]*)\}')
    iterations = 0
    while iterations < 20:
        match = pattern.search(text)
        if not match:
            break
        choices = match.group(1).split('|')
        replacement = random.choice(choices)
        text = text[:match.start()] + replacement + text[match.end():]
        iterations += 1
    return text

def wrap_tracking_links(content, recipient_email, tracking_base_url=None, target_url="https://winningheaven.com"):
    """
    Ensures email links & CTA buttons ALWAYS track clicks for every recipient on mobile & desktop.
    Wraps links via: {base_url}/r?e={encoded_email}&dest={encoded_dest}
    When recipient clicks, their email is recorded in Engaged Hot Leads and saved to uploads/engaged_hot_leads.csv.
    """
    if not content:
        return ""

    clean_email = recipient_email.strip().lower()
    encoded_email = urllib.parse.quote(clean_email)
    
    base_url = (tracking_base_url or "").strip().rstrip('/')
    if not base_url or "127.0.0.1" in base_url or "localhost" in base_url or "0.0.0.0" in base_url:
        try:
            cfg = load_config()
            cfg_url = (cfg.get("tracking_base_url") or "").strip().rstrip('/')
            if cfg_url and "127.0.0.1" not in cfg_url and "localhost" not in cfg_url:
                base_url = cfg_url
            else:
                base_url = "https://tool.winningheaven.com"
        except Exception:
            base_url = "https://tool.winningheaven.com"

    default_dest = (target_url or "https://winningheaven.com").strip()
    encoded_default_dest = urllib.parse.quote(default_dest)
    default_track_link = f"{base_url}/r?e={encoded_email}&dest={encoded_default_dest}"

    def link_replacer(match):
        orig_link = match.group(0)
        if "/r?e=" in orig_link or "/api/track" in orig_link:
            return orig_link
        encoded_dest = urllib.parse.quote(orig_link)
        return f"{base_url}/r?e={encoded_email}&dest={encoded_dest}"

    # 1. Wrap all winningheaven.com links & buttons
    pattern = r'https?://(?:www\.)?winningheaven\.com[^\s\'"<>]*'
    wrapped = re.sub(pattern, link_replacer, content, flags=re.IGNORECASE)

    # 2. Replace dynamic button & CTA placeholders
    placeholders = [
        "{track_link}", "{{track_link}}",
        "{cta_link}", "{{cta_link}}",
        "{cta_url}", "{{cta_url}}",
        "{button_link}", "{{button_link}}",
        "{click_url}", "{{click_url}}"
    ]
    for ph in placeholders:
        wrapped = wrapped.replace(ph, default_track_link)

    # 3. Replace {email} placeholders
    wrapped = wrapped.replace("{email}", clean_email).replace("{{email}}", clean_email)
    return wrapped

class EmailMarketingManager:
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.stop_requested = False
        self.worker_thread = None
        self.current_email = ""
        self.current_subject = ""
        self.current_html = ""
        self.current_plain = ""
        self.preferred_sender_account_id = None
        self.lock = threading.Lock()
        
        init_db()
        cfg = load_config()
        self.active_file = cfg.get("excel_file", "client sheet.xlsx")
        self.file_queue = cfg.get("file_queue", [])
        load_file_recipients(self.active_file)

    def set_active_file(self, file_name):
        with self.lock:
            if self.is_running:
                return False, "Cannot switch files while a campaign is running. Please pause or stop first."
            self.active_file = file_name
            cfg = load_config()
            cfg["excel_file"] = file_name
            save_config(cfg)
            
            total, added = load_file_recipients(file_name)
            log_event(f"Switched active lead file to '{file_name}' ({total} total leads).")
            return True, f"Active file set to {file_name} ({total} leads)."

    def set_file_queue(self, queue_list):
        with self.lock:
            clean_queue = [f for f in queue_list if isinstance(f, str) and f.strip()]
            self.file_queue = clean_queue
            cfg = load_config()
            cfg["file_queue"] = self.file_queue
            save_config(cfg)
            q_str = " ➔ ".join(self.file_queue) if self.file_queue else "None"
            log_event(f"📋 Campaign Queue updated: {q_str}")
            return True, f"Queue set with {len(self.file_queue)} file(s)."

    def delete_file(self, file_name):
        with self.lock:
            if self.is_running and self.active_file == file_name:
                return False, f"Cannot delete '{file_name}' while a campaign is actively running. Please stop the campaign first."

            # Remove from DB
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipients WHERE file_name = ?", (file_name,))
            conn.commit()
            conn.close()

            # Remove from disk
            p1 = os.path.join(BASE_DIR, file_name)
            p2 = os.path.join(UPLOADS_DIR, file_name)
            for p in [p1, p2]:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception as e:
                        log_event(f"Error removing file from disk: {str(e)}", level="WARNING")

            # Remove from queue
            if file_name in self.file_queue:
                self.file_queue = [f for f in self.file_queue if f != file_name]

            # If active file was deleted, switch to next available
            if self.active_file == file_name:
                available = get_available_lead_files()
                remaining = [f["name"] for f in available if f["name"] != file_name]
                if remaining:
                    self.active_file = remaining[0]
                    load_file_recipients(self.active_file)
                else:
                    self.active_file = ""

            cfg = load_config()
            cfg["excel_file"] = self.active_file
            cfg["file_queue"] = self.file_queue
            save_config(cfg)

            log_event(f"🗑️ Deleted lead list '{file_name}'. Active list is now '{self.active_file}'.")
            return True, f"Lead list '{file_name}' deleted successfully."

    def get_stats(self):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ?", (self.active_file,))
        total = cursor.fetchone()[0]
        
        if total == 0:
            available = get_available_lead_files()
            if available:
                for af in available:
                    if af["total"] > 0:
                        self.active_file = af["name"]
                        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ?", (self.active_file,))
                        total = cursor.fetchone()[0]
                        cfg = load_config()
                        cfg["excel_file"] = self.active_file
                        save_config(cfg)
                        break
        
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'sent'", (self.active_file,))
        sent = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'failed'", (self.active_file,))
        failed = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE file_name = ? AND status = 'pending'", (self.active_file,))
        pending = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*), COALESCE(SUM(click_count), 0) FROM clicks")
        click_row = cursor.fetchone()
        unique_clicks = click_row[0] if click_row else 0
        total_clicks = click_row[1] if click_row else 0

        today_str = time.strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM recipients WHERE status = 'sent' AND sent_at LIKE ?", (f"{today_str}%",))
        today_sent = cursor.fetchone()[0]
        
        conn.close()

        accounts = get_sender_accounts()
        enabled_accounts = [a for a in accounts if a.get("enabled")]
        cfg = load_config()
        global_daily_limit = int(cfg.get("daily_limit", 850))
        
        active_account = None
        for a in enabled_accounts:
            if a["sent_today"] < a["daily_limit"]:
                active_account = a["sender_email"]
                break
        if not active_account and enabled_accounts:
            active_account = enabled_accounts[0]["sender_email"]

        return {
            "active_file": self.active_file,
            "file_queue": self.file_queue,
            "total": total,
            "sent": sent,
            "failed": failed,
            "pending": pending,
            "today_sent": today_sent,
            "daily_limit": global_daily_limit,
            "daily_remaining": max(0, global_daily_limit - today_sent),
            "unique_clicks": unique_clicks,
            "total_clicks": total_clicks,
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "current_email": self.current_email,
            "accounts_count": len(accounts),
            "enabled_accounts_count": len(enabled_accounts),
            "active_sender_email": active_account or "No Active Account"
        }

    def get_clicks_data(self, search=None, limit=100, offset=0):
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT id, email, click_count, first_clicked_at, last_clicked_at, ip_address FROM clicks WHERE 1=1"
        params = []
        if search:
            query += " AND email LIKE ?"
            params.append(f"%{search}%")
        query += " ORDER BY click_count DESC, last_clicked_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query, tuple(params))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_logs(self, limit=60):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, level, message, recipient FROM logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_recipients(self, file_name=None, status=None, search=None, limit=100, offset=0):
        fname = file_name or self.active_file
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT id, file_name, email, status, sent_at, error_msg, sender_email FROM recipients WHERE file_name = ?"
        params = [fname]
        if status and status != "all":
            query += " AND status = ?"
            params.append(status)
        if search:
            query += " AND email LIKE ?"
            params.append(f"%{search}%")
        query += " ORDER BY id ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(query, tuple(params))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def retry_failed(self, file_name=None):
        fname = file_name or self.active_file
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE recipients SET status = 'pending', error_msg = NULL WHERE file_name = ? AND status = 'failed'", (fname,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        log_event(f"🔄 Re-queued {affected} failed emails in '{fname}' back to Pending.")
        return affected

    def reset_campaign(self, file_name=None):
        fname = file_name or self.active_file
        with self.lock:
            if self.is_running:
                self.stop_requested = True
                if self.worker_thread:
                    self.worker_thread.join(timeout=2)
            self.is_running = False
            self.is_paused = False
            self.stop_requested = False
            
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE recipients SET status = 'pending', sent_at = NULL, error_msg = NULL, attempts = 0 WHERE file_name = ?", (fname,))
            conn.commit()
            conn.close()
            log_event(f"Campaign reset for '{fname}'. All leads marked as Pending.")

    def test_send_single(self, to_email, subject, html_body, plain_body, sender_name=None, account_id=None):
        accounts = get_sender_accounts()
        target_acc = None
        if account_id:
            for acc in accounts:
                if acc["id"] == int(account_id):
                    target_acc = acc
                    break
        if not target_acc and accounts:
            target_acc = accounts[0]
            
        if not target_acc:
            cfg = load_config()
            target_acc = {
                "smtp_host": cfg.get("smtp_host", "smtp.hostinger.com"),
                "smtp_port": int(cfg.get("smtp_port", 465)),
                "use_ssl": cfg.get("use_ssl", True),
                "sender_email": cfg.get("sender_email", "verified@winningheaven.com"),
                "sender_password": cfg.get("sender_password", ""),
                "sender_name": sender_name or cfg.get("sender_name", "Winning Heaven VIP"),
                "reply_to": cfg.get("reply_to", "verified@winningheaven.com")
            }

        from_name = sender_name or target_acc.get("sender_name", "Winning Heaven VIP")
        from_addr = target_acc.get("sender_email")
        reply_to = target_acc.get("reply_to") or from_addr
        
        cfg = load_config()
        tracking_url = cfg.get("tracking_base_url", "")
        target_url = cfg.get("target_url", "https://winningheaven.com")
        
        # Apply Spintax rotation & tracking link wrapping
        final_subject = process_spintax(subject)
        final_html = process_spintax(html_body)
        final_plain = process_spintax(plain_body)

        html_processed = wrap_tracking_links(final_html, to_email, tracking_url, target_url)
        plain_processed = wrap_tracking_links(final_plain, to_email, tracking_url, target_url)

        domain = from_addr.split("@")[-1] if "@" in from_addr else "winningheaven.com"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = str(Header(final_subject, "utf-8"))
        msg["From"] = f"{Header(from_name, 'utf-8').encode()} <{from_addr}>"
        msg["To"] = to_email
        msg["Reply-To"] = reply_to
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=domain)
        msg["MIME-Version"] = "1.0"
        
        if plain_processed:
            msg.attach(MIMEText(plain_processed, "plain", "utf-8"))
        if html_processed:
            msg.attach(MIMEText(html_processed, "html", "utf-8"))

        server = self._create_smtp_connection(target_acc)
        server.sendmail(from_addr, [to_email], msg.as_string())
        try:
            server.quit()
        except Exception:
            pass
        
        log_event(f"Test email successfully sent to {to_email} via {from_addr}", level="SUCCESS", recipient=to_email)
        return True

    def start_campaign(self, subject, html_body, plain_body, sender_name=None, file_name=None, file_queue=None, sender_account_id=None):
        with self.lock:
            if self.is_running:
                if self.is_paused:
                    self.is_paused = False
                    log_event("Campaign Resumed.")
                    return True
                return False

            if sender_account_id is not None:
                self.preferred_sender_account_id = sender_account_id

            if file_queue is not None:
                clean_queue = [f for f in file_queue if isinstance(f, str) and f.strip()]
                self.file_queue = clean_queue
                if self.file_queue and not file_name:
                    file_name = self.file_queue.pop(0)

            if file_name:
                self.active_file = file_name
                load_file_recipients(file_name)

            self.is_running = True
            self.is_paused = False
            self.stop_requested = False
            self.current_subject = subject
            self.current_html = html_body
            self.current_plain = plain_body
            
            self.worker_thread = threading.Thread(target=self._run_campaign_loop, daemon=True)
            self.worker_thread.start()
            q_info = f" (Queue remaining: {' ➔ '.join(self.file_queue)})" if self.file_queue else ""
            acc_info = f" via Account #{self.preferred_sender_account_id}" if self.preferred_sender_account_id and str(self.preferred_sender_account_id) != "auto" else " (Auto Sender Rotation)"
            log_event(f"🚀 Campaign Started on '{self.active_file}'{acc_info}!{q_info}")
            return True

    def pause_campaign(self):
        with self.lock:
            if self.is_running and not self.is_paused:
                self.is_paused = True
                log_event("⏸️ Campaign Paused by user.")
                return True
            return False

    def stop_campaign(self):
        with self.lock:
            if self.is_running:
                self.stop_requested = True
                self.is_running = False
                self.is_paused = False
                self.current_email = ""
                log_event("⏹️ Campaign Stopped by user.")
                return True
            return False

    def _create_smtp_connection(self, acc):
        host = acc.get("smtp_host", "smtp.hostinger.com")
        port = int(acc.get("smtp_port", 465))
        from_addr = acc.get("sender_email", "")
        password = acc.get("sender_password", "")
        use_ssl = bool(acc.get("use_ssl", True if port == 465 else False))
        
        if use_ssl or port == 465:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, port, context=context, timeout=25)
            server.login(from_addr, password)
            return server
        else:
            server = smtplib.SMTP(host, port, timeout=25)
            server.starttls()
            server.login(from_addr, password)
            return server

    def _run_campaign_loop(self):
        cfg = load_config()
        min_delay = float(cfg.get("min_delay_seconds", 3))
        max_delay = float(cfg.get("max_delay_seconds", 6))
        batch_size = int(cfg.get("batch_size", 50))
        batch_pause = float(cfg.get("batch_pause_seconds", 60))
        
        tracking_url = cfg.get("tracking_base_url", "")
        target_url = cfg.get("target_url", "https://winningheaven.com")
        
        server = None
        current_acc = None
        consecutive_errors = 0
        batch_counter = 0

        try:
            while not self.stop_requested:
                while self.is_paused and not self.stop_requested:
                    time.sleep(1)

                # Check global campaign daily cap set by user via top stat card
                cfg = load_config()
                global_limit = int(cfg.get("daily_limit", 850))
                
                today_str = time.strftime("%Y-%m-%d")
                conn_chk = get_db()
                c_chk = conn_chk.cursor()
                c_chk.execute("SELECT COUNT(*) FROM recipients WHERE status = 'sent' AND sent_at LIKE ?", (f"{today_str}%",))
                today_total_sent = c_chk.fetchone()[0]
                conn_chk.close()

                if today_total_sent >= global_limit:
                    log_event(f"🛑 OVERALL CAMPAIGN DAILY LIMIT REACHED ({today_total_sent}/{global_limit} emails sent today)! Campaign paused. Change global cap or resume tomorrow.", level="WARNING")
                    self.is_paused = True
                    self.current_email = ""
                    if server:
                        try:
                            server.quit()
                        except Exception:
                            pass
                        server = None
                    current_acc = None
                    break

                # Fetch available accounts & find sender with remaining capacity today
                accounts = get_sender_accounts()
                enabled_accs = [a for a in accounts if a.get("enabled")]

                active_acc = None
                if self.preferred_sender_account_id and str(self.preferred_sender_account_id) != "auto":
                    for acc in enabled_accs:
                        if str(acc["id"]) == str(self.preferred_sender_account_id) or acc["sender_email"] == str(self.preferred_sender_account_id):
                            if acc["sent_today"] < acc["daily_limit"]:
                                active_acc = acc
                            break

                if not active_acc:
                    for acc in enabled_accs:
                        if acc["sent_today"] < acc["daily_limit"]:
                            active_acc = acc
                            if self.preferred_sender_account_id and str(self.preferred_sender_account_id) != "auto":
                                log_event(f"🔄 Preferred Sender Account daily limit reached! Auto-switching to backup sender: {acc['sender_email']} ({acc['sent_today']}/{acc['daily_limit']} sent today).", level="INFO")
                            break

                if not active_acc:
                    log_event("🛑 INDIVIDUAL DAILY LIMIT REACHED FOR ALL SENDER ACCOUNTS! Campaign automatically paused to protect deliverability. Add accounts or increase limits.", level="WARNING")
                    self.is_paused = True
                    self.current_email = ""
                    if server:
                        try:
                            server.quit()
                        except Exception:
                            pass
                        server = None
                    current_acc = None
                    break

                # If switching sender accounts, close old SMTP server
                if current_acc and current_acc["sender_email"] != active_acc["sender_email"]:
                    log_event(f"🔄 ROTATING SENDER ACCOUNT: Limit reached/switched from {current_acc['sender_email']} ➔ {active_acc['sender_email']} ({active_acc['sent_today']}/{active_acc['daily_limit']} sent today).", level="INFO")
                    if server:
                        try:
                            server.quit()
                        except Exception:
                            pass
                        server = None
                
                current_acc = active_acc

                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, attempts 
                    FROM recipients 
                    WHERE file_name = ? AND status = 'pending' 
                    ORDER BY id ASC LIMIT 1
                """, (self.active_file,))
                row = cursor.fetchone()
                conn.close()

                if not row:
                    prev_file = self.active_file
                    if self.file_queue:
                        next_file = self.file_queue.pop(0)
                        self.active_file = next_file
                        load_file_recipients(next_file)
                        
                        cfg = load_config()
                        cfg["excel_file"] = next_file
                        cfg["file_queue"] = self.file_queue
                        save_config(cfg)
                        
                        log_event(f"📁 List '{prev_file}' complete! Automatically advancing to next queued file: '{next_file}' ({len(self.file_queue)} remaining in queue).", level="SUCCESS")
                        continue
                    else:
                        log_event(f"🎉 All emails in list '{prev_file}' and campaign queue processed! Campaign complete.", level="SUCCESS")
                        break

                rec_id = row["id"]
                to_email = row["email"]
                attempts = row["attempts"] + 1

                self.current_email = to_email

                if server is None:
                    try:
                        server = self._create_smtp_connection(current_acc)
                        consecutive_errors = 0
                    except Exception as e:
                        log_event(f"SMTP Connection failed for {current_acc['sender_email']}: {str(e)}. Retrying in 10s...", level="ERROR")
                        time.sleep(10)
                        consecutive_errors += 1
                        if consecutive_errors >= 4:
                            log_event(f"Multiple SMTP failures on {current_acc['sender_email']}. Skipping to next account...", level="WARNING")
                            current_acc = None
                            server = None
                        continue

                from_name = current_acc.get("sender_name", "Winning Heaven VIP")
                from_addr = current_acc["sender_email"]
                reply_to = current_acc.get("reply_to") or from_addr
                
                # Apply Dynamic Spintax rotation & tracking links per recipient
                final_subject = process_spintax(self.current_subject)
                final_html = process_spintax(self.current_html)
                final_plain = process_spintax(self.current_plain)

                html_body = wrap_tracking_links(final_html, to_email, tracking_url, target_url)
                plain_body = wrap_tracking_links(final_plain, to_email, tracking_url, target_url)

                domain = from_addr.split("@")[-1] if "@" in from_addr else "winningheaven.com"
                
                msg = MIMEMultipart("alternative")
                msg["Subject"] = str(Header(final_subject, "utf-8"))
                msg["From"] = f"{Header(from_name, 'utf-8').encode()} <{from_addr}>"
                msg["To"] = to_email
                msg["Reply-To"] = reply_to
                msg["Date"] = formatdate(localtime=True)
                msg["Message-ID"] = make_msgid(domain=domain)
                msg["MIME-Version"] = "1.0"
                
                msg.attach(MIMEText(plain_body, "plain", "utf-8"))
                msg.attach(MIMEText(html_body, "html", "utf-8"))

                now_str = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    server.sendmail(from_addr, [to_email], msg.as_string())
                    
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("""
                        UPDATE recipients 
                        SET status = 'sent', sent_at = ?, attempts = ?, error_msg = NULL, sender_email = ? 
                        WHERE id = ?
                    """, (now_str, attempts, from_addr, rec_id))
                    conn.commit()
                    conn.close()

                    batch_counter += 1
                    current_acc["sent_today"] += 1
                    
                    log_event(f"✓ Sent via [{from_addr}]: {to_email} ({current_acc['sent_today']}/{current_acc['daily_limit']} today)", level="SUCCESS", recipient=to_email)
                    consecutive_errors = 0

                    if current_acc["sent_today"] >= current_acc["daily_limit"]:
                        log_event(f"🎯 Account {from_addr} hit limit of {current_acc['daily_limit']} emails/day! Switching to next sender account...", level="INFO")
                        if server:
                            try:
                                server.quit()
                            except Exception:
                                pass
                            server = None

                except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, ssl.SSLError, socket.timeout, socket.error, TimeoutError, OSError) as net_err:
                    log_event(f"🌐 Internet / SMTP reconnecting on {from_addr} ({str(net_err)}). Auto-retrying...", level="WARNING")
                    try:
                        if server:
                            server.quit()
                    except Exception:
                        pass
                    server = None
                    time.sleep(4)
                    continue

                except Exception as send_err:
                    err_msg = str(send_err)
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("""
                        UPDATE recipients 
                        SET status = 'failed', sent_at = ?, attempts = ?, error_msg = ?, sender_email = ? 
                        WHERE id = ?
                    """, (now_str, attempts, err_msg, from_addr, rec_id))
                    conn.commit()
                    conn.close()
                    log_event(f"✗ Failed via [{from_addr}] for {to_email}: {err_msg}", level="ERROR", recipient=to_email)

                if batch_size > 0 and batch_counter >= batch_size:
                    log_event(f"🛡️ Anti-Spam Safety: Reached batch pause of {batch_size} emails. Cooling down for {int(batch_pause)}s...", level="INFO")
                    batch_counter = 0
                    try:
                        if server:
                            server.quit()
                    except Exception:
                        pass
                    server = None
                    
                    pause_steps = int(batch_pause)
                    for _ in range(pause_steps):
                        if self.stop_requested or self.is_paused:
                            break
                        time.sleep(1)
                else:
                    delay = random.uniform(min_delay, max_delay)
                    time.sleep(delay)

        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass
            with self.lock:
                self.is_running = False
                self.is_paused = False
                self.current_email = ""


manager = EmailMarketingManager()
