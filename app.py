import os
import time
import json
import csv
import re
import io
import urllib.parse
from flask import Flask, render_template, request, jsonify, Response, redirect
from werkzeug.utils import secure_filename
from mailer import (
    manager, load_config, save_config, load_file_recipients, 
    get_available_lead_files, get_db, log_event, record_click,
    get_sender_accounts, add_sender_account, update_sender_account, delete_sender_account,
    parse_emails_from_file, UPLOADS_DIR
)
from templates_data import TEMPLATES, generate_custom_template, add_custom_template
from verifier import verifier_engine, verify_single_email

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max file upload

@app.route("/")
def index():
    return render_template("index.html", v=int(time.time()))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ==================== CLICK TRACKING REDIRECT ====================
@app.route("/r")
def track_click():
    raw_email = request.args.get("e", "").strip()
    dest = request.args.get("dest", "https://winningheaven.com").strip()
    
    if raw_email:
        try:
            email = urllib.parse.unquote(raw_email).lower()
        except Exception:
            email = raw_email.lower()
        
        ip = request.headers.get("X-Forwarded-For", request.remote_addr or "")
        ua = request.headers.get("User-Agent", "")[:200]
        record_click(email, ip=ip, user_agent=ua)
    
    if not dest.startswith("http"):
        dest = "https://winningheaven.com"
        
    return redirect(dest, code=302)

@app.route("/api/track-click", methods=["GET", "POST", "OPTIONS"])
def api_track_click():
    if request.method == "OPTIONS":
        resp = Response("", status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    if request.method == "POST":
        data = request.json or request.form or {}
        email = data.get("email") or data.get("e") or ""
    else:
        email = request.args.get("e") or request.args.get("email") or request.args.get("lead") or ""
        
    email = email.strip()
    if email:
        try:
            email = urllib.parse.unquote(email).lower()
        except Exception:
            email = email.lower()
            
        ip = request.headers.get("X-Forwarded-For", request.remote_addr or "")
        ua = request.headers.get("User-Agent", "")[:200]
        count = record_click(email, ip=ip, user_agent=ua)
        resp = jsonify({"success": True, "email": email, "click_count": count})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    
    resp = jsonify({"success": False, "error": "No email provided"})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp, 400

# ==================== LEAD FILES & LISTS API ====================
@app.route("/api/files", methods=["GET"])
def list_lead_files():
    files = get_available_lead_files()
    return jsonify({"active_file": manager.active_file, "files": files})

@app.route("/api/files/select", methods=["POST"])
def select_lead_file():
    data = request.json or {}
    file_name = data.get("file_name", "").strip()
    if not file_name:
        return jsonify({"success": False, "error": "No file name provided."}), 400
        
    success, msg = manager.set_active_file(file_name)
    if success:
        return jsonify({"success": True, "message": msg, "active_file": file_name})
    else:
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/files/upload", methods=["POST"])
def upload_lead_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in request."}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file."}), 400
        
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".xlsx", ".xls", ".csv", ".txt"]:
        return jsonify({"success": False, "error": "Only .xlsx, .xls, .csv, and .txt files are supported."}), 400
        
    save_path = os.path.join(UPLOADS_DIR, filename)
    file.save(save_path)
    
    # Auto-load recipients
    total, new_count = load_file_recipients(filename)
    manager.set_active_file(filename)
    
    return jsonify({
        "success": True, 
        "message": f"File '{filename}' uploaded successfully! Found {total} valid email leads.",
        "filename": filename,
        "total": total,
        "new_count": new_count
    })

@app.route("/api/files/delete", methods=["POST"])
def delete_lead_file():
    data = request.json or {}
    file_name = data.get("file_name", "").strip()
    if not file_name:
        return jsonify({"success": False, "error": "No file name specified for deletion."}), 400

    success, msg = manager.delete_file(file_name)
    if success:
        return jsonify({"success": True, "message": msg, "active_file": manager.active_file})
    else:
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/queue", methods=["GET", "POST"])
def manage_queue():
    if request.method == "POST":
        data = request.json or {}
        queue_list = data.get("file_queue", [])
        success, msg = manager.set_file_queue(queue_list)
        return jsonify({"success": success, "message": msg, "file_queue": manager.file_queue})
    
    return jsonify({"active_file": manager.active_file, "file_queue": manager.file_queue})

# ==================== CAMPAIGN & TEMPLATES API ====================
@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(manager.get_stats())

