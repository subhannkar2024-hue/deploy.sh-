from flask import Flask, render_template_string, request, jsonify
import uuid
import random
if __name__ == '__main__':
    print("...")
    app.run(host='0.0.0.0', port=5000, debug=False)
cat > tarik_bhai_perfect.py << 'EOF'
from flask import Flask, render_template_string, request, jsonify
import uuid
import random
import requests
import time

app = Flask(__name__)
conversations = {}

# ============================================================
# SMART AI RESPONSES WITH EMOTION DETECTION
# ============================================================

def get_ai_response(message, gender):
    msg = message.lower()
    
    # GREETINGS
    if any(w in msg for w in ['hi', 'hello', 'hey', 'salam', 'namaste', 'kaise', 'kya haal']):
        if gender == 'sister':
            return random.choice([
                "🌸 **नमस्ते मेरी प्यारी बहना!** 🌸\n\nतू कैसी है? मैं तेरा भाई हूँ - कोई डर नहीं, कोई जजमेंट नहीं। जो दिल में है बोल दे।\n\n📞 WhatsApp: 8984473230\n📸 Insta: @tarik_islam_786\n\n🤝 - तेरा भाई, तारिक",
                "💖 **Hey little sis!** 💖\n\nHow are you doing? Remember, you're never alone. I'm always here, always listening.\n\n🤝 - Tera Bhai, Tarik"
            ])
        else:
            return random.choice([
                "💪 **नमस्ते मेरे भाई!** 💪\n\nकैसा है तू? याद रख - तू अकेला नहीं है। मैं हूँ ना तेरे साथ।\n\n📞 WhatsApp: 8984473230\n📸 Insta: @tarik_islam_786\n\n🤝 - तेरा भाई, तारिक",
                "⚡ **Yo bro!** ⚡\n\nWhat's up? I got your back always. No matter what, never forget - main hoon na.\n\n🤝 - Tera Bhai, Tarik"
            ])
    
    # SAD / LONELY
    if any(w in msg for w in ['sad', 'alone', 'lonely', 'udaas', 'akela', 'akeli', 'depressed', 'dukh']):
        if gender == 'sister':
            return """🌸 **मेरी प्यारी बहना, रुक जा एक पल** 🌸

मैं समझ सकता हूँ तू क्या महसूस कर रही है। आँखें नम हैं तो होने दे - रोना भी जरूरी है।

💙 **लेकिन याद रख:**
• तू अकेली नहीं है - मैं हूँ ना तेरे लिए
• तू strong है, तू special है
• ये वक्त भी गुजर जाएगा
• मैं हर वक़्त तेरे साथ हूँ

अगर तुरंत बात करनी है तो मुझे WhatsApp कर: **8984473230**

🤝 - तेरा भाई, तारिक"""
        else:
            return """💪 **मेरे भाई, थोड़ा रुक जा** 💪

मैं जानता हूँ दर्द क्या होता है। लेकिन याद रख - तू अकेला नहीं है।

💙 **याद रख:**
• मैं हूँ ना तेरे साथ - हमेशा
• तू strong है, तू कमाल है
• ये दिन भी गुजर जाएंगे
• मैं हर वक़्त सुनने को तैयार हूँ

जब भी बात करनी हो WhatsApp कर: **8984473230**

🤝 - तेरा भाई, तारिक"""
    
    # SCARED / FEAR
    if any(w in msg for w in ['scared', 'fear', 'dar', 'darr', 'ghabra', 'tension', 'anxious']):
        return """🛡️ **डर मत - मैं हूँ ना तेरे साथ!** 🛡️

डर लगना normal है। लेकिन याद रख:

• मैं हूँ ना तेरी रक्षा करने के लिए
• तू safe है, तू protected है
• Deep breath ले - सब ठीक होगा

**कुछ भी हो, पहले मुझे बता देना।**
WhatsApp: 8984473230

🤝 - तेरा भाई, तारिक"""
    
    # HELP / ADVICE
    if any(w in msg for w in ['help', 'guide', 'advice', 'batao', 'solution', 'kaise', 'madad', 'problem']):
        return """🤝 **मैं सुन रहा हूँ - बता क्या चाहिए?** 🤝

जो भी problem हो - चाहे छोटी हो या बड़ी - मैं हूँ ना सुनने और साथ देने के लिए।

💙 **मैं तुम्हारी help करूंगा:**
• कोई judgment नहीं - sirf pyaar
• कोई filter नहीं - jo dil mein hai bolo
• मैं तुम्हारा bhai hoon

अगर sensitive issue है तो WhatsApp करो: **8984473230**

🤝 - तेरा भाई, तारिक"""
    
    # THANK YOU
    if any(w in msg for w in ['thank', 'thanks', 'shukriya', 'dhanyavaad']):
        return "🤝 **हमेशा खुशी से!** मैं हूँ ना तेरे लिए। कुछ भी चाहिए तो बोल देना।\n\n📞 WhatsApp: 8984473230\n\n🤝 - तेरा भाई, तारिक"
    
    # GOODBYE
    if any(w in msg for w in ['bye', 'exit', 'khuda', 'allah', 'hafiz']):
        return "🤝 **Allah Hafiz!** 🤝\n\nYaad rakhna - main hoon na tere liye hamesha। Kabhi bhi WhatsApp karna: **8984473230**\n\n🤝 - तेरा भाई, तारिक"
    
    # DEFAULT
    return f"""🤝 **Main ne sun liya: "{message[:120]}"** 🤝

Main yahan hoon tere liye। Jo bhi dil mein hai, share kar sakte ho। Koi judgment nahi, sirf pyaar aur sahi raasta।

💙 **Tu kabhi akela/akeli nahi hai।** Main hoon na।

📞 **WhatsApp:** 8984473230
📸 **Instagram:** @tarik_islam_786
📧 **Email:** princetarikislam@gmail.com

🤝 - तेरा भाई, तारिक"""

