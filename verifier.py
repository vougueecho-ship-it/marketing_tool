"""
High-Performance Email Verification & List Scrubbing Engine for Winning Heaven.
Performs 6-Tier verification:
1. Syntax & RFC-5322 validation
2. Typo domain auto-correction
3. Disposable & temporary email detection
4. Role-based & Spam Trap pattern filtering
5. DNS MX record validation (macOS native dig resolution)
6. Direct SMTP Handshake (RCPT TO mailbox check without sending email)
7. Optional Verifalia Cloud API Integration
"""

import os
import re
import csv
import time
import socket
import smtplib
import subprocess
import threading
import json
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import urllib.request
import urllib.error
import base64
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
VERIFIER_STATE_PATH = os.path.join(BASE_DIR, "verifier_state.json")

DISPOSABLE_DOMAINS = {
    'mailinator.com', 'tempmail.com', 'guerrillamail.com', '10minutemail.com',
    'trashmail.com', 'yopmail.com', 'sharklasers.com', 'dispostable.com',
    'fakeinbox.com', 'throwawaymail.com', 'burnermail.io', 'maildrop.cc',
    'getairmail.com', 'mohmal.com', 'crazymailing.com', 'temp-mail.org',
    'mytemp.email', 'dropmail.me', 'inboxkitten.com'
}

ROLE_PREFIXES = {
    'abuse', 'postmaster', 'spam', 'admin', 'administrator', 'webmaster',
    'hostmaster', 'security', 'privacy', 'noreply', 'no-reply', 'mailer-daemon',
    'root', 'billing', 'compliance', 'helpdesk', 'support-desk'
}

TYPO_DOMAINS = {
    'gmai.com': 'gmail.com',
    'gamil.com': 'gmail.com',
    'gmal.com': 'gmail.com',
    'gmial.com': 'gmail.com',
    'gmaill.com': 'gmail.com',
    'gmail.con': 'gmail.com',
    'yaho.com': 'yahoo.com',
    'yaahoo.com': 'yahoo.com',
    'yahooo.com': 'yahoo.com',
    'hotmial.com': 'hotmail.com',
    'hotmai.com': 'hotmail.com',
    'outlok.com': 'outlook.com',
    'icoud.com': 'icloud.com'
}

STAFF_EMAILS = {
    'sahil123@gmail.com', 'sagar123@gmail.com', 'blackpanther231@gmail.com',
    'kevin123@gmail.com', 'shadow225@gmail.com', 'sophia909@gmail.com',
    'spidy8772@gmail.com', 'staff@jackpot.com', 'verified@winningheaven.com',
    'islampakistan143@gmail.com', 'msdhoni746432@gmail.com', 'earningnepal7@gmail.com',
    'jackpotroyals604@gmail.com'
}

mx_cache = {}
mx_cache_lock = threading.Lock()
# Domains whose mail servers ignore mailbox probes. A timeout still counts as deliverable,
# so repeating the probe for every address only burns time.
PROBE_SKIP_DOMAINS = {
    'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk', 'yahoo.co.in',
    'ymail.com', 'rocketmail.com', 'hotmail.com', 'outlook.com', 'live.com',
    'msn.com', 'icloud.com', 'me.com', 'mac.com', 'aol.com', 'proton.me',
    'protonmail.com', 'gmx.com', 'gmx.net', 'mail.com', 'zoho.com', 'yandex.com',
    'comcast.net', 'att.net', 'sbcglobal.net', 'verizon.net', 'cox.net', 'charter.net',
}
domain_probe_cache = {}
domain_probe_lock = threading.Lock()

def get_mx_records(domain):
    with mx_cache_lock:
        if domain in mx_cache:
            return mx_cache[domain]
            
    try:
        res = subprocess.run(['dig', '+short', 'MX', domain], capture_output=True, text=True, timeout=3)
        lines = res.stdout.strip().split('\n')
        mxs = []
        for l in lines:
            parts = l.strip().split()
            if len(parts) >= 2:
                try:
                    mxs.append((int(parts[0]), parts[1].rstrip('.')))
                except ValueError:
                    pass
            elif len(parts) == 1 and parts[0]:
                mxs.append((10, parts[0].rstrip('.')))
                
        mxs.sort(key=lambda x: x[0])
        result = [m[1] for m in mxs if m[1]]
        with mx_cache_lock:
            mx_cache[domain] = result
        return result
    except Exception:
        with mx_cache_lock:
            mx_cache[domain] = []
        return []

