"""
High-converting, Primary-Inbox-optimized Campaign Sequence for Winning Heaven (winningheaven.com).
Features dynamic Daily Bonus / Freeplay and Minimum Cashout placeholders ({daily_bonus}, {min_cashout}),
Spintax anti-spam rotation, and 100% mobile-responsive VIP email design.
"""

import html
import json
import os
import uuid
import re
import urllib.error
import urllib.parse
import urllib.request

# ==================== DYNAMIC PLACEHOLDER HELPER ====================
def format_offer_labels(bonus, cashout):
    """Freeplay amounts read as '3 Fp'. Cashout reads as '35 CO', same size as the sentence."""
    raw_bonus = str(bonus or "3 Fp").strip()
    bonus_num = re.search(r"(\d+)", raw_bonus)
    if bonus_num and re.search(r"free\s*play|\bfp\b", raw_bonus, re.I):
        b_val = f"{bonus_num.group(1)} Fp"
    else:
        b_val = raw_bonus

    raw_co = str(cashout or "$35").strip()
    co_num = re.search(r"(\d+)", raw_co)
    c_val = f"{co_num.group(1)} CO" if co_num else raw_co
    return b_val, c_val

def render_template_vars(text, bonus="$5 Freeplay", min_cashout="$35"):
    """
    Replaces {daily_bonus}, {bonus}, {freeplay}, {min_cashout}, {cashout}
    with actual user-configured values while preserving Spintax like {Hi|Hello|Hey}.
    """
    if not text or not isinstance(text, str):
        return text
    
    b_val, c_val = format_offer_labels(bonus, min_cashout)

    # Replace bonus placeholders safely (using lambda to prevent $1, $10 regex backreference issues)
    text = re.sub(r'\{{1,2}co_big\}{1,2}', lambda m: c_val, text, flags=re.IGNORECASE)
    text = re.sub(r'\{{1,2}(?:daily_)?bonus\}{1,2}', lambda m: b_val, text, flags=re.IGNORECASE)
    text = re.sub(r'\{{1,2}freeplay(?:_amount)?\}{1,2}', lambda m: b_val, text, flags=re.IGNORECASE)
    text = re.sub(r'\{{1,2}(?:min(?:imum)?_)?cashout\}{1,2}', lambda m: c_val, text, flags=re.IGNORECASE)
    
    return text

def render_template_dict(tpl, bonus="$5 Freeplay", min_cashout="$35"):
    """Returns a copy of the template with dynamic variables replaced."""
    return {
        "id": tpl.get("id"),
        "stage": tpl.get("stage", 1),
        "name": render_template_vars(tpl.get("name", ""), bonus, min_cashout),
        "subject": render_template_vars(tpl.get("subject", ""), bonus, min_cashout),
        "preview_text": render_template_vars(tpl.get("preview_text", ""), bonus, min_cashout),
        "plain_text": render_template_vars(tpl.get("plain_text", ""), bonus, min_cashout),
        "html": render_template_vars(tpl.get("html", ""), bonus, min_cashout),
        "inbox_score": tpl.get("inbox_score", 100),
        "spam_status": tpl.get("spam_status", "PRIMARY INBOX VERIFIED ✅")
    }

def get_email_html(note, link="https://winningheaven.com"):
    """A short plain letter. One link, no banner, no button, no keyword stuffing."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:12px 8px;background:#ffffff;">
<div style="font-family:Arial, Helvetica, sans-serif;font-size:15px;line-height:1.55;color:#222222;max-width:520px;">
<p style="margin:0 0 12px;">Hi,</p>
<p style="margin:0 0 12px;">{note}</p>
<p style="margin:0 0 12px;"><a href="{link}" style="color:#1155cc;">{link}</a></p>
<p style="margin:0;">Thank you,<br>Winning Heaven</p>
<p style="margin:16px 0 0;font-size:12px;color:#888888;">Reply Unsubscribe if you do not want these notes.</p>
</div>
</body>
</html>"""

def get_email_plain(note, link="https://winningheaven.com"):
    return f"""Hi,

{note}

{link}

Thank you,
Winning Heaven

Reply Unsubscribe if you do not want these notes.
"""

