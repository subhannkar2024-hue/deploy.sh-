from flask import Flask, render_template_string, request, jsonify
import uuid
import random

app = Flask(__name__)
conversations = {}

def get_response(message, gender):
    msg = message.lower()
    
    if any(w in msg for w in ['hi', 'hello', 'hey', 'salam', 'namaste']):
        if gender == 'sister':
            return "🌸 Namaste meri pyaari behna! Main hoon Tarik Bhai. Kaise ho? Bol, main sun raha hoon. 🌸\n\n🤝 - Tera Bhai, Tarik"
        else:
            return "💪 Namaste mere bhai! Main hoon Tarik Bhai. Kaise hai tu? Bol, main sun raha hoon. 💪\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['sad', 'alone', 'lonely', 'udaas']):
        if gender == 'sister':
            return "🌸 Meri pyaari behna, tu akeli nahi hai. Main hoon na tere liye hamesha. WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
        else:
            return "💪 Mere bhai, tu akela nahi hai. Main hoon na tere saath. WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['scared', 'fear', 'dar']):
        return "🛡️ Darr mat! Main hoon na tere saath. Sab theek hoga. WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['thank', 'thanks']):
        return "🤝 Hamesha khushi se! Main hoon na tere liye.\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['bye', 'exit']):
        return "🤝 Allah Hafiz! Yaad rakhna - main hoon na tere liye hamesha. WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    return f"""🤝 Maine sun liya: "{message[:100]}..."

Main yahan hoon tere liye. Jo bhi dil mein hai, share kar sakte ho. Koi judgment nahi, sirf pyaar aur sahi raasta.

💙 Tu kabhi akela/akeli nahi hai. Main hoon na.

WhatsApp: 8984473230 | Instagram: @tarik_islam_786