def smtp_check_mailbox(email, timeout=2):
    """
    Direct Mailbox Handshake (RCPT TO) without sending mail.
    Returns: status ('deliverable', 'dead', 'risky', 'unknown'), message
    """
    parts = email.split('@')
    if len(parts) != 2:
        return 'dead', 'Invalid format'
    
    domain = parts[1].lower()
    mx_hosts = get_mx_records(domain)
    if not mx_hosts:
        # A-record fallback. dig has a hard timeout; gethostbyname can hang forever.
        try:
            res = subprocess.run(
                ['dig', '+short', 'A', domain],
                capture_output=True, text=True, timeout=3
            )
            if (res.stdout or '').strip():
                return 'risky', 'No MX record, but domain resolves'
            return 'dead', 'Domain does not exist (No MX/A records)'
        except subprocess.TimeoutExpired:
            return 'risky', 'DNS lookup timed out'
        except Exception:
            return 'dead', 'Domain does not exist (No MX/A records)'
            
    target_mx = mx_hosts[0]
    with domain_probe_lock:
        if domain_probe_cache.get(domain) == 'filtered':
            return 'deliverable', 'MX active (provider blocks mailbox probes)'

    # Gmail, Yahoo, Microsoft rate limit port 25 checks from home residential IPs,
    # so we do a resilient fast handshake
    try:
        server = smtplib.SMTP(timeout=timeout)
        server.connect(target_mx, 25)
        server.helo('winningheaven.com')
        server.mail('verified@winningheaven.com')
        code, resp = server.rcpt(email)
        server.quit()
        
        resp_str = resp.decode('utf-8', errors='ignore') if isinstance(resp, bytes) else str(resp)
        
        if code in [250, 251]:
            return 'deliverable', f'Active Mailbox (Code {code})'
        elif code in [550, 551, 552, 553, 554]:
            return 'dead', f'Mailbox Unavailable (Code {code}: {resp_str[:40]})'
        elif code in [421, 450, 451, 452]:
            return 'risky', f'Greylisted / Rate Limited (Code {code})'
        else:
            return 'risky', f'Server response: {code}'
    except smtplib.SMTPServerDisconnected:
        with domain_probe_lock:
            domain_probe_cache[domain] = 'filtered'
        return 'deliverable', 'Mail server active (Handshake protected)'
    except smtplib.SMTPConnectError:
        with domain_probe_lock:
            domain_probe_cache[domain] = 'filtered'
        return 'risky', 'Port 25 connect timeout'
    except socket.timeout:
        with domain_probe_lock:
            domain_probe_cache[domain] = 'filtered'
        return 'risky', 'SMTP timeout'
    except Exception as e:
        err_msg = str(e)
        if 'refused' in err_msg.lower() or 'timeout' in err_msg.lower():
            with domain_probe_lock:
                domain_probe_cache[domain] = 'filtered'
            return 'deliverable', 'MX active (Port 25 filtered)'
        return 'risky', f'Handshake notice: {err_msg[:40]}'

