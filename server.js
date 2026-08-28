const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const PORT = process.env.PORT || 3000;
const FLASK_PORT = 5050;

console.log('🚀 Starting Winning Heaven Email Marketing Tool on Hostinger...');

// 1. Install python dependencies if missing
const installProc = spawn('pip3', ['install', '-r', 'requirements.txt'], {
  cwd: __dirname,
  stdio: 'inherit'
});

installProc.on('close', (code) => {
  console.log(`📦 Dependency check completed (Code: ${code}). Launching Python Flask server...`);

  // 2. Launch Python Flask App
  const pythonProc = spawn('python3', ['app.py'], {
    cwd: __dirname,
    stdio: 'inherit',
    env: { ...process.env, PORT: `${FLASK_PORT}` }
  });

  pythonProc.on('error', (err) => {
    console.error('❌ Failed to start python process:', err);
  });

  pythonProc.on('exit', (code, signal) => {
    console.log(`⚠️ Python process exited with code ${code}, signal ${signal}`);
  });
});

// 3. Node.js Reverse Proxy to route Hostinger web traffic (Port 3000/PORT) to Flask (Port 5050)
const server = http.createServer((req, res) => {
  const options = {
    hostname: '127.0.0.1',
    port: FLASK_PORT,
    path: req.url,
    method: req.method,
    headers: req.headers
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  proxyReq.on('error', (err) => {
    res.writeHead(502, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
      <div style="font-family:sans-serif; text-align:center; padding:50px; background:#0f172a; color:#fff; min-height:100vh;">
        <h1 style="color:#f59e0b;">⏳ Starting Winning Heaven Marketing Dashboard...</h1>
        <p style="color:#94a3b8;">The Python engine is initializing on the server. Please refresh in a few seconds.</p>
        <button onclick="location.reload()" style="background:#22c55e; color:#fff; border:0; padding:10px 20px; border-radius:6px; font-weight:700; cursor:pointer; margin-top:20px;">
          🔄 Refresh Dashboard
        </button>
      </div>
    `);
  });

  req.pipe(proxyReq, { end: true });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`👑 Hostinger Gateway listening on Port ${PORT} -> Forwarding to Flask (${FLASK_PORT})`);
});
