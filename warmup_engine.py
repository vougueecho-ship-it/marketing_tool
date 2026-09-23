import os
import time
import random
import re
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from email.header import decode_header
import sqlite3
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campaign_data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== DATABASE INITIALIZATION ====================
def init_warmup_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warmup_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            smtp_host TEXT DEFAULT 'smtp.gmail.com',
            smtp_port INTEGER DEFAULT 465,
            imap_host TEXT DEFAULT 'imap.gmail.com',
            imap_port INTEGER DEFAULT 993,
            use_ssl INTEGER DEFAULT 1,
            status TEXT DEFAULT 'warming', -- warming, paused, mature, graduated
            warmup_days INTEGER DEFAULT 1,
            health_score INTEGER DEFAULT 15,
            daily_target INTEGER DEFAULT 5,
            sent_today INTEGER DEFAULT 0,
            received_today INTEGER DEFAULT 0,
            replied_today INTEGER DEFAULT 0,
            unspammed_today INTEGER DEFAULT 0,
            total_sent INTEGER DEFAULT 0,
            total_received INTEGER DEFAULT 0,
            total_replied INTEGER DEFAULT 0,
            total_unspammed INTEGER DEFAULT 0,
            is_graduated INTEGER DEFAULT 0,
            last_active_at TEXT,
            last_day_reset TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warmup_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            from_email TEXT,
            to_email TEXT,
            subject TEXT,
            message_id TEXT,
            in_reply_to TEXT,
            status TEXT DEFAULT 'sent', -- sent, replied
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warmup_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            from_email TEXT,
            to_email TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

init_warmup_db()

