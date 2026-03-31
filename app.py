from flask import Flask, render_template_string, request, jsonify
import uuid
import random

app = Flask(__name__)
conversations = {}

def get_response(message):
    msg = message.lower()
    
    if any(w in msg for w in ['hi', 'hello', 'hey', 'salam', 'namaste']):
        return "💖 Hello meri pyaari behna! Main hoon Tarik Bhai. Kaise ho? Main sun raha hoon. Tension mat le, main hoon na tere liye.\n\n📞 WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['sad', 'alone', 'lonely', 'udaas', 'akeli']):
        return "💔 Meri pyaari behna, tu akeli nahi hai. Main hoon na tere liye hamesha.\n\n💙 Yaad rakhna: Tu strong hai, tu beautiful hai.\n\n📞 WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['scared', 'fear', 'dar', 'darr']):
        return "🛡️ Behen, dar mat! Main hoon na tere saath. Tu safe hai, tu protected hai.\n\n📞 WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['thank', 'thanks', 'shukriya']):
        return "🤝 Hamesha khushi se behna! Main hoon na tere liye.\n\n🤝 - Tera Bhai, Tarik"
    
    if any(w in msg for w in ['bye', 'exit']):
        return "🤝 Allah Hafiz behna! Yaad rakhna - main hoon na tere liye hamesha. WhatsApp: 8984473230\n\n🤝 - Tera Bhai, Tarik"
    
    return f"🤝 Meri pyaari behna, maine sun liya.\n\nMain yahan hoon tere liye. Jo bhi dil mein hai, share kar sakti ho. Koi judgment nahi, sirf pyaar.\n\n💙 Tu kabhi akeli nahi hai. Main hoon na.\n\n📞 WhatsApp: 8984473230 | 📸 Instagram: @tarik_islam_786\n\n🤝 - Tera Bhai, Tarik"

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tarik Bhai - Your Loving Brother</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#1a0a2a,#2a0a3a);font-family:system-ui;min-height:100vh;padding:16px}
.container{max-width:700px;margin:0 auto}
.header{background:rgba(255,255,255,0.08);border-radius:50px;padding:25px;text-align:center;border:1px solid #ec489a;margin-bottom:20px}
.logo{width:80px;height:80px;background:linear-gradient(135deg,#ec489a,#a855f7);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:40px;margin:0 auto 15px;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
h1{font-size:36px;background:linear-gradient(135deg,#ff99cc,#ec489a);-webkit-background-clip:text;color:transparent}
.tagline{color:#ec489a;font-size:14px}
.promise-card{background:rgba(236,72,153,0.15);border-radius:35px;padding:25px;text-align:center;border:1px solid #ec489a;margin-bottom:20px}
.carousel{background:rgba(255,255,255,0.05);border-radius:60px;padding:20px;text-align:center;border:1px solid #ec489a;margin-bottom:20px}
.carousel-text{font-size:16px;transition:0.5s}
.contact-grid{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:20px}
.contact-btn{background:rgba(255,255,255,0.08);border:1px solid #ec489a;border-radius:50px;padding:10px 20px;text-decoration:none;color:white;font-size:12px;display:inline-flex;align-items:center;gap:8px}
.chat-container{background:rgba(0,0,0,0.4);border-radius:35px;border:1px solid #ec489a;overflow:hidden}
.chat-header{display:flex;justify-content:space-between;padding:15px 20px;background:rgba(0,0,0,0.3);border-bottom:1px solid #ec489a}
.status-dot{width:10px;height:10px;background:#22c55e;border-radius:50%;display:inline-block;margin-right:8px;animation:blink 1.5s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
.clear-btn{background:rgba(239,68,68,0.2);border:1px solid #ef4444;color:#f87171;padding:6px 14px;border-radius:30px;cursor:pointer}
.messages{height:400px;overflow-y:auto;padding:20px}
.message{display:flex;margin-bottom:15px}
.message.user{justify-content:flex-end}
.message.bot{justify-content:flex-start}
.avatar{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 10px}
.bot .avatar{background:linear-gradient(135deg,#ec489a,#a855f7)}
.user .avatar{background:linear-gradient(135deg,#a855f7,#ec489a);order:2}
.bubble{max-width:75%;padding:12px 18px;border-radius:25px;font-size:14px;white-space:pre-wrap}
.user .bubble{background:linear-gradient(135deg,#ec489a,#a855f7);color:white}
.bot .bubble{background:rgba(255,255,255,0.1);border:1px solid #ec489a;color:#e5e7eb}
.time{font-size:9px;color:rgba(255,255,255,0.5);margin-top:6px}
.typing-indicator{display:flex;gap:6px;padding:12px 18px;background:rgba(255,255,255,0.1);border-radius:25px;width:fit-content}
.typing-dot{width:8px;height:8px;background:#ec489a;border-radius:50%;animation:bounce 1.4s infinite}
.typing-dot:nth-child(2){animation-delay:0.2s}
.typing-dot:nth-child(3){animation-delay:0.4s}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-8px)}}
.input-area{padding:16px 20px;border-top:1px solid #ec489a}
.input-wrapper{display:flex;gap:12px}
.input-wrapper input{flex:1;background:rgba(255,255,255,0.1);border:1px solid #ec489a;border-radius:50px;padding:14px 18px;color:white;outline:none}
.send-btn{background:linear-gradient(135deg,#ec489a,#a855f7);border:none;border-radius:50px;padding:14px 28px;color:white;cursor:pointer}
.footer{text-align:center;margin-top:20px;font-size:11px;color:rgba(255,255,255,0.4);padding:15px}
</style>
</head>
<body>
<div class="container">
<div class="header"><div class="logo">💖</div><h1>🤝 TARIK BHAI</h1><div class="tagline">✨ TERA BHAI - HAMESHA TERE LIYE ✨</div></div>
<div class="promise-card"><div style="font-size:45px;">💖</div><div style="margin:15px 0"><strong>Meri Pyaari Behen</strong><br><br>Main hoon Tarik Bhai - tera bada bhai. Tu kabhi akeli nahi hai. Main hoon na tere liye - hamesha.</div></div>
<div class="carousel"><div class="carousel-text" id="carouselText">💖 मैं हूँ ना तेरे लिए - हमेशा 💖</div></div>
<div class="contact-grid"><a href="https://wa.me/918984473230" class="contact-btn">📱 WhatsApp</a><a href="https://www.instagram.com/tarik_islam_786/" class="contact-btn">📷 Instagram</a><a href="mailto:princetarikislam@gmail.com" class="contact-btn">✉️ Email</a><a href="tel:+918984473230" class="contact-btn">📞 Call</a></div>
<div class="chat-container"><div class="chat-header"><div><span class="status-dot"></span> Tarik Bhai - Always Here for You 💙</div><button class="clear-btn" onclick="clearChat()">Clear</button></div>
<div class="messages" id="messages"><div class="message bot"><div class="avatar">💖</div><div class="bubble"><strong>💖 Assalamu Alaikum meri pyaari behna!</strong><br><br>Main hoon Tarik Bhai - tera bada bhai. Main yahan hoon tere liye - hamesha.<br><br>Jo bhi dil mein hai, jo bhi dard hai - share kar sakti ho. Main sun raha hoon.<br><div class="time">⚡ Always Here</div></div></div></div>
<div class="input-area"><div class="input-wrapper"><input type="text" id="messageInput" placeholder="💬 Bol behna... main sun raha hoon..." onkeypress="if(event.key==='Enter') sendMessage()"><button class="send-btn" onclick="sendMessage()">Send</button></div></div></div>
<div class="footer">📞 +91 8984473230 | 📧 princetarikislam@gmail.com | 📷 @tarik_islam_786<br>💙 Tu kabhi akeli nahi hai - Main hoon na 💙</div>
</div>
<script>
var msgs=["💖 मैं हूँ ना तेरे लिए - हमेशा 💖","💙 You are never alone - I am here for you 💙","🌸 Tu meri behen hai - main hoon na tere liye 🌸","🤗 Agar darr lage - bas ek message karo 🤗","💪 Tu strong hai - main tere saath hoon 💪","❤️ Koi problem ho toh bolna - saath mein solve karenge ❤️"];
var idx=0,carText=document.getElementById("carouselText");
setInterval(function(){idx=(idx+1)%msgs.length;carText.innerHTML=msgs[idx];},4000);
var cid=null,loading=false;
var msgsDiv=document.getElementById("messages"),input=document.getElementById("messageInput");
function getTime(){return new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
function addMsg(role,text){var d=document.createElement("div");d.className="message "+role;var icon=role==="user"?"👤":"💖";d.innerHTML='<div class="avatar">'+icon+'</div><div class="bubble">'+text.replace(/\\n/g,"<br>")+'<div class="time">'+getTime()+'</div></div>';msgsDiv.appendChild(d);d.scrollIntoView({behavior:"smooth"});}
function showTyping(){var t=document.createElement("div");t.className="message bot";t.id="typing";t.innerHTML='<div class="avatar">💖</div><div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>';msgsDiv.appendChild(t);t.scrollIntoView({behavior:"smooth"});}
function hideTyping(){var t=document.getElementById("typing");if(t)t.remove();}
async function sendMessage(){var msg=input.value.trim();if(!msg||loading)return;addMsg("user",msg);input.value="";loading=true;showTyping();try{var r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:msg,conversation_id:cid})});var d=await r.json();hideTyping();addMsg("bot",d.response);cid=d.conversation_id;}catch(e){hideTyping();addMsg("bot","💖 Behen, thoda technical issue. WhatsApp karo: 8984473230 💙");}loading=false;}
async function clearChat(){if(cid)await fetch("/clear/"+cid,{method:"DELETE"});cid=null;msgsDiv.innerHTML="";addMsg("bot","💖 Chat clear. Main abhi bhi yahan hoon. Yaad rakhna - tu kabhi akeli nahi hai 💖\n\n🤝 - Tera Bhai, Tarik");}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '')
    cid = data.get('conversation_id')
    if not cid:
        cid = str(uuid.uuid4())
    response = get_response(msg)
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
    app.run(host='0.0.0.0', port=5000, debug=False)
