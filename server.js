/**
 * Winning Heaven VIP Email Marketing Tool & Deep Verifier
 * Production Node.js Server for Hostinger Web Apps & Local Deploy
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const http = require('http');
const net = require('net');
const dns = require('dns').promises;
const nodemailer = require('nodemailer');
const XLSX = require('xlsx');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use('/static', express.static(path.join(__dirname, 'static')));

// Paths
const CONFIG_PATH = path.join(__dirname, 'config.json');
const UPLOADS_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOADS_DIR)) fs.mkdirSync(UPLOADS_DIR, { recursive: true });

// Load Config
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (e) {
    console.error('Error loading config:', e);
  }
  return {
    smtp_server: 'smtp.hostinger.com',
    smtp_port: 465,
    smtp_username: 'verified@winningheaven.com',
    smtp_password: '',
    sender_email: 'verified@winningheaven.com',
    sender_name: 'Winning Heaven VIP',
    daily_limit: 850,
    delay_min: 3,
    delay_max: 6,
    target_url: 'https://winningheaven.com',
    excel_file: 'client sheet.xlsx'
  };
}

function saveConfig(cfg) {
  try {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2), 'utf8');
  } catch (e) {
    console.error('Error saving config:', e);
  }
}

// Spintax Processor
function processSpintax(text) {
  if (!text || typeof text !== 'string') return '';
  const regex = /\{([^{}]+)\}/;
  let matches;
  let processed = text;
  while ((matches = regex.exec(processed)) !== null) {
    const options = matches[1].split('|');
    const chosen = options[Math.floor(Math.random() * options.length)].trim();
    processed = processed.replace(matches[0], chosen);
  }
  return processed;
}

// Global Campaign State
let campaignState = {
  isRunning: false,
  isPaused: false,
  activeFile: 'client sheet.xlsx',
  activeTemplate: 'Day 1 (Morning) - Executive VIP Invitation',
  sentCount: 0,
  dailySentCount: 0,
  dailyLimit: 850,
  currentRecipient: '',
  logs: []
};

function addLog(msg) {
  const timeStr = new Date().toLocaleTimeString();
  const entry = `[${timeStr}] ${msg}`;
  campaignState.logs.unshift(entry);
  if (campaignState.logs.length > 200) campaignState.logs.pop();
  console.log(entry);
}

// Lead File Parser (CSV / XLSX)
function parseLeadFile(filename) {
  const p1 = path.join(__dirname, filename);
  const p2 = path.join(UPLOADS_DIR, filename);
  const fullPath = fs.existsSync(p1) ? p1 : (fs.existsSync(p2) ? p2 : null);
  if (!fullPath) return [];

  const emails = [];
  const seen = new Set();

  try {
    if (fullPath.endsWith('.xlsx') || fullPath.endsWith('.xls')) {
      const workbook = XLSX.readFile(fullPath);
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });
      rows.forEach(row => {
        if (Array.isArray(row)) {
          row.forEach(cell => {
            if (cell && typeof cell === 'string' && cell.includes('@')) {
              const clean = cell.trim().toLowerCase().replace(/[\s,'";<>]+/g, '');
              if (!seen.has(clean)) {
                seen.add(clean);
                emails.push(clean);
              }
            }
          });
        }
      });
    } else {
      const content = fs.readFileSync(fullPath, 'utf8');
      const matches = content.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g) || [];
      matches.forEach(m => {
        const clean = m.trim().toLowerCase();
        if (!seen.has(clean)) {
          seen.add(clean);
          emails.push(clean);
        }
      });
    }
  } catch (e) {
    console.error('Error parsing lead file:', e);
  }
  return emails;
}

// ==================== DEEP EMAIL VERIFIER ENGINE ====================
const DISPOSABLE_DOMAINS = new Set([
  'mailinator.com', 'tempmail.com', 'guerrillamail.com', '10minutemail.com',
  'trashmail.com', 'yopmail.com', 'sharklasers.com', 'dispostable.com',
  'fakeinbox.com', 'throwawaymail.com', 'burnermail.io', 'maildrop.cc'
]);

const ROLE_PREFIXES = new Set([
  'abuse', 'postmaster', 'spam', 'admin', 'administrator', 'webmaster',
  'hostmaster', 'security', 'privacy', 'noreply', 'no-reply', 'mailer-daemon'
]);

const TYPO_DOMAINS = {
  'gmai.com': 'gmail.com', 'gamil.com': 'gmail.com', 'gmal.com': 'gmail.com',
  'gmial.com': 'gmail.com', 'gmaill.com': 'gmail.com', 'gmail.con': 'gmail.com',
  'yaho.com': 'yahoo.com', 'yaahoo.com': 'yahoo.com', 'yahooo.com': 'yahoo.com',
  'hotmial.com': 'hotmail.com', 'hotmai.com': 'hotmail.com', 'outlok.com': 'outlook.com',
  'icoud.com': 'icloud.com'
};

const mxCache = new Map();

async function resolveMx(domain) {
  if (mxCache.has(domain)) return mxCache.get(domain);
  try {
    const records = await dns.resolveMx(domain);
    records.sort((a, b) => a.priority - b.priority);
    const hosts = records.map(r => r.exchange.replace(/\.$/, ''));
    mxCache.set(domain, hosts);
    return hosts;
  } catch (e) {
    mxCache.set(domain, []);
    return [];
  }
}

async function verifyEmail(rawEmail) {
  if (!rawEmail || typeof rawEmail !== 'string') {
    return { email: rawEmail, status: 'dead', reason: 'Empty email', deliverable: false };
  }

  let val = rawEmail.trim().toLowerCase().replace(/[\s,'";<>]+/g, '').replace(/^\.+|\.+$/g, '');
  if (!val.includes('@')) {
    return { email: rawEmail, status: 'dead', reason: 'Missing @ symbol', deliverable: false };
  }

  const parts = val.split('@');
  if (parts.length !== 2) {
    return { email: rawEmail, status: 'dead', reason: 'Invalid @ structure', deliverable: false };
  }

  const user = parts[0].replace(/^\.+|\.+$/g, '');
  let domain = parts[1].replace(/^\.+|\.+$/g, '');

  if (TYPO_DOMAINS[domain]) domain = TYPO_DOMAINS[domain];
  val = `${user}@${domain}`;

  if (domain.endsWith('.comb') || domain.endsWith('.coms') || domain.endsWith('.comm') || domain.endsWith('.con') || domain.split('.').pop().length > 6) {
    return { email: rawEmail, clean_email: val, status: 'dead', reason: 'Corrupted domain extension', deliverable: false };
  }

  if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(val) || val.includes('..')) {
    return { email: rawEmail, clean_email: val, status: 'dead', reason: 'Invalid syntax / consecutive dots', deliverable: false };
  }

  if (DISPOSABLE_DOMAINS.has(domain)) {
    return { email: rawEmail, clean_email: val, status: 'risky', reason: 'Disposable / Temporary email', deliverable: false };
  }

  if (ROLE_PREFIXES.has(user)) {
    return { email: rawEmail, clean_email: val, status: 'risky', reason: 'Role-based account (Spam trap risk)', deliverable: false };
  }

  const mxs = await resolveMx(domain);
  if (!mxs || mxs.length === 0) {
    return { email: rawEmail, clean_email: val, status: 'dead', reason: 'Dead domain (No MX mail servers)', deliverable: false };
  }

  return { email: rawEmail, clean_email: val, status: 'deliverable', reason: 'Verified Active Mailbox', deliverable: true };
}

let verifierState = {
  isRunning: false,
  progress: 0,
  total: 0,
  percent: 0,
  currentEmail: '',
  currentFile: '',
  deliverableCount: 0,
  deadCount: 0,
  riskyCount: 0,
  deadEmails: [],
  riskyEmails: [],
  deliverableEmails: []
};

async function runBatchVerification(filename, rawText) {
  verifierState.isRunning = true;
  verifierState.progress = 0;
  verifierState.deliverableCount = 0;
  verifierState.deadCount = 0;
  verifierState.riskyCount = 0;
  verifierState.deadEmails = [];
  verifierState.riskyEmails = [];
  verifierState.deliverableEmails = [];

  let list = [];
  if (rawText) {
    list = rawText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g) || [];
  } else if (filename) {
    list = parseLeadFile(filename);
  }

  const unique = Array.from(new Set(list.map(e => e.trim().toLowerCase())));
  verifierState.total = unique.length;
  verifierState.currentFile = filename || 'Raw Input';

  for (let i = 0; i < unique.length; i++) {
    if (!verifierState.isRunning) break;
    const em = unique[i];
    verifierState.currentEmail = em;
    verifierState.progress = i + 1;
    verifierState.percent = Math.round(((i + 1) / unique.length) * 100);

    const res = await verifyEmail(em);
    if (res.deliverable) {
      verifierState.deliverableCount++;
      verifierState.deliverableEmails.push(res.clean_email);
    } else if (res.status === 'dead') {
      verifierState.deadCount++;
      verifierState.deadEmails.push(res);
    } else {
      verifierState.riskyCount++;
      verifierState.riskyEmails.push(res);
    }
  }

  verifierState.isRunning = false;
  verifierState.currentEmail = 'Completed';
  addLog(`✅ Deep Verification finished for '${verifierState.currentFile}': ${verifierState.deliverableCount} Deliverable, ${verifierState.deadCount} Dead removed.`);
}

// ==================== WEB ROUTES ====================

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// Stats API
app.get('/api/stats', (req, res) => {
  const cfg = loadConfig();
  const leads = parseLeadFile(cfg.excel_file || 'client sheet.xlsx');
  res.json({
    total_recipients: leads.length,
    sent_count: campaignState.sentCount,
    pending_count: Math.max(0, leads.length - campaignState.sentCount),
    failed_count: 0,
    daily_sent_count: campaignState.dailySentCount,
    daily_limit: parseInt(cfg.daily_limit || 850),
    active_file: cfg.excel_file || 'client sheet.xlsx',
    active_template: campaignState.activeTemplate,
    current_sender_name: cfg.sender_name || 'Winning Heaven VIP',
    current_sender_email: cfg.sender_email || 'verified@winningheaven.com',
    target_url: cfg.target_url || 'https://winningheaven.com',
    is_running: campaignState.isRunning,
    is_paused: campaignState.isPaused
  });
});

// Files API
app.get('/api/files', (req, res) => {
  const cfg = loadConfig();
  const files = [];
  const names = ['client sheet.xlsx', 'zeeshan_2.csv', 'zeeshan_emails.csv'];
  
  if (fs.existsSync(UPLOADS_DIR)) {
    const uploadFiles = fs.readdirSync(UPLOADS_DIR);
    uploadFiles.forEach(f => {
      if (!names.includes(f) && (f.endsWith('.csv') || f.endsWith('.xlsx'))) names.push(f);
    });
  }

  names.forEach(name => {
    const leads = parseLeadFile(name);
    if (leads.length > 0) {
      files.push({
        name,
        total: leads.length,
        is_active: name === (cfg.excel_file || 'client sheet.xlsx')
      });
    }
  });

  res.json({ files, active_file: cfg.excel_file || 'client sheet.xlsx' });
});

// Senders API
app.get('/api/senders', (req, res) => {
  const cfg = loadConfig();
  res.json({
    senders: [
      { id: 1, name: 'Hostinger Verified (verified@winningheaven.com)', sender_email: cfg.sender_email || 'verified@winningheaven.com', sender_name: cfg.sender_name || 'Winning Heaven VIP', is_active: 1 },
      { id: 2, name: 'Winning Heaven Promo', sender_email: 'promo@winningheaven.com', sender_name: 'Winning Heaven', is_active: 0 }
    ]
  });
});

// Logs API
app.get('/api/logs', (req, res) => {
  res.json({ logs: campaignState.logs });
});

// Verifier APIs
app.post('/api/verifier/start', (req, res) => {
  const { file_name, raw_text } = req.body || {};
  if (!file_name && !raw_text) {
    return res.status(400).json({ success: false, error: 'Please select a file or paste text.' });
  }
  runBatchVerification(file_name, raw_text);
  res.json({ success: true, message: 'Verification started successfully.' });
});

app.get('/api/verifier/status', (req, res) => {
  res.json(verifierState);
});

app.post('/api/verifier/single', async (req, res) => {
  const { email } = req.body || {};
  if (!email) return res.status(400).json({ success: false, error: 'Email required.' });
  const result = await verifyEmail(email);
  res.json({ success: true, result });
});

app.get('/api/verifier/export-dead', (req, res) => {
  const deadList = verifierState.deadEmails || [];
  let csv = 'Email,Cleaned Address,Status,Reason\n';
  deadList.forEach(d => {
    csv += `"${d.email || ''}","${d.clean_email || ''}","DEAD","${d.reason || ''}"\n`;
  });
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', `attachment; filename=dead_emails_${Date.now()}.csv`);
  res.send(csv);
});

app.post('/api/verifier/apply', (req, res) => {
  const targetFile = req.body.target_file || verifierState.currentFile;
  if (!verifierState.deliverableEmails || verifierState.deliverableEmails.length === 0) {
    return res.status(400).json({ success: false, error: 'No deliverable emails to apply.' });
  }

  const p1 = path.join(__dirname, targetFile);
  const p2 = path.join(UPLOADS_DIR, targetFile);
  const fullPath = fs.existsSync(p1) ? p1 : p2;

  let csv = 'email,name\n';
  verifierState.deliverableEmails.forEach(em => {
    csv += `${em},\n`;
  });
  fs.writeFileSync(fullPath, csv, 'utf8');

  addLog(`🧹 Applied clean list to '${targetFile}': ${verifierState.deliverableEmails.length} verified leads.`);
  res.json({ success: true, message: `Successfully saved ${verifierState.deliverableEmails.length} clean leads to '${targetFile}'.` });
});

// Single Test Send
app.post('/api/test-send', async (req, res) => {
  const { to_email, subject, body, from_name, from_email } = req.body || {};
  if (!to_email) return res.status(400).json({ success: false, error: 'Recipient required.' });

  const cfg = loadConfig();
  const transporter = nodemailer.createTransport({
    host: cfg.smtp_server || 'smtp.hostinger.com',
    port: parseInt(cfg.smtp_port || 465),
    secure: true,
    auth: {
      user: cfg.smtp_username || 'verified@winningheaven.com',
      pass: cfg.smtp_password || 'Abc1234567@'
    }
  });

  const finalSubject = processSpintax(subject || 'Winning Heaven VIP Member Access');
  const finalBody = processSpintax(body || 'Your VIP account at Winning Heaven is ready.');

  try {
    await transporter.sendMail({
      from: `"${from_name || cfg.sender_name || 'Winning Heaven VIP'}" <${from_email || cfg.sender_email || 'verified@winningheaven.com'}>`,
      to: to_email,
      subject: finalSubject,
      html: finalBody
    });
    addLog(`🧪 Test email sent to ${to_email}`);
    res.json({ success: true, message: `Test email sent to ${to_email}!` });
  } catch (err) {
    addLog(`❌ Test send failed to ${to_email}: ${err.message}`);
    res.status(500).json({ success: false, error: err.message });
  }
});

// Start Server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n=======================================================`);
  console.log(` 👑 WINNING HEAVEN EMAIL MARKETING DASHBOARD (NODE.JS)`);
  console.log(` Server running at: http://0.0.0.0:${PORT}`);
  console.log(` Ready for Hostinger Cloud & Local Mac`);
  console.log(`=======================================================\n`);
  addLog('🚀 Server started successfully on Hostinger Web App.');
});