🤝 - Tera Bhai, Tarik"""

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Tarik Bhai - Your Big Brother</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:linear-gradient(135deg,#0a0a0a,#1a0033);font-family:system-ui;min-height:100vh;padding:16px}
        .container{max-width:700px;margin:0 auto;height:95vh;display:flex;flex-direction:column;gap:16px}
        .header{background:rgba(0,0,0,0.5);backdrop-filter:blur(20px);border-radius:40px;padding:20px;text-align:center;border:1px solid #a855f7}
        .logo{width:70px;height:70px;background:linear-gradient(135deg,#7c3aed,#ec489a);border-radius:25px;display:flex;align-items:center;justify-content:center;font-size:36px;margin:0 auto 12px}
        h1{font-size:32px;background:linear-gradient(135deg,#fff,#a855f7,#ec489a);-webkit-background-clip:text;background-clip:text;color:transparent}
        .gender-buttons{display:flex;justify-content:center;gap:15px;margin:15px 0}
        .gender-btn{background:rgba(31,41,55,0.8);border:1px solid #a855f7;border-radius:50px;padding:8px 24px;cursor:pointer;color:white}
        .gender-btn.active{background:linear-gradient(135deg,#7c3aed,#a855f7)}
        .carousel{background:rgba(124,58,237,0.2);border-radius:60px;padding:16px;text-align:center;border:1px solid #a855f7}
        .carousel-text{font-size:15px}
        .contact-row{display:flex;justify-content:center;gap:12px;flex-wrap:wrap}
        .contact-btn{background:rgba(0,0,0,0.5);border-radius:50px;padding:8px 16px;text-decoration:none;color:white;font-size:12px;display:inline-flex;align-items:center;gap:6px;border:1px solid #a855f7}
        .chat-box{background:rgba(0,0,0,0.3);backdrop-filter:blur(20px);border-radius:30px;border:1px solid #a855f7;display:flex;flex-direction:column;overflow:hidden;flex:1}
        .chat-header{display:flex;justify-content:space-between;padding:12px 16px;background:rgba(0,0,0,0.4);border-bottom:1px solid #a855f7}
        .clear-btn{background:rgba(239,68,68,0.2);border:1px solid #ef4444;color:#f87171;padding:4px 12px;border-radius:30px;cursor:pointer}
        .messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
        .message{display:flex;animation:fadeIn 0.3s}
        @keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        .message.user{justify-content:flex-end}
        .message.bot{justify-content:flex-start}
        .avatar{width:36px;height:36px;border-radius:18px;display:flex;align-items:center;justify-content:center;margin:0 8px;font-size:18px}
        .bot .avatar{background:linear-gradient(135deg,#7c3aed,#a855f7)}
        .user .avatar{background:linear-gradient(135deg,#ec489a,#a855f7);order:2}
        .bubble{max-width:70%;padding:10px 14px;border-radius:20px;font-size:14px;white-space:pre-wrap}
        .user .bubble{background:#7c3aed;color:white;border-bottom-right-radius:4px}
        .bot .bubble{background:rgba(31,41,55,0.9);border:1px solid #a855f7;color:#e5e7eb;border-bottom-left-radius:4px}
        .timestamp{font-size:9px;color:gray;margin-top:4px;text-align:right}
        .typing{display:flex;gap:5px;padding:10px 14px;background:rgba(31,41,55,0.9);border-radius:20px;width:fit-content}
        .typing span{width:7px;height:7px;background:#a855f7;border-radius:50%;animation:bounce 1.4s infinite}
        @keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-6px)}}
        .input-area{padding:12px;border-top:1px solid #a855f7}
        .input-wrap{display:flex;gap:10px}
        .input-wrap input{flex:1;background:rgba(31,41,55,0.9);border:1px solid #a855f7;border-radius:50px;padding:12px;color:white;outline:none}
        .send-btn{background:linear-gradient(135deg,#7c3aed,#a855f7);border:none;border-radius:50px;padding:12px 20px;color:white;cursor:pointer}
        .footer{text-align:center;font-size:10px;color:#6b7280}
        .status-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;margin-right:6px;animation:blink 1.5s infinite}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
        @media(max-width:550px){.bubble{max-width:85%}h1{font-size:28px}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🧠</div>
            <h1>🤝 TARIK BHAI</h1>
            <div class="gender-buttons">
                <button class="gender-btn" id="brotherBtn" onclick="selectGender('brother')">👨 भाई</button>
                <button class="gender-btn" id="sisterBtn" onclick="selectGender('sister')">👩 बहन</button>
            </div>
        </div>
        <div class="carousel"><div class="carousel-text" id="carouselText">🤝 मैं हूँ ना तेरे लिए 🤝</div></div>
        <div class="contact-row">
            <a href="https://wa.me/918984473230" class="contact-btn">📱 WhatsApp</a>
            <a href="https://www.instagram.com/tarik_islam_786/" class="contact-btn">📷 Instagram</a>
            <a href="mailto:princetarikislam@gmail.com" class="contact-btn">✉️ Email</a>
            <a href="tel:+918984473230" class="contact-btn">📞 Call</a>
        </div>
        <div class="chat-box">
            <div class="chat-header"><div><span class="status-dot"></span> Tarik Bhai - Always Here</div><button class="clear-btn" onclick="clearChat()">🗑️ Clear</button></div>
            <div class="messages" id="messages"><div class="message bot"><div class="avatar">🧠</div><div class="bubble"><strong>🤝 Assalamu Alaikum! 🤝</strong><br><br>Main hoon Tarik Bhai. Pehle batao - Bhai ya Behen?<br><br>👆 Upar select karo<br><br>Main hoon na tere liye hamesha!<div class="timestamp">⚡ Ready</div></div></div></div>
            <div class="input-area"><div class="input-wrap"><input type="text" id="messageInput" placeholder="💬 Bol bhai/behen, main sun raha hoon..." onkeypress="if(event.key==='Enter') sendMessage()"><button class="send-btn" onclick="sendMessage()">Send</button></div></div>
        </div>
        <div class="footer">📞 +91 8984473230 | 📧 princetarikislam@gmail.com | 📷 @tarik_islam_786</div>
    </div>
    <script>
        const msgs=["🤝 मैं हूँ ना तेरे लिए 🤝","💙 You are never alone - Main hoon na 💙","🌺 Merri pyaari behno, main hamesha tumhare liye hoon 🌺","🤗 Agar darr lage, toh bas ek message karo 🤗","💪 Tu strong hai, main tere saath hoon 💪"];
        let idx=0,carText=document.getElementById('carouselText');
        setInterval(()=>{idx=(idx+1)%msgs.length;carText.innerHTML=msgs[idx];},4000);
        let gender=null,cid=null,loading=false;
        const msgsDiv=document.getElementById('messages'),input=document.getElementById('messageInput');
        function getTime(){return new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
        function addMsg(role,text){const d=document.createElement('div');d.className=`message ${role}`;d.innerHTML=`<div class="avatar">${role==='user'?'👤':'🧠'}</div><div class="bubble">${text.replace(/\\n/g,'<br>')}<div class="timestamp">${getTime()}</div></div>`;msgsDiv.appendChild(d);d.scrollIntoView({behavior:'smooth'});}
        function showTyping(){const t=document.createElement('div');t.className='message bot';t.id='typing';t.innerHTML='<div class="avatar">🧠</div><div class="typing"><span></span><span></span><span></span></div>';msgsDiv.appendChild(t);t.scrollIntoView({behavior:'smooth'});}
        function hideTyping(){const t=document.getElementById('typing');if(t)t.remove();}
        function selectGender(g){gender=g;document.getElementById('brotherBtn').classList.remove('active');document.getElementById('sisterBtn').classList.remove('active');document.getElementById(g+'Btn').classList.add('active');msgsDiv.innerHTML='';if(g==='sister'){addMsg('bot','🌸 Namaste meri pyaari behna! Main hoon Tarik Bhai. Bol, main sun raha hoon. Tension mat le, main hoon na tere liye 🌸\n\n🤝 - Tera Bhai, Tarik');}else{addMsg('bot','💪 Namaste mere bhai! Main hoon Tarik Bhai. Bol, main sun raha hoon. Tension mat le, main hoon na tere saath 💪\n\n🤝 - Tera Bhai, Tarik');}}
        async function sendMessage(){const msg=input.value.trim();if(!msg||loading)return;if(!gender){addMsg('bot','🤝 Pehle batao - Bhai ya Behen? Upar select karo 👆');input.value='';return;}addMsg('user',msg);input.value='';loading=true;showTyping();try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,conversation_id:cid,gender:gender})});const d=await r.json();hideTyping();addMsg('bot',d.response);cid=d.conversation_id;}catch(e){hideTyping();addMsg('bot','🤝 Bhai/Behen, main hoon yahan. WhatsApp: 8984473230 💙');}loading=false;}
        async function clearChat(){if(cid)await fetch(`/clear/${cid}`,{method:'DELETE'});cid=null;msgsDiv.innerHTML='';if(gender==='sister'){addMsg('bot','🌸 Chat clear. Main abhi bhi yahan hoon. Batao kya baat karni hai? 🌸\n\n🤝 - Tera Bhai, Tarik');}else{addMsg('bot','💪 Chat clear. Main abhi bhi yahan hoon. Batao kya baat karni hai? 💪\n\n🤝 - Tera Bhai, Tarik');}}
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
    response = get_response(msg, gender)
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
    print("\n🤝 TARIK BHAI - YOUR BIG BROTHER 🤝")
    print("Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