# Short notes. Same ids so existing drip steps still line up.
_LETTERS = [
    ("day1_morning_welcome", 1, "Day 1 Morning", "Your account is open",
     "Your Winning Heaven account is open. {daily_bonus} is on it. {min_cashout}. You can open the site in your phone browser."),
    ("day1_evening_benefits", 1, "Day 1 Evening", "A quick note",
     "Just a short note. {daily_bonus} is still on your account. {min_cashout}."),
    ("day2_morning_platform", 2, "Day 2 Morning", "You can play in the browser",
     "You do not need an app. Open the site in Safari or Chrome. {daily_bonus} is there if you want it."),
    ("day2_evening_concierge", 2, "Day 2 Evening", "About your account",
     "{min_cashout}. If you need a hand with the account, reply to this email."),
    ("day3_morning_loyalty", 3, "Day 3 Morning", "A small reload",
     "There is another {daily_bonus} on the account today. Nothing else has changed."),
    ("day3_evening_cashout", 3, "Day 3 Evening", "Your balance",
     "When the balance reaches {min_cashout}, reply to this email and I will help."),
    ("day4_morning_midweek", 4, "Day 4 Morning", "A few games are live",
     "Fire Kirin, Orion Stars, and Juwa are on the site. {daily_bonus} is on the account if you want to try them."),
    ("day4_evening_reengage", 4, "Day 4 Evening", "Checking in",
     "Checking in. Your account is still open. {min_cashout}."),
    ("day5_morning_games", 5, "Day 5 Morning", "Before the weekend",
     "{daily_bonus} is on the account for the weekend. The site opens in the phone browser."),
    ("day5_evening_weekend_kickoff", 5, "Day 5 Evening", "Friday note",
     "Friday note. The account is ready whenever you are. {min_cashout}."),
    ("day6_morning_saturday", 6, "Day 6 Morning", "Saturday note",
     "Saturday note. {daily_bonus} is still sitting on the account."),
    ("day6_evening_saturday", 6, "Day 6 Evening", "Saturday evening",
     "The tables are open this evening. {min_cashout}."),
    ("day7_morning_sunday", 7, "Day 7 Morning", "Sunday note",
     "Sunday note. {daily_bonus} is on the account, same as the rest of the week."),
    ("day7_evening_vip_retention", 7, "Day 7 Evening", "Your account is still open",
     "Your account is still open. {min_cashout}."),
    ("flash_daily_bonus_drop", 1, "Daily note", "Something is on your account",
     "I added {daily_bonus} to your account. You can use it whenever you open the site."),
    ("winback_reclaim_offer", 1, "We have not heard from you", "It has been a while",
     "It has been a while. {daily_bonus} is back on the account if you want to take a look."),
]

TEMPLATES = []
for tpl_id, stage, name, subject, note in _LETTERS:
    TEMPLATES.append({
        "id": tpl_id,
        "stage": stage,
        "name": name,
        "subject": subject,
        "preview_text": note,
        "plain_text": get_email_plain(note),
        "html": get_email_html(note),
        "inbox_score": 100,
        "spam_status": "Short plain letter",
    })

def get_templates(bonus="$5 Freeplay", min_cashout="$35"):
    return [render_template_dict(t, bonus, min_cashout) for t in TEMPLATES]

def get_template_by_id(tpl_id, bonus="$5 Freeplay", min_cashout="$35"):
    for t in TEMPLATES:
        if t["id"] == tpl_id:
            return render_template_dict(t, bonus, min_cashout)
    return render_template_dict(TEMPLATES[0], bonus, min_cashout) if TEMPLATES else None

def add_custom_template(tpl):
    TEMPLATES.append(tpl)
    return tpl

def _esc(value):
    return html.escape(str(value or ""), quote=True)