@app.route("/api/logs", methods=["GET"])
def get_logs():
    limit = request.args.get("limit", 60, type=int)
    return jsonify(manager.get_logs(limit=limit))

@app.route("/api/recipients", methods=["GET"])
def get_recipients():
    file_name = request.args.get("file_name", manager.active_file)
    status = request.args.get("status", "all")
    search = request.args.get("search", "")
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    data = manager.get_recipients(file_name=file_name, status=status, search=search, limit=limit, offset=offset)
    return jsonify(data)

@app.route("/api/clicks", methods=["GET"])
def get_clicks():
    search = request.args.get("search", "")
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    data = manager.get_clicks_data(search=search, limit=limit, offset=offset)
    return jsonify(data)

@app.route("/api/templates", methods=["GET"])
def get_templates():
    return jsonify(TEMPLATES)

@app.route("/api/templates/generate", methods=["POST"])
def generate_template_api():
    data = request.json or {}
    prompt = data.get("prompt", "").strip()
    tone = data.get("tone", "vip").strip()
    offer_headline = data.get("offer_headline", "").strip()
    
    if not prompt:
        return jsonify({"success": False, "error": "Please type a short description of what you want your email to say."}), 400
        
    tpl = generate_custom_template(prompt, tone=tone, offer_headline=offer_headline)
    return jsonify({"success": True, "template": tpl})

@app.route("/api/templates/save", methods=["POST"])
def save_template_api():
    data = request.json or {}
    tpl = data.get("template")
    if not tpl or not tpl.get("subject") or not tpl.get("html"):
        return jsonify({"success": False, "error": "Invalid template data."}), 400
        
    saved_tpl = add_custom_template(tpl)
    log_event(f"✨ Custom AI Template Saved: '{saved_tpl['name']}'")
    return jsonify({"success": True, "message": f"Template '{saved_tpl['name']}' saved successfully!", "templates": TEMPLATES})

@app.route("/api/templates/delete", methods=["POST"])
def delete_template_api():
    global TEMPLATES
    data = request.json or {}
    template_id = data.get("template_id", "").strip()
    if not template_id:
        return jsonify({"success": False, "error": "Template ID required."}), 400
        
    if len(TEMPLATES) <= 1:
        return jsonify({"success": False, "error": "Cannot delete the last remaining template. At least one template must remain."}), 400
        
    original_len = len(TEMPLATES)
    TEMPLATES[:] = [t for t in TEMPLATES if t.get("id") != template_id]
    
    if len(TEMPLATES) < original_len:
        log_event(f"🗑️ Template Deleted: '{template_id}'")
        return jsonify({"success": True, "message": "Template deleted successfully!", "templates": TEMPLATES})
    else:
        return jsonify({"success": False, "error": "Template not found."}), 404


@app.route("/api/leads/clean", methods=["POST"])
def clean_leads_api():
    data = request.json or {}
    raw_text = data.get("raw_text", "")
    target_file = data.get("target_file", "").strip()
    mode = data.get("mode", "new") # "new" or "merge"

    if not raw_text.strip():
        return jsonify({"success": False, "error": "No text provided for cleaning."}), 400

    # Clean text & find email matches
    cleaned_text = raw_text.replace("Email is", "").replace("Email", "").replace("،", ",").replace("۔", "").replace('"', '')
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found_emails = re.findall(email_pattern, cleaned_text)
    
    raw_count = len(found_emails)
    
    # Unique emails in input (internal deduplication)
    seen_in_input = []
    seen_set = set()
    duplicates_in_input = 0
    
    for em in found_emails:
        em_lower = em.strip().lower()
        if em_lower in seen_set:
            duplicates_in_input += 1
            continue
        seen_set.add(em_lower)
        seen_in_input.append(em_lower)
        
    existing_emails = set()
    already_in_file = 0
    unique_new = []
    
    if mode == "merge" and target_file:
        file_path = os.path.join(UPLOADS_DIR, target_file)
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), target_file)
        if os.path.exists(file_path):
            try:
                existing_emails = set(parse_emails_from_file(file_path))
            except Exception as e:
                print("Error reading target file:", e)
                
        for em_lower in seen_in_input:
            if em_lower in existing_emails:
                already_in_file += 1
                continue
            unique_new.append(em_lower)
    else:
        # Mode is "new": Keep ALL internal unique clean emails
        unique_new = seen_in_input

    return jsonify({
        "success": True,
        "raw_count": raw_count,
        "input_unique_count": len(seen_in_input),
        "duplicates_in_input": duplicates_in_input,
        "already_in_target_file": already_in_file,
        "target_file_existing_count": len(existing_emails),
        "new_unique_emails": unique_new,
        "final_total_if_saved": len(existing_emails) + len(unique_new) if mode == "merge" else len(unique_new)
    })