def log_warmup(action, from_email="", to_email="", details=""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO warmup_logs (timestamp, action, from_email, to_email, details)
            VALUES (?, ?, ?, ?, ?)
        """, (now_str, action, from_email, to_email, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[WARMUP LOG ERROR] {e}")

# ==================== REALISTIC HUMAN CONVERSATION TEMPLATES ====================
CONVERSATION_TOPICS = [
    {
        "subjects": [
            "Quick question regarding our project timeline",
            "Project update and next steps",
            "Notes from our earlier discussion",
            "Schedule for this week's review",
            "Reviewing the proposal draft"
        ],
        "openers": [
            "Hi there,\n\nI was just reviewing our project schedule and wanted to double-check if the proposed timeline works for your team?",
            "Hello,\n\nHope your week is going smoothly! Just following up on the documents we talked about earlier.",
            "Hi,\n\nCould you please take a quick look at the latest updates when you get a chance? Let me know your thoughts.",
            "Hey,\n\nChecking in to see if we're still on track for the sync call later this week?",
            "Hi there,\n\nAttached are my initial thoughts on the workflow we discussed yesterday. Would love to get your feedback."
        ],
        "replies": [
            "Hi,\n\nThanks for reaching out! The timeline looks completely fine from our end. Let's proceed as planned.",
            "Hello,\n\nGot your note. Everything looks great so far. I will review the remaining details this afternoon.",
            "Hey,\n\nThanks for the update! Yes, we are definitely on track. I'll send over the confirmation shortly.",
            "Hi there,\n\nLooks good to me! Appreciate the quick turnaround on this. Have a great rest of your day.",
            "Thanks for checking in! I've gone through the notes and have no objections. Talk soon!"
        ]
    },
    {
        "subjects": [
            "Feedback on the shared design draft",
            "Regarding the contract agreement details",
            "Meeting agenda for tomorrow afternoon",
            "Checking availability for a quick sync",
            "Invoice verification and receipt"
        ],
        "openers": [
            "Hi,\n\nJust wanted to confirm if you received the updated draft? Let me know if any adjustments are needed.",
            "Hello,\n\nHope all is well. Are you free for a brief 10-minute catch-up call tomorrow around 2 PM?",
            "Hi there,\n\nThank you for sharing the details earlier. I have a minor question regarding section 3.",
            "Hey,\n\nJust wanted to make sure everything was received properly on your end. Talk soon!",
            "Hi,\n\nSending a quick check-in before the weekend to make sure we've covered all open items."
        ],
        "replies": [
            "Hi,\n\nYes, received it safely! Looks very clean and organized. Thanks for putting this together.",
            "Hello,\n\n2 PM tomorrow works perfectly for me. Looking forward to our discussion.",
            "Hey,\n\nThanks for following up. All received in good order. Talk to you soon!",
            "Hi there,\n\nEverything looks good on my end. Let's catch up tomorrow to wrap it up.",
            "Appreciate the follow-up! Everything is in place. Have a wonderful week ahead!"
        ]
    }
]

# ==================== DYNAMIC MATURITY & HEALTH SCORE CALCULATION ====================
def calculate_warmup_target_and_health(warmup_days, total_sent, total_replied, total_unspammed):
    """
    Ramping Schedule per user requirements:
    Day 1-4 (Cold): 4 to 8 emails/day (Health: 15% - 40%)
    Day 5-9 (Maturing): 10 to 16 emails/day (Health: 50% - 85%)
    Day 10-14+ (Mature 🟢 90%+): 18 to 25 emails/day (Ready for cold marketing!)
    """
    warmup_days = max(1, int(warmup_days or 1))
    if warmup_days <= 4:
        target = random.randint(4, 8)
        # Health score rises from 15% to 40%
        health = min(40, 15 + ((warmup_days - 1) * 8))
        status = "cold"
    elif warmup_days <= 9:
        target = random.randint(10, 16)
        # Health score rises from 50% to 85%
        health = min(85, 50 + ((warmup_days - 5) * 8))
        status = "maturing"
    else:
        target = random.randint(18, 25)
        # Day 10 starts at 90% (Mature 🟢) and reaches up to 100% on Day 14+
        health = min(100, 90 + ((warmup_days - 10) * 2))
        status = "mature"

    # Bonus for high reply rate & rescued spam
    if total_sent > 0:
        reply_ratio = min(1.0, total_replied / total_sent)
        health = min(100, int(health + (reply_ratio * 4)))

    return target, health, status

# ==================== WARMUP ENGINE CONTROLLER ====================
class WarmupEngine:
    def __init__(self):
        self.is_running = False
        self.worker_thread = None
        self._stop_event = threading.Event()
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if self.is_running:
                return True
            self.is_running = True
            self._stop_event.clear()
            self.worker_thread = threading.Thread(target=self._run_loop, daemon=True)
            self.worker_thread.start()
            log_warmup("ENGINE_STARTED", details="Warmup engine started background peer-to-peer worker.")
            return True

    def stop(self):
        with self.lock:
            if not self.is_running:
                return True
            self.is_running = False
            self._stop_event.set()
            log_warmup("ENGINE_STOPPED", details="Warmup engine paused by user.")
            return True

    def _check_and_reset_daily_limits(self):
        """Reset sent_today counts at midnight and update warmup_days & targets."""
        conn = get_db()
        cursor = conn.cursor()
        today_str = time.strftime("%Y-%m-%d")
        
        cursor.execute("SELECT id, warmup_days, total_sent, total_replied, total_unspammed, last_day_reset FROM warmup_accounts")
        rows = cursor.fetchall()
        for r in rows:
            acc_id = r["id"]
            last_reset = r["last_day_reset"] or ""
            if last_reset != today_str:
                new_days = (r["warmup_days"] or 1) + 1 if last_reset else (r["warmup_days"] or 1)
                new_target, new_health, new_status = calculate_warmup_target_and_health(
                    new_days, r["total_sent"] or 0, r["total_replied"] or 0, r["total_unspammed"] or 0
                )
                cursor.execute("""
                    UPDATE warmup_accounts 
                    SET sent_today = 0, received_today = 0, replied_today = 0, unspammed_today = 0,
                        warmup_days = ?, daily_target = ?, health_score = ?,
                        status = CASE WHEN status = 'graduated' THEN 'graduated' ELSE ? END,
                        last_day_reset = ?
                    WHERE id = ?
                """, (new_days, new_target, new_health, new_status, today_str, acc_id))
        conn.commit()
        conn.close()

    def _run_loop(self):
        print("[WARMUP ENGINE] Background worker loop started.")
        while self.is_running and not self._stop_event.is_set():
            try:
                self._check_and_reset_daily_limits()
                
                # 1. Check if there are active warmup accounts
                accounts = self.get_active_accounts()
                if len(accounts) < 2:
                    # Need at least 2 accounts for peer-to-peer conversation
                    time.sleep(15)
                    continue

                # 2. Pick sender account A that still has quota today
                eligible_senders = [a for a in accounts if a["sent_today"] < a["daily_target"]]
                if not eligible_senders:
                    # All accounts completed today's target! Sleep a bit
                    time.sleep(60)
                    continue

                sender = random.choice(eligible_senders)
                
                # 3. Pick receiver account B (different from sender)
                eligible_receivers = [a for a in accounts if a["id"] != sender["id"]]
                if not eligible_receivers:
                    time.sleep(15)
                    continue
                receiver = random.choice(eligible_receivers)

                # 4. Perform Peer-to-Peer Warmup Send
                success = self.send_warmup_email(sender, receiver)
                if success:
                    # 5. After short natural delay (5-15s), receiver checks IMAP, unspams, and auto-replies!
                    self._stop_event.wait(random.randint(5, 12))
                    if not self.is_running:
                        break
                    self.receive_and_reply(receiver, sender)

                # 6. Natural delay between conversations (30s to 75s) to avoid bot detection
                sleep_time = random.randint(30, 75)
                self._stop_event.wait(sleep_time)

            except Exception as e:
                print(f"[WARMUP ENGINE LOOP ERROR] {e}")
                time.sleep(20)

    def get_active_accounts(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM warmup_accounts WHERE status != 'paused' ORDER BY id ASC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def send_warmup_email(self, sender, receiver):
        """Sends an authentic-looking human conversation email from sender to receiver."""
        try:
            topic = random.choice(CONVERSATION_TOPICS)
            subject = random.choice(topic["subjects"])
            body_text = random.choice(topic["openers"])
            
            # Add unique message ID and thread tracking
            msg_id = make_msgid(domain=sender["email"].split("@")[-1])
            thread_id = f"wm_thread_{int(time.time())}_{random.randint(1000, 9999)}"

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{sender['name'] or 'Team'} <{sender['email']}>"
            msg["To"] = receiver["email"]
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = msg_id
            msg["X-Warmup-Thread"] = thread_id

            # Simple clean plain text and HTML
            part_plain = MIMEText(body_text, "plain", "utf-8")
            part_html = MIMEText(f"<div style='font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #111;'>{body_text.replace(chr(10), '<br>')}</div>", "html", "utf-8")
            msg.attach(part_plain)
            msg.attach(part_html)

            # Send via SMTP SSL
            server = smtplib.SMTP_SSL(sender["smtp_host"], sender["smtp_port"], timeout=25)
            server.login(sender["email"], sender["password"])
            server.sendmail(sender["email"], [receiver["email"]], msg.as_string())
            server.quit()

            # Record conversation and update counts
            now_str = time.strftime("%Y-%m-%d %H:%M:%S")
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO warmup_conversations (thread_id, from_email, to_email, subject, message_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, 'sent', ?)
            """, (thread_id, sender["email"], receiver["email"], subject, msg_id, now_str))

            cursor.execute("""
                UPDATE warmup_accounts 
                SET sent_today = sent_today + 1, total_sent = total_sent + 1, last_active_at = ?
                WHERE id = ?
            """, (now_str, sender["id"]))

            cursor.execute("""
                UPDATE warmup_accounts 
                SET received_today = received_today + 1, total_received = total_received + 1, last_active_at = ?
                WHERE id = ?
            """, (now_str, receiver["id"]))
            conn.commit()
            conn.close()

            log_warmup("SENT_WARMUP", sender["email"], receiver["email"], f"Subject: '{subject}' | Thread: {thread_id}")
            return True

        except Exception as e:
            err_msg = str(e)
            log_warmup("ERROR", sender["email"], receiver["email"], f"Failed to send warmup email: {err_msg}")
            return False

    def receive_and_reply(self, receiver, sender):
        """
        Receiver logs in via IMAP:
        1. Checks Spam folder — if an email from another warmup account landed in Spam, RESCUES it to INBOX!
        2. Checks INBOX, marks as read, stars it, and auto-replies to complete the 2-way conversation!
        """
        try:
            # Login to IMAP
            mail = imaplib.IMAP4_SSL(receiver["imap_host"], receiver["imap_port"])
            mail.login(receiver["email"], receiver["password"])

            # -------------------------------------------------------------
            # STEP A: SPAM RESCUE (Check Spam folder and move to Inbox)
            # -------------------------------------------------------------
            spam_folders = ['[Gmail]/Spam', 'Spam', 'Junk']
            for s_box in spam_folders:
                try:
                    res, _ = mail.select(s_box)
                    if res == 'OK':
                        # Search for emails from the sender
                        status, data = mail.search(None, f'(FROM "{sender["email"]}")')
                        if status == 'OK' and data[0]:
                            msg_ids = data[0].split()
                            for mid in msg_ids:
                                # Move email from Spam to INBOX!
                                mail.copy(mid, 'INBOX')
                                mail.store(mid, '+FLAGS', '\\Deleted')
                                mail.expunge()

                                # Update rescued count
                                conn = get_db()
                                cursor = conn.cursor()
                                cursor.execute("UPDATE warmup_accounts SET unspammed_today = unspammed_today + 1, total_unspammed = total_unspammed + 1 WHERE id = ?", (sender["id"],))
                                conn.commit()
                                conn.close()

                                log_warmup("RESCUED_FROM_SPAM", sender["email"], receiver["email"], f"🚨 Successfully rescued email from Spam folder and moved to Primary Inbox!")
                except Exception:
                    pass

            # -------------------------------------------------------------
            # STEP B: INBOX READ & AUTO-REPLY
            # -------------------------------------------------------------
            mail.select('INBOX')
            status, data = mail.search(None, f'(UNSEEN FROM "{sender["email"]}")')
            if status == 'OK' and data[0]:
                msg_ids = data[0].split()
                # Pick the latest email
                target_mid = msg_ids[-1]
                res, msg_data = mail.fetch(target_mid, '(RFC822)')
                if res == 'OK':
                    raw_email = msg_data[0][1]
                    email_msg = email.message_from_bytes(raw_email)

                    # Mark as read & flag/star
                    mail.store(target_mid, '+FLAGS', '(\\Seen \\Flagged)')

                    # Prepare Auto-Reply
                    orig_subject = email_msg.get('Subject', '')
                    orig_msg_id = email_msg.get('Message-ID', '')
                    
                    reply_subject = orig_subject if orig_subject.lower().startswith('re:') else f"Re: {orig_subject}"
                    topic = random.choice(CONVERSATION_TOPICS)
                    reply_text = random.choice(topic["replies"])

                    reply_msg = MIMEMultipart("alternative")
                    reply_msg["Subject"] = reply_subject
                    reply_msg["From"] = f"{receiver['name'] or 'Team'} <{receiver['email']}>"
                    reply_msg["To"] = sender["email"]
                    reply_msg["Date"] = formatdate(localtime=True)
                    reply_msg["Message-ID"] = make_msgid(domain=receiver["email"].split("@")[-1])
                    if orig_msg_id:
                        reply_msg["In-Reply-To"] = orig_msg_id
                        reply_msg["References"] = orig_msg_id

                    reply_msg.attach(MIMEText(reply_text, "plain", "utf-8"))
                    reply_msg.attach(MIMEText(f"<div style='font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #111;'>{reply_text.replace(chr(10), '<br>')}</div>", "html", "utf-8"))

                    # Send reply via SMTP SSL
                    reply_server = smtplib.SMTP_SSL(receiver["smtp_host"], receiver["smtp_port"], timeout=25)
                    reply_server.login(receiver["email"], receiver["password"])
                    reply_server.sendmail(receiver["email"], [sender["email"]], reply_msg.as_string())
                    reply_server.quit()

                    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
                    conn = get_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE warmup_accounts 
                        SET replied_today = replied_today + 1, total_replied = total_replied + 1, last_active_at = ?
                        WHERE id = ?
                    """, (now_str, receiver["id"]))
                    conn.commit()
                    conn.close()

                    log_warmup("AUTOREPLIED", receiver["email"], sender["email"], f"Threaded reply sent: '{reply_subject}'")

            mail.close()
            mail.logout()
            return True

        except Exception as e:
            err_msg = str(e)
            log_warmup("ERROR", receiver["email"], sender["email"], f"IMAP Auto-Reply/Rescue Error: {err_msg}")
            return False

# Global warmup engine singleton
warmup_manager = WarmupEngine()

# ==================== ACCOUNT MANAGEMENT & GRADUATION HELPERS ====================
def add_warmup_account(data):
    init_warmup_db()
    email_clean = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip() or email_clean.split("@")[0]
    
    if not email_clean or not password:
        return False, "Email and Google App Password are required."
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM warmup_accounts WHERE email = ?", (email_clean,))
    if cursor.fetchone():
        conn.close()
        return False, f"Account '{email_clean}' is already in the Warmup Pool."
    
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    today_str = time.strftime("%Y-%m-%d")
    initial_target, initial_health, initial_status = calculate_warmup_target_and_health(1, 0, 0, 0)
    
    cursor.execute("""
        INSERT INTO warmup_accounts (
            name, email, password, smtp_host, smtp_port, imap_host, imap_port, use_ssl,
            status, warmup_days, health_score, daily_target, sent_today, received_today,
            replied_today, unspammed_today, total_sent, total_received, total_replied,
            total_unspammed, is_graduated, last_active_at, last_day_reset, created_at
        ) VALUES (
            ?, ?, ?, 'smtp.gmail.com', 465, 'imap.gmail.com', 993, 1,
            ?, 1, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?, ?, ?
        )
    """, (name, email_clean, password, initial_status, initial_health, initial_target, now_str, today_str, now_str))
    conn.commit()
    conn.close()
    
    log_warmup("ACCOUNT_ADDED", email_clean, details=f"Added to Warmup Pool (Day 1 Cold, Target: {initial_target} emails/day)")
    return True, f"Account '{email_clean}' added to Warmup Pool."

def bulk_add_warmup_accounts(raw_text):
    """
    Parses pasted text in formats:
    email,password
    email:password
    email password
    """
    init_warmup_db()
    lines = [l.strip() for l in raw_text.strip().splitlines() if l.strip()]
    added = 0
    skipped = 0
    errors = []

    for line in lines:
        parts = re.split(r'[,:\s\t]+', line)
        if len(parts) >= 2:
            em = parts[0].strip().lower()
            pwd = parts[1].strip()
            if "@" in em and len(pwd) >= 6:
                ok, msg = add_warmup_account({"email": em, "password": pwd})
                if ok:
                    added += 1
                else:
                    skipped += 1
            else:
                skipped += 1
        else:
            skipped += 1

    return {
        "success": True,
        "added": added,
        "skipped": skipped,
        "message": f"Successfully imported {added} accounts! ({skipped} skipped/duplicates)"
    }

def graduate_warmup_account(acc_id):
    """
    Graduates a mature account from the Warmup Pool into active Campaign Sender Rotation!
    """
    init_warmup_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warmup_accounts WHERE id = ?", (acc_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Account not found."
    
    acc = dict(row)
    em = acc["email"]
    pwd = acc["password"]
    name = f"Gmail Mature ({em.split('@')[0]})"
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if already exists in sender_accounts
    cursor.execute("SELECT id FROM sender_accounts WHERE sender_email = ?", (em,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("""
            UPDATE sender_accounts
            SET sender_password = ?, enabled = 1, daily_limit = 80
            WHERE sender_email = ?
        """, (pwd, em))
    else:
        cursor.execute("""
            INSERT INTO sender_accounts (name, provider, smtp_host, smtp_port, use_ssl, sender_email, sender_password, sender_name, reply_to, daily_limit, enabled, created_at)
            VALUES (?, 'gmail', 'smtp.gmail.com', 465, 1, ?, ?, 'Winning Heaven VIP', ?, 80, 1, ?)
        """, (name, em, pwd, em, now_str))
        
    cursor.execute("UPDATE warmup_accounts SET is_graduated = 1, status = 'graduated' WHERE id = ?", (acc_id,))
    conn.commit()
    conn.close()
    
    log_warmup("GRADUATED", em, details="🎓 Account graduated to active Campaign Sender Rotation (80 daily cap).")
    return True, f"Account '{em}' graduated to Campaign Sender rotation!"

def toggle_warmup_account(acc_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM warmup_accounts WHERE id = ?", (acc_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Account not found."
    
    cur_status = row["status"]
    new_status = "paused" if cur_status != "paused" else "warming"
    cursor.execute("UPDATE warmup_accounts SET status = ? WHERE id = ?", (new_status, acc_id))
    conn.commit()
    conn.close()
    return True, f"Account status set to '{new_status}'."

def delete_warmup_account(acc_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM warmup_accounts WHERE id = ?", (acc_id,))
    conn.commit()
    conn.close()
    return True, "Account deleted from Warmup Pool."

def test_warmup_credentials(email_addr, password):
    """Verifies both SMTP and IMAP connection with Gmail."""
    res = {"smtp": False, "imap": False, "errors": []}
    # 1. Test SMTP
    try:
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        s.login(email_addr, password)
        s.quit()
        res["smtp"] = True
    except Exception as e:
        res["errors"].append(f"SMTP Error: {str(e)}")

    # 2. Test IMAP
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        m.login(email_addr, password)
        m.logout()
        res["imap"] = True
    except Exception as e:
        res["errors"].append(f"IMAP Error: {str(e)}")

    res["success"] = res["smtp"] and res["imap"]
    return res

def get_warmup_stats():
    init_warmup_db()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM warmup_accounts")
    total_accounts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM warmup_accounts WHERE health_score >= 90 OR status = 'mature'")
    mature_accounts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM warmup_accounts WHERE status IN ('cold', 'maturing', 'warming')")
    active_warming = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM warmup_accounts WHERE is_graduated = 1")
    graduated_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(sent_today), 0) as sent_today,
            COALESCE(SUM(received_today), 0) as received_today,
            COALESCE(SUM(replied_today), 0) as replied_today,
            COALESCE(SUM(unspammed_today), 0) as unspammed_today,
            COALESCE(AVG(health_score), 0) as avg_health
        FROM warmup_accounts
    """)
    row = cursor.fetchone()
    
    conn.close()
    return {
        "total_accounts": total_accounts,
        "mature_accounts": mature_accounts,
        "active_warming": active_warming,
        "graduated_count": graduated_count,
        "sent_today": row["sent_today"],
        "received_today": row["received_today"],
        "replied_today": row["replied_today"],
        "unspammed_today": row["unspammed_today"],
        "avg_health": round(row["avg_health"], 1),
        "is_engine_running": warmup_manager.is_running
    }

def get_all_warmup_accounts():
    init_warmup_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warmup_accounts ORDER BY health_score DESC, id ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_warmup_logs(limit=50):
    init_warmup_db()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warmup_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