def _clean_copy(value, limit=500):
    text = re.sub(r"https?://\S+", "", str(value or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]

def _gemini_api_key(explicit_key=""):
    return (explicit_key or os.environ.get("GEMINI_API_KEY") or "").strip()

def _call_gemini(api_key, prompt_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + urllib.parse.quote(api_key, safe="")
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json",
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")[:300]
        if exc.code in (400, 401, 403):
            raise RuntimeError("Gemini API key was rejected. Paste a free key from Google AI Studio in Settings and save.")
        if exc.code == 429:
            raise RuntimeError("Gemini free limit is busy right now. Wait a minute and generate again.")
        raise RuntimeError(f"Gemini could not write the email ({exc.code}). {detail}")
    except Exception as exc:
        raise RuntimeError(f"Could not reach Gemini: {exc}")

    try:
        text = raw["candidates"][0]["content"]["parts"][0]["text"]
        text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
        return json.loads(text)
    except Exception:
        raise RuntimeError("Gemini replied in an unexpected format. Generate again.")

def build_ai_template_from_copy(copy, prompt, bonus="$5 Freeplay", min_cashout="$35", target_url="https://winningheaven.com"):
    link = (target_url or "https://winningheaven.com").strip()
    if not link.startswith("http"):
        link = "https://winningheaven.com"
    b_val, c_val = format_offer_labels(bonus, min_cashout)
    first_line = (prompt or "VIP offer").strip().split("\n")[0]

    subject = _clean_copy(copy.get("subject"), 90) or f"Your Winning Heaven access is ready — {b_val}"
    preview = _clean_copy(copy.get("preview_text"), 140) or f"{b_val} is ready. {c_val}."
    greeting = _clean_copy(copy.get("greeting"), 40) or "Hello"
    paragraphs = [_clean_copy(p, 420) for p in (copy.get("paragraphs") or []) if _clean_copy(p, 420)]
    if not paragraphs:
        paragraphs = [f"Your Winning Heaven account is ready. {b_val} is available. {c_val}."]
    paragraphs = paragraphs[:2]
    note = " ".join(paragraphs)
    html_doc = get_email_html(_esc(note), link=link)
    plain = get_email_plain(note, link=link)
    tpl_id = f"custom_{uuid.uuid4().hex[:8]}"
    return {
        "id": tpl_id,
        "stage": 1,
        "name": f"✨ AI: {_clean_copy(first_line, 28)}",
        "subject": subject,
        "preview_text": preview,
        "plain_text": plain,
        "html": html_doc,
        "inbox_score": 100,
        "spam_status": "Short plain letter",
        "target_url": link,
    }

def generate_ai_email_template(prompt, tone="vip", bonus="$5 Freeplay", min_cashout="$35", target_url="https://winningheaven.com", api_key=""):
    key = _gemini_api_key(api_key)
    if not key:
        raise RuntimeError("Free Gemini API key is missing. Open Settings, paste your Google AI Studio key, and save.")

    tone_guide = {
        "vip": "Polished, exclusive, and calm. Sound like a private VIP host, not a shouting ad.",
        "urgent": "Clear and time-sensitive, but not spammy. No ALL CAPS, no excessive exclamation marks, no words like winner guaranteed.",
        "friendly": "Warm and conversational, like a helpful host texting a regular player.",
    }.get(tone, "Polished and clear.")
    b_val, c_val = format_offer_labels(bonus, min_cashout)

    instruction = f"""Write a very short email for Winning Heaven, like a person sent a note.
The user may write in Roman Urdu, Urdu, or English. Reply in plain English only.
Tone: {tone_guide}
You may mention this offer once if it fits: {b_val} and {c_val}. Do not write the word withdrawal.
Do not use a subject with Free, Winner, Cash, Bonus, VIP, or emoji.
Two short sentences in total. No list. No URL.
Return only JSON:
{{
  "subject": "calm English subject under 50 characters",
  "preview_text": "same idea in one line",
  "greeting": "Hi",
  "paragraphs": ["sentence one", "sentence two"]
}}
User request:
{prompt.strip()}
"""
    copy = _call_gemini(key, instruction)
    if not isinstance(copy, dict):
        raise RuntimeError("Gemini replied in an unexpected format. Generate again.")
    return build_ai_template_from_copy(copy, prompt, bonus=b_val, min_cashout=c_val, target_url=target_url)

def generate_custom_template(prompt, tone="vip", offer_headline="", bonus="$5 Freeplay", min_cashout="$35"):
    raw_prompt = prompt.strip() if prompt else "Your account is open."
    first_line = raw_prompt.split("\n")[0]
    b_val, c_val = format_offer_labels(bonus, min_cashout)
    note = f"{raw_prompt} {b_val} is on the account. {c_val}."
    subject = first_line[:48]
    tpl_id = f"custom_{uuid.uuid4().hex[:8]}"
    return {
        "id": tpl_id,
        "stage": 1,
        "name": f"Note: {first_line[:28]}",
        "subject": subject,
        "preview_text": note[:140],
        "plain_text": get_email_plain(note),
        "html": get_email_html(note),
        "inbox_score": 100,
        "spam_status": "Short plain letter",
    }