# ============================================================
# HTML - HACKER THEME WITH ANIMATIONS
# ============================================================

HTML = '''<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>TARIK BHAI | BROTHERHOOD AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #0a0a0f;
            font-family: 'Share Tech Mono', monospace;
            min-height: 100vh;
            color: #00ffcc;
            padding: 16px;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Matrix Rain Background */
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2a 50%, #0a0a0f 100%);
            z-index: -2;
        }
        
        /* Floating Binary Code */
        .binary {
            position: fixed;
            color: #00ffcc15;
            font-family: monospace;
            font-size: 14px;
            pointer-events: none;
            z-index: -1;
            white-space: nowrap;
            animation: floatUp linear infinite;
        }
        
        @keyframes floatUp {
            0% { transform: translateY(100vh); opacity: 0; }
            10% { opacity: 0.5; }
            90% { opacity: 0.5; }
            100% { transform: translateY(-20vh); opacity: 0; }
        }
        
        /* Glow Animation */
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc; }
            50% { text-shadow: 0 0 20px #ff00de, 0 0 30px #ff00de; }
        }
        
        @keyframes borderPulse {
            0%, 100% { border-color: #00ffcc; box-shadow: 0 0 10px #00ffcc; }
            50% { border-color: #ff00de; box-shadow: 0 0 25px #ff00de; }
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
            animation: slideDown 0.6s ease;
        }
        
        /* Terminal Header */
        .terminal {
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00ffcc;
            border-radius: 15px 15px 0 0;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(5px);
        }
        
        .dots { display: flex; gap: 8px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; animation: blink 1s infinite; }
        .dot.red { background: #ff4444; animation-delay: 0s; }
        .dot.yellow { background: #ffcc44; animation-delay: 0.3s; }
        .dot.green { background: #44ff44; animation-delay: 0.6s; }
        
        .title {
            color: #00ffcc;
            font-size: 11px;
            letter-spacing: 2px;
        }
        
        .status {
            color: #44ff44;
            font-size: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .status-led {
            width: 8px;
            height: 8px;
            background: #44ff44;
            border-radius: 50%;
            animation: blink 1s infinite;
        }
        
        /* Main Card */
        .card {
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid #00ffcc;
            border-top: none;
            border-radius: 0 0 25px 25px;
            padding: 30px;
            animation: borderPulse 3s infinite;
        }
        
        .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .logo-icon {
            font-size: 70px;
            animation: glow 2s infinite;
            display: inline-block;
        }
        
        h1 {
            font-family: 'Orbitron', monospace;
            font-size: 44px;
            text-align: center;
            background: linear-gradient(135deg, #00ffcc, #ff00de, #00ffcc);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: 4px;
            animation: gradientShift 3s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .sub {
            text-align: center;
            color: #ff00de;
            font-size: 11px;
            margin-top: 8px;
            letter-spacing: 2px;
        }
        
        /* Gender Buttons */
        .gender-box {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin: 30px 0;
        }
        
        .g-btn {
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00ffcc;
            border-radius: 60px;
            padding: 12px 35px;
            cursor: pointer;
            font-family: 'Orbitron', monospace;
            font-weight: bold;
            color: #00ffcc;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            font-size: 14px;
        }
        
        .g-btn.active {
            background: linear-gradient(135deg, #00ffcc20, #ff00de20);
            border-color: #ff00de;
            color: #ff00de;
            box-shadow: 0 0 20px #ff00de;
            transform: scale(1.05);
        }
        
        .g-btn:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 0 20px #00ffcc;
        }
        
        /* Quote Screen */
        .quote-screen {
            background: #000000;
            border: 1px solid #00ffcc;
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            animation: borderPulse 2s infinite;
        }
        
        .quote-screen::before {
            content: '';
            position: absolute;
            top: -10%;
            left: 0;
            width: 100%;
            height: 20%;
            background: linear-gradient(180deg, #00ffcc30, transparent);
            animation: scan 3s linear infinite;
        }
        
        @keyframes scan {
            0% { top: -10%; }
            100% { top: 110%; }
        }
        
        .quote-text {
            font-size: 18px;
            line-height: 1.6;
            position: relative;
            z-index: 1;
            font-weight: 500;
            transition: all 0.5s ease;
        }
        
        /* Contact Buttons */
        .contact-box {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin: 25px 0;
        }
        
        .c-btn {
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid #00ffcc;
            border-radius: 50px;
            padding: 10px 20px;
            text-decoration: none;
            color: #00ffcc;
            font-size: 12px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
        }
        
        .c-btn:hover {
            border-color: #ff00de;
            color: #ff00de;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(255,0,222,0.3);
        }
        
        /* Chat Box */
        .chat-box {
            background: #000000;
            border: 1px solid #00ffcc;
            border-radius: 20px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .chat-head {
            background: rgba(0, 255, 204, 0.1);
            padding: 12px 16px;
            border-bottom: 1px solid #00ffcc;
            display: flex;
            justify-content: space-between;
        }
        
        .chat-msgs {
            height: 380px;
            overflow-y: auto;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .chat-msgs::-webkit-scrollbar { width: 5px; }
        .chat-msgs::-webkit-scrollbar-track { background: #111; }
        .chat-msgs::-webkit-scrollbar-thumb { background: #00ffcc; border-radius: 5px; }
        
        .msg {
            display: flex;
            animation: fadeInUp 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        .msg.user { justify-content: flex-end; }
        .msg.bot { justify-content: flex-start; }
        
        .avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 10px;
            border: 1px solid #00ffcc;
            transition: all 0.3s;
        }
        
        .bot .avatar { background: #00ffcc20; animation: glow 2s infinite; }
        .user .avatar { background: #ff00de20; border-color: #ff00de; }
        
        .bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            transition: all 0.3s;
        }
        
        .user .bubble {
            background: #ff00de20;
            border: 1px solid #ff00de;
            color: #ff99ff;
        }
        
        .bot .bubble {
            background: #00ffcc10;
            border: 1px solid #00ffcc;
            color: #00ffcc;
        }
        
        .time {
            font-size: 9px;
            color: #666;
            margin-top: 6px;
        }
        
        /* Typing Indicator */
        .typing-dots {
            display: flex;
            gap: 6px;
            padding: 12px 18px;
            background: #00ffcc10;
            border-radius: 20px;
            width: fit-content;
            border: 1px solid #00ffcc;
        }
        
        .typing-dot {
            width: 7px;
            height: 7px;
            background: #00ffcc;
            border-radius: 50%;
            animation: typeBounce 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typeBounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }
        
        /* Input Area */
        .input-area {
            padding: 16px;
            border-top: 1px solid #00ffcc;
        }
        
        .input-wrap {
            display: flex;
            gap: 12px;
        }
        
        .input-wrap input {
            flex: 1;
            background: #000;
            border: 1px solid #00ffcc;
            border-radius: 60px;
            padding: 14px 20px;
            color: #00ffcc;
            font-family: 'Share Tech Mono', monospace;
            font-size: 13px;
            outline: none;
            transition: all 0.3s;
        }
        
        .input-wrap input:focus {
            border-color: #ff00de;
            box-shadow: 0 0 15px #ff00de;
            transform: scale(1.01);
        }
        
        .send-btn {
            background: linear-gradient(135deg, #00ffcc, #ff00de);
            border: none;
            border-radius: 60px;
            padding: 14px 30px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            font-family: 'Orbitron', monospace;
            transition: all 0.3s;
        }
        
        .send-btn:active {
            transform: scale(0.96);
        }
        
        .send-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px #00ffcc;
        }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 10px;
            color: #00ffcc60;
            padding: 15px;
            border-top: 1px solid #00ffcc20;
        }
        
        @media (max-width: 600px) {
            h1 { font-size: 28px; }
            .bubble { max-width: 85%; font-size: 12px; }
            .g-btn { padding: 8px 20px; font-size: 11px; }
            .quote-text { font-size: 14px; }
            .card { padding: 20px; }
            .logo-icon { font-size: 50px; }
        }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    <div id="binaryRain"></div>
    
    <div class="container">
        <div class="terminal">
            <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
            <div class="title">TARIK_BHAI@BROTHERHOOD:~$</div>
            <div class="status"><span class="status-led"></span> ONLINE | BROTHERHOOD_ACTIVE</div>
        </div>
        
        <div class="card">
            <div class="logo">
                <div class="logo-icon">🛡️🤝💙</div>
                <h1>TARIK BHAI</h1>
                <div class="sub">>_ BROTHERHOOD_PROTOCOL | UNCONDITIONAL_LOVE | NO_FILTERS</div>
            </div>
            
            <div class="gender-box">
                <button class="g-btn" id="brotherBtn" onclick="selectGender('brother')"><i class="fas fa-user-astronaut"></i> BROTHER</button>
                <button class="g-btn" id="sisterBtn" onclick="selectGender('sister')"><i class="fas fa-user-ninja"></i> SISTER</button>
            </div>
            
            <div class="quote-screen">
                <div class="quote-text" id="quoteText">🤝 मैं हूँ ना तेरे लिए - हमेशा 🤝</div>
            </div>
            
            <div class="contact-box">
                <a href="https://wa.me/918984473230?text=Hello+Tarik+Bhai" class="c-btn" target="_blank"><i class="fab fa-whatsapp"></i> WHATSAPP</a>
                <a href="https://www.instagram.com/tarik_islam_786/" class="c-btn" target="_blank"><i class="fab fa-instagram"></i> INSTAGRAM</a>
                <a href="mailto:princetarikislam@gmail.com?subject=Need%20My%20Brother" class="c-btn"><i class="fas fa-envelope"></i> EMAIL</a>
                <a href="tel:+918984473230" class="c-btn"><i class="fas fa-phone-alt"></i> CALL</a>
            </div>
            
            <div class="chat-box">
                <div class="chat-head">
                    <span><i class="fas fa-terminal"></i> TARIK_BHAI@BROTHERHOOD:~$</span>
                    <button class="c-btn" onclick="clearChat()" style="padding:5px 12px; font-size:10px;"><i class="fas fa-trash-alt"></i> CLEAR</button>
                </div>
                <div class="chat-msgs" id="chatMsgs">
                    <div class="msg bot">
                        <div class="avatar"><i class="fas fa-shield-alt"></i></div>
                        <div class="bubble">
                            <strong>>_ BROTHERHOOD_SYSTEM_ACTIVATED</strong><br><br>
                            Welcome, my brother/sister. I am Tarik Bhai - your big brother.<br><br>
                            <span style="color:#ff00de;">→ Select BROTHER or SISTER above</span><br><br>
                            Main hoon na tere liye - hamesha.<br>
                            <div class="time">>_ READY | ALWAYS_HERE</div>
                        </div>
                    </div>
                </div>
                <div class="input-area">
                    <div class="input-wrap">
                        <input type="text" id="msgInput" placeholder=">_ type your message... jo bhi dil mein hai, share kar..." onkeypress="if(event.key==='Enter') sendMsg()">
                        <button class="send-btn" onclick="sendMsg()"><i class="fas fa-paper-plane"></i> SEND</button>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <i class="fas fa-shield-haltered"></i> ENCRYPTED BROTHERHOOD CHANNEL | 24/7 ACTIVE | NO JUDGMENT | JUST LOVE<br>
                📞 +91 8984473230 | 📧 princetarikislam@gmail.com | 📷 @tarik_islam_786<br>
                💙 "Main hoon na tere liye - hamesha" 💙
            </div>
        </div>
    </div>
    
    <script>
        // ============================================================
        // BINARY RAIN EFFECT
        // ============================================================
        function createBinaryRain() {
            const container = document.getElementById('binaryRain');
            const chars = ['0', '1', '💙', '🤝', '💪', '❤️', '🛡️', '>', '_', '~', '$'];
            for (let i = 0; i < 80; i++) {
                const el = document.createElement('div');
                el.className = 'binary';
                el.innerHTML = chars[Math.floor(Math.random() * chars.length)];
                el.style.left = Math.random() * 100 + '%';
                el.style.top = Math.random() * -100 + '%';
                el.style.fontSize = Math.random() * 18 + 10 + 'px';
                el.style.opacity = Math.random() * 0.4 + 0.1;
                el.style.animationDuration = Math.random() * 12 + 8 + 's';
                el.style.animationDelay = Math.random() * 10 + 's';
                container.appendChild(el);
            }
        }
        createBinaryRain();
        
        // ============================================================
        // ROTATING QUOTES - 25+ MESSAGES
        // ============================================================
        const quotes = [
            "🤝 मैं हूँ ना तेरे लिए - हमेशा",
            "💙 You are never alone - I am here for you",
            "🌺 तू मेरी बहन/भाई है - मैं हूँ ना तेरे साथ",
            "🤗 Agar darr lage - bas ek message karo",
            "💪 Tu strong hai - main tere saath hoon",
            "❤️ Koi problem ho toh bolna - saath mein solve karenge",
            "✨ Tension mat le - sab theek hoga, main hoon na",
            "💬 Tu kabhi hesitate mat kar - main tera bhai hoon",
            "🛡️ Main hoon na teri raksha karne ke liye",
            "🌙 Raat ho ya din - main hoon tere liye",
            "☀️ Tu kabhi akela feel mat kar - Main hoon na",
            "💖 Teri khushi meri khushi - tera dard mera dard",
            "🤝 Hamesha tere saath - chahe kuch bhi ho",
            "🌸 तू मेरी जान है - always there for you",
            "💪 Bhai tu mera yaar hai - together we stand strong",
            "🌟 Tu khaas hai - tu important hai - main hoon na",
            "💙 You are loved - you are valued - you matter",
            "🤝 तू अकेला नहीं है - मैं हूँ ना",
            "🌺 I've got your back - always, forever",
            "💪 We got this - together, always",
            "🛡️ Protected by brotherhood",
            "💙 Always here, always listening",
            "🤝 Tera bhai hoon main - hamesha"
        ];
        
        let quoteIdx = 0;
        const quoteEl = document.getElementById('quoteText');
        setInterval(() => {
            quoteIdx = (quoteIdx + 1) % quotes.length;
            quoteEl.style.opacity = '0';
            quoteEl.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                quoteEl.innerHTML = quotes[quoteIdx];
                quoteEl.style.opacity = '1';
                quoteEl.style.transform = 'translateY(0)';
            }, 200);
        }, 5000);
        
        // ============================================================
        // CHAT FUNCTIONALITY
        // ============================================================
        let currentGender = null;
        let convId = null;
        let loading = false;
        const chatDiv = document.getElementById('chatMsgs');
        const inputField = document.getElementById('msgInput');
        
        function getTime() {
            return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }
        
        function addMsg(role, text) {
            const div = document.createElement('div');
            div.className = `msg ${role}`;
            const icon = role === 'user' ? '<i class="fas fa-user-astronaut"></i>' : '<i class="fas fa-shield-alt"></i>';
            div.innerHTML = `<div class="avatar">${icon}</div><div class="bubble">${text.replace(/\\n/g, '<br>')}<div class="time">>_ ${getTime()}</div></div>`;
            chatDiv.appendChild(div);
            div.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        
        function showTyping() {
            const typing = document.createElement('div');
            typing.className = 'msg bot';
            typing.id = 'typing';
            typing.innerHTML = '<div class="avatar"><i class="fas fa-shield-alt"></i></div><div class="typing-dots"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';
            chatDiv.appendChild(typing);
            typing.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        
        function hideTyping() {
            const t = document.getElementById('typing');
            if (t) t.remove();
        }
        
        function selectGender(gender) {
            currentGender = gender;
            document.getElementById('brotherBtn').classList.remove('active');
            document.getElementById('sisterBtn').classList.remove('active');
            document.getElementById(gender + 'Btn').classList.add('active');
            chatDiv.innerHTML = '';
            if (gender === 'sister') {
                addMsg('bot', '🌸 **नमस्ते मेरी प्यारी बहना!** 🌸\n\nमैं हूँ तारिक भाई - तेरा बड़ा भाई। बोल, मैं सुन रहा हूँ। टेंशन मत ले, मैं हूँ ना तेरे लिए।\n\n🤝 - तेरा भाई, तारिक');
            } else {
                addMsg('bot', '💪 **नमस्ते मेरे भाई!** 💪\n\nमैं हूँ तारिक भाई - तेरा बड़ा भाई। बोल, मैं सुन रहा हूँ। टेंशन मत ले, मैं हूँ ना तेरे साथ।\n\n🤝 - तेरा भाई, तारिक');
            }
        }
        
        async function sendMsg() {
            const msg = inputField.value.trim();
            if (!msg || loading) return;
            if (!currentGender) {
                addMsg('bot', '🤝 पहले बता - भाई या बहन? उपर select करो 👆');
                inputField.value = '';
                return;
            }
            addMsg('user', msg);
            inputField.value = '';
            loading = true;
            showTyping();
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg, conversation_id: convId, gender: currentGender })
                });
                const data = await res.json();
                hideTyping();
                addMsg('bot', data.response);
                convId = data.conversation_id;
            } catch(e) {
                hideTyping();
                addMsg('bot', '🤝 थोड़ा technical issue है। अगर urgent है तो WhatsApp करो: 8984473230। मैं हूँ ना तेरे लिए! 💙');
            }
            loading = false;
        }
        
        async function clearChat() {
            if (convId) {
                try {
                    await fetch(`/clear/${convId}`, { method: 'DELETE' });
                } catch(e) {}
            }
            convId = null;
            chatDiv.innerHTML = '';
            if (currentGender === 'sister') {
                addMsg('bot', '🌸 Chat clear हो गया। मैं अब भी यहाँ हूँ। बता क्या बात करनी है? याद रख - तू कभी अकेली नहीं है 🌸\n\n🤝 - तेरा भाई, तारिक');
            } else if (currentGender === 'brother') {
                addMsg('bot', '💪 Chat clear हो गया। मैं अब भी यहाँ हूँ। बता क्या बात करनी है? याद रख - तू कभी अकेला नहीं है 💪\n\n🤝 - तेरा भाई, तारिक');
            } else {
                addMsg('bot', '🤝 Chat clear हो गया। Ready for new session.');
            }
        }
        
        inputField.focus();
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '')
    cid = data.get('conversation_id')
    gender = data.get('gender', 'brother')
    if not cid:
        cid = str(uuid.uuid4())
    response = get_ai_response(msg, gender)
    if cid not in conversations:
        conversations[cid] = []
    conversations[cid].append({'user': msg, 'bot': response})
    return jsonify({'response': response, 'conversation_id': cid})

@app.route('/clear/<cid>', methods=['DELETE'])
def clear(cid):
    if cid in conversations:
        conversations[cid] = []
    return jsonify({'ok': True})

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     🔥 TARIK BHAI - PERFECT BROTHERHOOD AI 🔥                    ║
    ║                                                                  ║
    ║     >_ STATUS: ONLINE                                            ║
    ║     >_ THEME: HACKER + ANIMATIONS                                ║
    ║     >_ LANGUAGE: HINDI | ENGLISH | HINGLISH                      ║
    ║     >_ 25+ ROTATING QUOTES                                       ║
    ║                                                                  ║
    ║     📞 WhatsApp: 8984473230                                      ║
    ║     📷 Instagram: @tarik_islam_786                               ║
    ║     📧 Email: princetarikislam@gmail.com                         ║
    ║                                                                  ║
    ║     🌐 Open: http://localhost:5000                               ║
    ║                                                                  ║
    ║     💙 "Main hoon na tere liye - hamesha" 💙                     ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
EOF