@app.route("/api/leads/save", methods=["POST"])
def save_cleaned_leads_api():
    data = request.json or {}
    emails = data.get("emails", [])
    mode = data.get("mode", "new") # "new" or "merge"
    filename = data.get("filename", "").strip()
    target_file = data.get("target_file", "").strip()

    if not emails and mode == "new":
        return jsonify({"success": False, "error": "No email addresses to save."}), 400

    if mode == "merge":
        if not target_file:
            return jsonify({"success": False, "error": "Please select a target file to merge into."}), 400
            
        final_filename = target_file
        file_path = os.path.join(UPLOADS_DIR, final_filename)
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), final_filename)

        existing_set = set(parse_emails_from_file(file_path)) if os.path.exists(file_path) else set()

        for em in emails:
            existing_set.add(em.strip().lower())

        combined_list = sorted(list(existing_set))
        
        # Save back to disk
        save_path = os.path.join(UPLOADS_DIR, final_filename)
        if not os.path.exists(UPLOADS_DIR):
            os.makedirs(UPLOADS_DIR, exist_ok=True)

        if final_filename.endswith(".xlsx") or final_filename.endswith(".xls"):
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["email", "name"])
            for em in combined_list:
                ws.append([em, ""])
            wb.save(save_path)
            # Also sync to root if file exists in root
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), final_filename)
            if os.path.exists(root_path):
                wb.save(root_path)
        else:
            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["email", "name"])
                for em in combined_list:
                    writer.writerow([em, ""])
                
        # Clear & re-sync DB
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM recipients WHERE file_name = ?", (final_filename,))
        conn.commit()
        conn.close()
        
        total, added = load_file_recipients(final_filename)
        
        # Set as active file
        cfg = load_config()
        cfg["excel_file"] = final_filename
        save_config(cfg)
        manager.set_active_file(final_filename)

        log_event(f"🧹 Merged {len(emails)} emails into '{final_filename}'. Total unique leads now: {total}")
        
        return jsonify({
            "success": True, 
            "message": f"Successfully merged {len(emails)} new unique leads into '{final_filename}'! Total unique leads now: {total}",
            "filename": final_filename,
            "total_leads": total
        })

    else: # mode == "new"
        if not filename:
            filename = f"Cleaned_Leads_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        if not filename.endswith(".csv") and not filename.endswith(".xlsx"):
            filename += ".csv"

        filename = secure_filename(filename)
        save_path = os.path.join(UPLOADS_DIR, filename)

        unique_set = sorted(list(set([e.strip().lower() for e in emails])))
        with open(save_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "name"])
            for em in unique_set:
                writer.writerow([em, ""])

        total, added = load_file_recipients(filename)
        
        # Set active file in config
        cfg = load_config()
        cfg["excel_file"] = filename
        save_config(cfg)
        manager.set_active_file(filename)
        
        log_event(f"✨ Created new lead list '{filename}' with {total} unique leads!")
        return jsonify({
            "success": True,
            "message": f"Created new lead list '{filename}' with {total} unique leads! Set as active campaign list.",
            "filename": filename,
            "total_leads": total
        })

# ==================== EMAIL VERIFICATION & LIST SCRUBBING ====================
@app.route("/api/verifier/start", methods=["POST"])
def start_verification_api():
    data = request.json or {}
    file_name = data.get("file_name", "").strip()
    raw_text = data.get("raw_text", "").strip()
    check_smtp = bool(data.get("check_smtp", True))
    
    if not file_name and not raw_text:
        return jsonify({"success": False, "error": "Please select a file or paste emails to verify."}), 400
        
    ok, msg = verifier_engine.start_verification(file_name=file_name if file_name else None, raw_text=raw_text if raw_text else None, check_smtp=check_smtp)
    if ok:
        log_event(f"🔍 Started Deep Email Verification on '{file_name or 'Raw Input'}'")
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/api/verifier/status", methods=["GET"])
def verifier_status_api():
    status = verifier_engine.get_status()
    return jsonify(status)