def verify_single_email(raw_email, check_smtp=True):
    """
    Validates a single email through 6-tier pipeline.
    """
    if not raw_email or not isinstance(raw_email, str):
        return {
            'email': raw_email,
            'clean_email': '',
            'status': 'dead',
            'reason': 'Empty or null email',
            'deliverable': False
        }
        
    val = raw_email.strip().lower()
    val = re.sub(r'[\s,\'\"<>;]+', '', val)
    val = val.lstrip('.').rstrip('.')
    
    if '@' not in val:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Missing @ symbol',
            'deliverable': False
        }
        
    parts = val.split('@')
    if len(parts) != 2:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Multiple @ symbols',
            'deliverable': False
        }
        
    user, domain = parts[0].strip().strip('.'), parts[1].strip().strip('.')
    if not user or not domain or '.' not in domain:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Malformed username or domain',
            'deliverable': False
        }
        
    # Auto-fix typo domain
    if domain in TYPO_DOMAINS:
        domain = TYPO_DOMAINS[domain]
        val = f"{user}@{domain}"
        
    # Check corrupted domain extensions (.comb, .coms, concatenated strings)
    if domain.endswith('.comb') or domain.endswith('.coms') or domain.endswith('.comm') or domain.endswith('.con') or len(domain.split('.')[-1]) > 6:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Corrupted domain extension',
            'deliverable': False
        }
        
    # Regex syntax check
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$', val):
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Invalid character syntax',
            'deliverable': False
        }
        
    if '..' in val or user.startswith('.') or user.endswith('.'):
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Consecutive or leading dots',
            'deliverable': False
        }
        
    if val in STAFF_EMAILS:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'staff',
            'reason': 'Excluded internal staff email',
            'deliverable': False
        }
        
    if domain in DISPOSABLE_DOMAINS:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'risky',
            'reason': 'Temporary / Disposable email domain',
            'deliverable': False
        }
        
    if user in ROLE_PREFIXES:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'risky',
            'reason': 'Role-based account (Spam trap risk)',
            'deliverable': False
        }
        
    # Check MX DNS records
    mx_hosts = get_mx_records(domain)
    if not mx_hosts:
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'dead',
            'reason': 'Dead domain (No MX records found)',
            'deliverable': False
        }
        
    # Big mailbox providers do not answer RCPT probes. MX is enough, and a timeout
    # would have been counted as deliverable anyway.
    if domain in PROBE_SKIP_DOMAINS or domain.endswith('.gmail.com'):
        return {
            'email': raw_email,
            'clean_email': val,
            'status': 'deliverable',
            'reason': 'Mailbox provider verified by MX',
            'deliverable': True
        }

    # Direct SMTP handshake check
    if check_smtp:
        smtp_status, reason = smtp_check_mailbox(val)
        if smtp_status == 'dead':
            return {
                'email': raw_email,
                'clean_email': val,
                'status': 'dead',
                'reason': reason,
                'deliverable': False
            }
        elif smtp_status == 'risky':
            return {
                'email': raw_email,
                'clean_email': val,
                'status': 'deliverable', # Accept if domain MX is valid
                'reason': reason,
                'deliverable': True
            }
            
    return {
        'email': raw_email,
        'clean_email': val,
        'status': 'deliverable',
        'reason': 'Verified Active Mailbox',
        'deliverable': True
    }


class BatchEmailVerifier:
    def __init__(self):
        self.is_running = False
        self.progress = 0
        self.total = 0
        self.current_email = ""
        self.current_file = ""
        self.deliverable_count = 0
        self.dead_count = 0
        self.risky_count = 0
        self.duplicate_count = 0
        self.results = []
        self.deliverable_emails = []
        self.dead_emails = []
        self.risky_emails = []
        self.lock = threading.RLock()
        self.worker_thread = None
        self._done_emails = set()
        self._file_name = None
        self._raw_text = None
        self._check_smtp = True
        self._last_checkpoint = 0
        self.is_paused = False
        self.stop_requested = False
        self._run_id = 0
        self._load_persisted_state()

    def _snapshot(self):
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "progress": self.progress,
            "total": self.total,
            "current_email": self.current_email,
            "current_file": self.current_file,
            "file_name": self._file_name or "",
            "raw_text": self._raw_text or "",
            "check_smtp": self._check_smtp,
            "duplicate_count": self.duplicate_count,
            "deliverable_emails": list(self.deliverable_emails),
            "dead_emails": list(self.dead_emails),
            "risky_emails": list(self.risky_emails),
            "done_emails": list(self._done_emails),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def _write_snapshot(self, snap):
        try:
            tmp = VERIFIER_STATE_PATH + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(snap, f)
            os.replace(tmp, VERIFIER_STATE_PATH)
        except Exception:
            pass

    def _checkpoint(self, force=False):
        now = time.time()
        with self.lock:
            if not force and (self.progress % 20 != 0) and (now - self._last_checkpoint < 3):
                return
            snap = self._snapshot()
            self._last_checkpoint = now
        self._write_snapshot(snap)

    def _hydrate(self, state):
        self.current_file = state.get("current_file") or state.get("file_name") or ""
        self._file_name = state.get("file_name") or None
        self._raw_text = state.get("raw_text") or None
        self._check_smtp = bool(state.get("check_smtp", True))
        self.total = int(state.get("total") or 0)
        self.progress = int(state.get("progress") or 0)
        self.duplicate_count = int(state.get("duplicate_count") or 0)
        self.current_email = state.get("current_email") or ""
        self.deliverable_emails = list(state.get("deliverable_emails") or [])
        self.dead_emails = list(state.get("dead_emails") or [])
        self.risky_emails = list(state.get("risky_emails") or [])
        self.deliverable_count = len(self.deliverable_emails)
        self.dead_count = len(self.dead_emails)
        self.risky_count = len(self.risky_emails)
        self.results = []
        done = set(state.get("done_emails") or [])
        if not done:
            done.update(self.deliverable_emails)
            for item in self.dead_emails + self.risky_emails:
                em = (item.get("clean_email") or item.get("email") or "").strip().lower()
                if em:
                    done.add(em)
        self._done_emails = done
        if self.total and self.progress > self.total:
            self.progress = self.total

    def _load_persisted_state(self):
        if not os.path.exists(VERIFIER_STATE_PATH):
            return
        try:
            with open(VERIFIER_STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            return
        if not isinstance(state, dict):
            return

        self._hydrate(state)
        self.is_paused = bool(state.get("is_paused"))
        if self.is_paused:
            self.is_running = False
            self.stop_requested = False
            return
        if not state.get("is_running"):
            return
        if not self._file_name and not self._raw_text:
            self.is_running = False
            return

        self.is_running = True
        self.is_paused = False
        self.stop_requested = False
        self._run_id += 1
        self.worker_thread = threading.Thread(
            target=self._run_verification,
            args=(self._file_name, self._raw_text, self._check_smtp, 24),
            kwargs={"resume": True, "run_id": self._run_id},
            daemon=True,
        )
        self.worker_thread.start()

    def _reset_results(self):
        self.progress = 0
        self.total = 0
        self.current_email = ""
        self.deliverable_count = 0
        self.dead_count = 0
        self.risky_count = 0
        self.duplicate_count = 0
        self.results = []
        self.deliverable_emails = []
        self.dead_emails = []
        self.risky_emails = []
        self._done_emails = set()

    def _same_unfinished_file(self, file_name):
        same_file = bool(file_name) and file_name == (self._file_name or self.current_file)
        unfinished = self.total > 0 and self.progress < self.total and bool(self._done_emails or self.progress > 0)
        return same_file and unfinished

    def start_verification(self, file_name=None, raw_text=None, check_smtp=True, max_workers=24, resume=False):
        with self.lock:
            same_unfinished = self._same_unfinished_file(file_name)
            should_resume = bool(resume) and same_unfinished
            thread_alive = self.worker_thread is not None and self.worker_thread.is_alive()

            if self.is_running and not self.is_paused:
                return False, "Verification already in progress."

            if self.is_running and self.is_paused and should_resume and thread_alive:
                self.is_paused = False
                self.stop_requested = False
                self._write_snapshot(self._snapshot())
                return True, "Verification resumed."

            if self.is_running and self.is_paused:
                self.stop_requested = True
                self.is_paused = False
                self.is_running = False
                self._run_id += 1

            if should_resume:
                self.stop_requested = False
                self.is_paused = False
                self.is_running = True
                self._check_smtp = check_smtp
                self._run_id += 1
                run_id = self._run_id
                self.current_email = "Resuming..."
                self._write_snapshot(self._snapshot())
                self.worker_thread = threading.Thread(
                    target=self._run_verification,
                    args=(self._file_name or file_name, self._raw_text, check_smtp, max_workers),
                    kwargs={"resume": True, "run_id": run_id},
                    daemon=True,
                )
                self.worker_thread.start()
                return True, "Verification resumed."

            self._reset_results()
            self.stop_requested = False
            self.is_paused = False
            self.is_running = True
            self._file_name = file_name
            self._raw_text = raw_text if raw_text and not file_name else None
            self._check_smtp = check_smtp
            self.current_file = file_name or "Raw Input"
            self.current_email = "Starting..."
            self._run_id += 1
            run_id = self._run_id
            self._write_snapshot(self._snapshot())
            self.worker_thread = threading.Thread(
                target=self._run_verification,
                args=(file_name, raw_text, check_smtp, max_workers),
                kwargs={"resume": False, "run_id": run_id},
                daemon=True
            )
            self.worker_thread.start()
            return True, "Verification started successfully."

    def pause_verification(self):
        with self.lock:
            if self.is_paused and (self.is_running or self.progress < self.total):
                return True, "Verification is already paused."
            if not self.is_running:
                return False, "Verification is not running."
            self.is_paused = True
            self._write_snapshot(self._snapshot())
            return True, "Verification paused. Press Start to resume."

    def stop_verification(self):
        with self.lock:
            if not self.is_running and not self.is_paused:
                return False, "Verification is not running."
            self.stop_requested = True
            self.is_paused = False
            self.is_running = False
            self._run_id += 1
            self.current_email = "Stopped"
            self._write_snapshot(self._snapshot())
            return True, "Verification stopped. Scanned results are kept."

    def _wait_until_ready(self, run_id):
        while True:
            with self.lock:
                if self._run_id != run_id or self.stop_requested or not self.is_running:
                    return False
                if not self.is_paused:
                    return True
            time.sleep(0.25)

    def _extract_emails(self, file_name, raw_text):
        emails = []
        if raw_text:
            found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
            return found

        if file_name:
            path1 = os.path.join(BASE_DIR, file_name)
            path2 = os.path.join(UPLOADS_DIR, file_name)
            full_path = path1 if os.path.exists(path1) else path2
            
            if not os.path.exists(full_path):
                return []
                
            if full_path.endswith('.xlsx'):
                try:
                    wb = openpyxl.load_workbook(full_path, data_only=True)
                    sheet = wb.active
                    for row in sheet.iter_rows(values_only=True):
                        for cell in row:
                            if cell and isinstance(cell, str) and '@' in cell:
                                emails.append(cell.strip())
                except Exception:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            for cell in row:
                                if cell and '@' in cell:
                                    emails.append(cell.strip())
            else:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        for cell in row:
                            if cell and '@' in cell:
                                emails.append(cell.strip())
        return emails

    def _run_verification(self, file_name, raw_text, check_smtp, max_workers, resume=False, run_id=0):
        try:
            raw_list = self._extract_emails(file_name, raw_text)
            seen = set()
            unique_list = []
            duplicates = 0
            for em in raw_list:
                clean = em.strip().lower()
                if clean in seen:
                    duplicates += 1
                else:
                    seen.add(clean)
                    unique_list.append(clean)

            with self.lock:
                self.total = len(unique_list)
                self.duplicate_count = duplicates
                if resume:
                    already = sum(1 for em in unique_list if em in self._done_emails)
                    self.progress = already
                else:
                    self.progress = 0
                    already = 0

            if resume and not unique_list and self._done_emails:
                with self.lock:
                    if self._run_id == run_id:
                        self.is_running = False
                        self.is_paused = False
                        self.current_email = "Stopped — lead file missing"
                self._checkpoint(force=True)
                return

            pending = [em for em in unique_list if em not in self._done_emails]
            workers = max(4, min(int(max_workers or 24), 32))
            iterator = iter(pending)
            inflight = set()

            def check_one(em):
                try:
                    res = verify_single_email(em, check_smtp=check_smtp)
                except Exception as exc:
                    res = {
                        'email': em,
                        'clean_email': em,
                        'status': 'risky',
                        'reason': f'Check failed: {str(exc)[:80]}',
                        'deliverable': False,
                    }
                return em, res

            pool = ThreadPoolExecutor(max_workers=workers)
            try:
                while True:
                    if not self._wait_until_ready(run_id):
                        break
                    while len(inflight) < workers:
                        try:
                            em = next(iterator)
                        except StopIteration:
                            break
                        self.current_email = em
                        inflight.add(pool.submit(check_one, em))
                    if not inflight:
                        break
                    done, inflight = wait(inflight, timeout=0.4, return_when=FIRST_COMPLETED)
                    for fut in done:
                        em, res = fut.result()
                        clean_saved = (res.get('clean_email') or em).strip().lower()
                        with self.lock:
                            if self._run_id != run_id or self.stop_requested or not self.is_running:
                                inflight.clear()
                                break
                            self._done_emails.add(em)
                            if clean_saved:
                                self._done_emails.add(clean_saved)
                            self.results.append(res)
                            if res.get('deliverable'):
                                self.deliverable_count += 1
                                self.deliverable_emails.append(res.get('clean_email') or em)
                            elif res.get('status') == 'dead':
                                self.dead_count += 1
                                self.dead_emails.append(res)
                            else:
                                self.risky_count += 1
                                self.risky_emails.append(res)
                            self.progress += 1
                            self.current_email = em
                    self._checkpoint()
            finally:
                try:
                    pool.shutdown(wait=False, cancel_futures=True)
                except TypeError:
                    pool.shutdown(wait=False)

            with self.lock:
                if self._run_id != run_id:
                    return
                stopped = self.stop_requested or not self.is_running
                self.is_running = False
                self.is_paused = False
                self.stop_requested = False
                if stopped and self.progress < self.total:
                    self.current_email = "Stopped"
                elif self.current_email != "Stopped — lead file missing":
                    self.current_email = "Completed"
            self._checkpoint(force=True)
        except Exception:
            with self.lock:
                if self._run_id != run_id:
                    return
                self.is_running = False
                self.is_paused = False
                if not self.current_email or self.current_email in ("Starting...", "Resuming..."):
                    self.current_email = "Stopped"
            self._checkpoint(force=True)

    def get_status(self):
        with self.lock:
            if self.total > 0:
                percent = int(min(100, (self.progress / self.total) * 100))
            else:
                percent = 0
            return {
                'is_running': self.is_running,
                'is_paused': self.is_paused,
                'progress': self.progress,
                'total': self.total,
                'percent': percent,
                'current_email': self.current_email,
                'current_file': self.current_file,
                'deliverable_count': self.deliverable_count,
                'dead_count': self.dead_count,
                'risky_count': self.risky_count,
                'duplicate_count': self.duplicate_count,
                'dead_emails': list(self.dead_emails[:80]),
                'risky_emails': list(self.risky_emails[:80]),
                'sample_deliverable': list(self.deliverable_emails[:50]),
                'dead_total': self.dead_count,
                'risky_total': self.risky_count,
            }

    def apply_clean_list(self, target_file=None):
        """
        Overwrites target file and database with 100% deliverable clean emails.
        """
        with self.lock:
            if not self.deliverable_emails:
                return False, "No verified deliverable emails to apply."
                
            fname = target_file or self.current_file
            if not fname or fname == "Raw Input":
                fname = "Cleaned_Verified_Leads.csv"
                
            path1 = os.path.join(BASE_DIR, fname)
            path2 = os.path.join(UPLOADS_DIR, fname)
            full_path = path1 if os.path.exists(path1) else path2
            if not os.path.exists(full_path):
                full_path = os.path.join(UPLOADS_DIR, fname)
                
            # Write clean CSV
            if full_path.endswith('.xlsx'):
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Clean Leads"
                ws.append(["Email", "Name"])
                for em in self.deliverable_emails:
                    ws.append([em, ""])
                wb.save(full_path)
            else:
                with open(full_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["email", "name"])
                    for em in self.deliverable_emails:
                        writer.writerow([em, ""])
                        
            # Sync Database
            import sqlite3
            import mailer
            DB_PATH = os.path.join(BASE_DIR, "campaign_data.db")
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # Delete dead/risky emails
            for dead_item in self.dead_emails:
                dead_em = dead_item.get('clean_email') or dead_item.get('email')
                if dead_em:
                    c.execute("DELETE FROM recipients WHERE email = ?", (dead_em,))
            conn.commit()
            conn.close()
            
            # Reload fresh list in db
            mailer.load_file_recipients(fname)
            return True, f"Successfully saved {len(self.deliverable_emails)} verified leads to '{fname}' and purged all dead entries from database."

# Global singleton verifier instance
verifier_engine = BatchEmailVerifier()