@app.route("/api/verifier/apply", methods=["POST"])
def apply_clean_verification_api():
    data = request.json or {}
    target_file = data.get("target_file", "").strip()
    
    ok, msg = verifier_engine.apply_clean_list(target_file=target_file if target_file else None)
    if ok:
        log_event(f"🧹 Applied Verified Clean List: {msg}")
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/api/verifier/single", methods=["POST"])
def verify_single_email_api():
    data = request.json or {}
    email = data.get("email", "").strip()
    check_smtp = bool(data.get("check_smtp", True))
    
    if not email:
        return jsonify({"success": False, "error": "Email address is required."}), 400
        
    result = verify_single_email(email, check_smtp=check_smtp)
    return jsonify({"success": True, "result": result})

@app.route("/api/verifier/export-dead", methods=["GET"])
def export_dead_emails_api():
    status = verifier_engine.get_status()
    dead_list = status.get("dead_emails", [])
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Email", "Cleaned Address", "Status", "Reason / Failure Cause"])
    for d in dead_list:
        writer.writerow([
            d.get("email", ""),
            d.get("clean_email", ""),
            d.get("status", "dead").upper(),
            d.get("reason", "Mailbox unavailable")
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=dead_invalid_emails_{int(time.time())}.csv"}
    )

@app.route("/api/daily-limit", methods=["POST"])
def update_daily_limit():
    data = request.json or {}
    new_limit = data.get("daily_limit")
    extend_by = data.get("extend_by")
    
    cfg = load_config()
    current_limit = int(cfg.get("daily_limit", 850))
    
    if extend_by is not None:
        new_limit = current_limit + int(extend_by)
    elif new_limit is not None:
        new_limit = int(new_limit)
    else:
        return jsonify({"success": False, "error": "Please provide daily_limit or extend_by."}), 400
        
    if new_limit < 1:
        new_limit = 1
        
    cfg["daily_limit"] = new_limit
    save_config(cfg)
    log_event(f"📈 Daily limit updated to {new_limit} emails/day (Previous: {current_limit}).", level="INFO")
    return jsonify({"success": True, "daily_limit": new_limit, "message": f"Daily sending limit updated to {new_limit} emails!"})

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    if request.method == "POST":
        data = request.json or {}
        cfg = load_config()
        for k in ["smtp_host", "smtp_port", "sender_email", "sender_password", "sender_name", "reply_to", "tracking_base_url", "min_delay_seconds", "max_delay_seconds", "batch_size", "batch_pause_seconds", "daily_limit", "excel_file"]:
            if k in data:
                cfg[k] = data[k]
        save_config(cfg)
        log_event("Settings updated successfully.")
        return jsonify({"success": True, "config": cfg})
    return jsonify(load_config())

@app.route("/api/senders", methods=["GET"])
def list_sender_accounts():
    accounts = get_sender_accounts()
    return jsonify({"success": True, "accounts": accounts})

@app.route("/api/senders/add", methods=["POST"])
def create_sender_account():
    data = request.json or {}
    ok, msg = add_sender_account(data)
    if ok:
        return jsonify({"success": True, "message": msg, "accounts": get_sender_accounts()})
    else:
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/senders/update", methods=["POST"])
def edit_sender_account():
    data = request.json or {}
    account_id = data.get("account_id")
    if not account_id:
        return jsonify({"success": False, "error": "account_id is required."}), 400
    ok, msg = update_sender_account(account_id, data)
    if ok:
        return jsonify({"success": True, "message": msg, "accounts": get_sender_accounts()})
    else:
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/senders/delete", methods=["POST"])
def remove_sender_account():
    data = request.json or {}
    account_id = data.get("account_id")
    if not account_id:
        return jsonify({"success": False, "error": "account_id is required."}), 400
    ok, msg = delete_sender_account(account_id)
    if ok:
        return jsonify({"success": True, "message": msg, "accounts": get_sender_accounts()})
    else:
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/test-email", methods=["POST"])
def send_test_email():
    data = request.json or {}
    to_email = data.get("to_email", "").strip()
    subject = data.get("subject", "").strip()
    html_body = data.get("html_body", "").strip()
    plain_body = data.get("plain_body", "").strip()
    sender_name = data.get("sender_name", "Winning Heaven VIP")
    account_id = data.get("account_id")
    
    if not to_email or "@" not in to_email:
        return jsonify({"success": False, "error": "Please enter a valid recipient email address."}), 400
    if not subject:
        return jsonify({"success": False, "error": "Subject line is required."}), 400
    
    try:
        manager.test_send_single(to_email, subject, html_body, plain_body, sender_name, account_id=account_id)
        return jsonify({"success": True, "message": f"Test email sent to {to_email}! Check your inbox."})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to send test email: {str(e)}"}), 500

@app.route("/api/campaign/start", methods=["POST"])
def start_campaign():
    try:
        data = request.json or {}
        subject = data.get("subject", "").strip()
        html_body = data.get("html_body", "").strip()
        plain_body = data.get("plain_body", "").strip()
        sender_name = data.get("sender_name")
        file_name = data.get("file_name", manager.active_file)
        file_queue = data.get("file_queue")
        sender_account_id = data.get("sender_account_id") or data.get("account_id")
        
        if not subject:
            return jsonify({"success": False, "error": "Please provide an email subject."}), 400
        if not html_body and not plain_body:
            return jsonify({"success": False, "error": "Email body cannot be empty."}), 400
            
        ok = manager.start_campaign(subject, html_body, plain_body, sender_name, file_name=file_name, file_queue=file_queue, sender_account_id=sender_account_id)
        if ok:
            q_msg = f" with {len(manager.file_queue)} queued file(s)" if manager.file_queue else ""
            return jsonify({"success": True, "message": f"Campaign started successfully on list '{manager.active_file}'{q_msg}!"})
        else:
            return jsonify({"success": False, "error": "Campaign is already running or paused. Resume or stop it first."}), 400
    except Exception as e:
        log_event(f"Error starting campaign: {str(e)}", level="ERROR")
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

@app.route("/api/campaign/pause", methods=["POST"])
def pause_campaign():
    ok = manager.pause_campaign()
    return jsonify({"success": ok, "message": "Campaign paused." if ok else "Campaign not running."})

@app.route("/api/campaign/stop", methods=["POST"])
def stop_campaign():
    ok = manager.stop_campaign()
    return jsonify({"success": ok, "message": "Campaign stopped." if ok else "Campaign not running."})

@app.route("/api/campaign/reset", methods=["POST"])
def reset_campaign():
    data = request.json or {}
    file_name = data.get("file_name", manager.active_file)
    manager.reset_campaign(file_name=file_name)
    return jsonify({"success": True, "message": f"Recipients in '{file_name}' reset to pending state."})

@app.route("/api/campaign/retry-failed", methods=["POST"])
def retry_failed_campaign():
    data = request.json or {}
    file_name = data.get("file_name", manager.active_file)
    count = manager.retry_failed(file_name=file_name)
    return jsonify({"success": True, "message": f"{count} failed emails in '{file_name}' moved back to Pending queue.", "count": count})

@app.route("/api/export-report", methods=["GET"])
def export_report():
    file_name = request.args.get("file_name", manager.active_file)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_name, email, status, sent_at, error_msg FROM recipients WHERE file_name = ? ORDER BY id ASC", (file_name,))
    rows = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "File / List", "Email", "Status", "Sent At", "Error Message"])
    for r in rows:
        writer.writerow([r["id"], r["file_name"], r["email"], r["status"], r["sent_at"] or "", r["error_msg"] or ""])
    
    output.seek(0)
    clean_fn = secure_filename(file_name).replace(".", "_")
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=winningheaven_report_{clean_fn}.csv"}
    )

@app.route("/api/export-clicks", methods=["GET"])
def export_clicks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, click_count, first_clicked_at, last_clicked_at, ip_address FROM clicks ORDER BY click_count DESC")
    rows = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User Email", "Total Clicks Count", "First Click Time", "Last Click Time", "IP Address"])
    for r in rows:
        writer.writerow([r["id"], r["email"], r["click_count"], r["first_clicked_at"], r["last_clicked_at"], r["ip_address"] or ""])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=winningheaven_engaged_hot_leads.csv"}
    )

if __name__ == "__main__":
    print("\n=======================================================")
    print(" 👑 WINNING HEAVEN EMAIL MARKETING DASHBOARD")
    print(" Local Dashboard running at: http://127.0.0.1:5050")
    print(" Connected to Hostinger: verified@winningheaven.com")
    print("=======================================================\n")
    app.run(host="0.0.0.0", port=5050, debug=False)
